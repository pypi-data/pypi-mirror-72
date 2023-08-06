import logging
import os.path as osp
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional
import openai

from .load_dataset import load_dataset, Sampler
from . import data_streams

logger = logging.getLogger(__name__)


@contextmanager
def scoped_log(message):
    tstart = time.time()
    logger.info(f"▕▔ {message}")
    yield
    logger.info(f"▕▁ Done in {time.time()-tstart:.2f} seconds")


@dataclass
class FinetuningHps:
    train_paths: list
    val_paths: list
    num_epochs: int = 1
    train_batch_size: int = 32
    val_batch_size: int = 50
    max_tokens: int = 2048
    update_scale: float = 1.0
    create_plan: bool = True
    plan_output_file: Optional[str] = None
    completions_every: int = 5
    n_completions: int = 1
    completion_tokens: int = 128
    completion_temperature: float = 0.4
    snapshots_every: int = 100


def train(planner, hps):
    stream_kwargs = dict(tokens_per_example=hps.max_tokens)
    enc = planner.make_encoding()
    for iepoch in range(hps.num_epochs):
        decayed_scale = hps.update_scale * (1 - iepoch / hps.num_epochs)
        train_it = data_streams.stream_from_files(
            hps.train_paths,
            **stream_kwargs,
            batch_size=hps.train_batch_size,
            seed=iepoch,
            enc=enc,
        )
        val_it = (
            data_streams.stream_from_files(
                hps.val_paths,
                **stream_kwargs,
                batch_size=hps.val_batch_size,
                seed=iepoch,
                enc=enc,
                forever=True,
            )
            if len(hps.val_paths) > 0
            else None
        )
        with scoped_log(f"Running epoch: {iepoch}"):
            for i, batch in enumerate(train_it):
                if hps.completions_every > 0 and i % hps.completions_every == 0:
                    ### Sampling eval
                    planner.add(
                        "POST /v1/completions",
                        n=hps.n_completions,
                        max_tokens=hps.completion_tokens,
                        temperature=hps.completion_temperature,
                        echo=True,
                    )

                if hps.snapshots_every > 0 and i > 0 and i % hps.snapshots_every == 0:
                    planner.add(
                        "POST /v1/snapshots",
                        description=f"Step {i} of openai-finetune",
                    )

                # Training batch
                # TODO in-epoch update_scale planner, probably cosine
                planner.add(
                    "POST /v1/updates",
                    example=batch["tokens"],
                    mask=batch["mask"],
                    scale=decayed_scale,
                )

                if val_it is not None:
                    val_batch = next(val_it)
                    planner.add(
                        "POST /v1/completions",
                        prompt=val_batch["tokens"],
                        logprobs=0,
                        max_tokens=0,
                        echo=True,
                    )


def save_snapshot(planner, epoch):
    planner.add("POST /v1/snapshots", description=f"Epoch {epoch} of openai-finetune")


def eval_step(planner, batch):
    planner.add(
        "POST /v1/completions",
        prompt=batch["tokens"],
        logprobs=0,
        max_tokens=0,
        echo=True,
    )


def train_epoch(planner, data_iterator, epnum, update_scale):
    toks_done = 0
    tokens = []

    last_update = None
    last_toks = None


def val_epoch(planner, data_iterator):
    for batch in data_iterator:
        eval_step(planner, batch)
