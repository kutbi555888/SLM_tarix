"""Model, optimizer, tasodifiy holatlar va keyingi qadamni saqlash/tiklash."""

import os
import tempfile
import random
import numpy as np
import torch
from src.paths import project_path


def atomic_save(payload, path):
    path = project_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    os.close(fd)
    try:
        torch.save(payload, tmp)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def capture_rng():
    state = np.random.get_state()
    return {
        "python": random.getstate(),
        "numpy": [state[0], state[1].tolist(), state[2], state[3], state[4]],
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng(state):
    random.setstate(state["python"])
    s = state["numpy"]
    np.random.set_state((s[0], np.asarray(s[1], dtype=np.uint32), s[2], s[3], s[4]))
    torch.set_rng_state(state["torch"].cpu())
    if torch.cuda.is_available() and state["cuda"]:
        torch.cuda.set_rng_state_all([s.cpu() for s in state["cuda"]])


def read_checkpoint(path, device="cpu"):
    return torch.load(project_path(path), map_location=device, weights_only=True)


def export_model(payload, path):
    keys = (
        "model_state",
        "model_config",
        "step",
        "best_val_loss",
        "tokenizer_sha256",
        "data_sha256",
    )
    result = {k: payload[k] for k in keys}
    result["purpose"] = (
        "O'quv tajribasi; tarixiy faktlarni tekshirmasdan ishonchli javob deb qabul qilmang."
    )
    atomic_save(result, path)
