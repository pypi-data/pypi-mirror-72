"""
A concise implementation of data loading & batching.
For fine-tuning on small datasets, we can't afford to drop any of the data, so we've
reimplemented this functionality from data gym
"""
import random
import json
import itertools
import blobfile

from .load_dataset import load_dataset, Sampler
import numpy as np


def shuffle_stream(stream, bufsize, seed=None):
    """
    Use a shuffle buffer to reorder sequence
    """
    rng = random.Random(seed)
    buf = []
    while True:
        buf = list(itertools.islice(stream, bufsize))
        if not buf:
            break
        rng.shuffle(buf)
        yield from buf


def read_lines(filename):
    """
    Read all lines of a jsonl file, return sequence of dicts
    """
    with blobfile.BlobFile(filename, "r") as fh:
        if filename.endswith("jsonl"):
            for line in fh:
                yield json.loads(line)
        elif filename.endswith("txt"):
            yield {"data": fh.read()}
        else:
            raise ValueError(
                f"File type could not be inferred for {filename}. (HINT: if this is a text file, try renaming to {filename}.txt)"
            )


def get_all_lines(filenames):
    """
    Return all lines from a list of files
    """
    for filename in filenames:
        yield from read_lines(filename)


def slice_stream(stream, start, step):
    while True:
        chunk = list(itertools.islice(stream, step))
        if len(chunk) == step:  # Ensure that all shards yield exactly the same
            yield chunk[start]  # sequence length
        else:
            break


def encode_data(encoder, data):
    if isinstance(data, dict):
        keys = set(data.keys())
        if keys == {"tokens"}:
            tokens = data["tokens"]
            masks = [[1.0 for t in ts] for ts in tokens]
        elif data.keys() == {"text_list"}:
            tokens = [encoder.encode(text) for text in data["text_list"]]
            masks = [[1.0 for t in ts] for ts in tokens]
        elif data.keys() == {"text_list", "loss_weights"}:
            tokens = [encoder.encode(text) for text in data["text_list"]]
            masks = data["loss_weights"]
        else:
            raise NotImplementedError(
                f"Don't know what to do with these keys: {data.keys()}"
            )

    elif isinstance(data, str):
        tokens = [encoder.encode(data)]
        masks = [[1.0] * len(tokens[0])]

    # elif isinstance(data, dict):
    #     keys = set(data.keys())
    #     if keys == {"text"}:
    #         assert False
    #         add(data["text"], 1.0)
    #     elif keys == {"texts"}:
    #         assert False
    #         for text in data["texts"]:
    #             add(text, 1.0)
    #     elif keys == {"tokens"}:
    #         for tokens_ in data["tokens"]:
    #             add(tokens_, [1.0 for t in tokens_], text=False)
    #     else:
    #         raise NotImplementedError(
    #             f"Don't know what to do with these keys: {data.keys()}"
    #         )
    # else:
    #     raise NotImplementedError(f"invalid data type: {type(data)}")
    # TODO: bring back?
    #     pairs.append((encoder.eot_token, 1.0))
    max_len = 2048
    tokens = [ts[:max_len] for ts in tokens]
    masks = [ms[:max_len] for ms in masks]
    return dict(tokens=tokens, mask=masks)


def safezip(xs, ys):
    assert len(xs) == len(ys)
    return zip(xs, ys)


def pack_stream(it, tokens_per_example, overlap):
    buf = []
    for x in it:
        buf.extend(x)
        while len(buf) >= tokens_per_example:
            yield buf[:tokens_per_example]
            buf = buf[tokens_per_example - overlap :]
    if buf:
        yield buf


def cat(ds):
    assert len(ds) > 0
    keys = ds[0].keys()
    out = {k: [] for k in keys}
    for d in ds:
        for k in keys:
            out[k].append(d[k])
    return out
    # return {k: [t for e in v for t in e] for k, v in out.items()}


def batch_tensors(it, batchsize, pad_elem, allow_partial_batch=False):
    done = False
    while not done:
        batch = list(itertools.islice(it, batchsize))
        done = len(batch) < batchsize
        force = allow_partial_batch and len(batch) > 0
        if done and not force:
            continue
        if len(batch) > 1:  # pad everything to longest length in batch
            maxlen = max(len(el["tokens"]) for el in batch)
            batch = [timepad_dict(el, pad_elem, maxlen) for el in batch]
        yield cat(batch)


def timepad_dict(d, pad_elem, newsize):
    return {
        "tokens": timepad(d["tokens"], pad_elem, newsize),
        "mask": timepad(d["mask"], 0, newsize),
    }


def timepad(lst, pad_elem, newsize):
    "Pad tensor along time dimension to have a certain size"
    return lst + [pad_elem] * (newsize - len(lst))


def to_tensors(pairs):
    tokens, masks = zip(*pairs)
    return dict(tokens=[tokens], mask=[masks])
    # return dict(
    #     tokens=np.array([tokens], dtype=np.int64).tolist(),
    #     mask=np.array([masks], dtype=np.float32).tolist(),
    # )


def encode_and_flatten(it, encoder):
    for jsonobj in it:
        encoded = encode_data(encoder, jsonobj["data"])
        for t, m in zip(encoded["tokens"], encoded["mask"]):
            yield {"tokens": t, "mask": m}


def stream_from_files(
    files,
    tokens_per_example,
    *,
    enc,
    seed=None,
    shard_idx=0,
    num_shards=1,
    shuffle=True,
    overlap=1,
    batch_size=1,
    pack=True,
    allow_partial_batch=False,
    forever=False,
):
    it = iter(files)
    if shuffle:
        it = shuffle_stream(it, bufsize=100, seed=seed)
    it = get_all_lines(it)  # dictionaries
    # it = slice_stream(it, start=shard_idx, step=num_shards)  # Shard by lines not files
    if forever:
        it = itertools.cycle(it)
    if shuffle:
        it = shuffle_stream(it, bufsize=1_000_000, seed=seed)
    it = encode_and_flatten(it, enc)
    # if pack:
    #     it = pack_stream(it, tokens_per_example, overlap=overlap)
    # it = map(to_tensors, it)
    it = batch_tensors(
        it, batch_size, pad_elem=enc.eot_token, allow_partial_batch=allow_partial_batch
    )
    return it


def estimate_num_tokens(files, seed=0, n_samples=200, *, enc):
    """
    Estimate number of tokens by randomly sampling a subset and encoding them
    encoding is the slow part
    """
    rng = random.Random(seed)
    it = iter(files)
    all_lines = list(get_all_lines(it))  # dictionaries
    subset_lines = rng.sample(all_lines, min(n_samples, len(all_lines)))
    subset_sizes = [len(encode_data(enc, jsonobj)) for jsonobj in subset_lines]
    mean = np.mean(subset_sizes)
    if len(subset_lines) == len(all_lines):
        mean_stderr = 0
    else:
        mean_stderr = np.std(subset_sizes) / np.sqrt(len(subset_sizes))
    factor = len(all_lines)
    return int(mean * factor), mean_stderr * factor
