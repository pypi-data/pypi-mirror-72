import numpy as np
import time
from datetime import datetime


class EventPrinter:
    def __init__(self, run=None):
        self.run = run
        self.updates_after_header = 0
        self.created = time.time()
        self.val_loss = None

    def pretty_print(self, data):
        if data["object"] == "headers":
            print(
                f"{data['created_by']['run']} created from {data['created_by']['plan']} at {datetime.fromtimestamp(data['created'])}"
            )
            self.updates_after_header = 0
            self.created = data["created"]
        elif data["object"] == "text_completion":
            if data["choices"][0]["logprobs"] is None:
                print("Completions:")
                for choice in data["choices"]:
                    print(f"---\n{choice['text']}")
                self.updates_after_header = 0
            else:
                logprobs = [
                    c["logprobs"]["token_logprobs"][1:] for c in data["choices"]
                ]
                logprobs = np.array(logprobs)
                self.val_loss = -logprobs.mean()
                print(self.val_loss)

        elif data["object"] == "snapshot":
            print(f"Created snapshot {data['id']}")
            self.updates_after_header = 0
        elif data["object"] == "update":
            print_data = {
                "elapsed (s)": data["created"] - self.created,
                # TODO - replace by fraction done?
                "loss": -data["loss"],
                "scale": data["scale"],
                "tokens": data["tokens"],
            }
            print_data["val_loss"] = self.val_loss
            if self.run is not None:
                # used as a run event reader (not in sync mode finetuning)
                print_data["plan line"] = data["created_by"]["lineno"]
                print_data["completed"] = (
                    data["created_by"]["lineno"] / self.run.total_lines
                )
            self.val_loss = None
            if self.updates_after_header % 10 == 0:
                print(f"\n{' | '.join([k.rjust(12) for k in print_data.keys()])}")
            print(" | ".join(fixed_width(v) for v in print_data.values()))
            self.updates_after_header += 1
        else:
            raise ValueError(f"Unknown event type: {data['object']}")


def fixed_width(v, width=12):
    if isinstance(v, float):
        fmt = "{:" + str(width) + ".3g}"
        return fmt.format(v)
    else:
        return "".join([" "] * (width - len(str(v))) + [str(v)])
