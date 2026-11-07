"""O'rtacha token xatosi, perplexity va sodda taqqoslash modellari."""

import math
import numpy as np
import torch
from src.paths import project_path


def perplexity(loss):
    """Perplexity = exp(loss). Kichikroq qiymat odatda yaxshiroq."""
    return math.exp(loss) if loss < 700 else float("inf")


@torch.inference_mode()
def full_split_loss(model, path, block_size, device, dtype="uint16", max_blocks=None):
    data = np.memmap(project_path(path), dtype=dtype, mode="r")
    if len(data) < 2:
        raise ValueError("Baholash uchun kamida 2 token kerak.")
    was_training = model.training
    model.eval()
    total, count = 0.0, 0
    # Oxirgi qisqa bo'lak ham hisobga olinadi; har nishon bir marta baholanadi.
    for block, start in enumerate(range(0, len(data) - 1, block_size)):
        if max_blocks is not None and block >= max_blocks:
            break
        end = min(start + block_size, len(data) - 1)
        x = torch.tensor(
            np.asarray(data[start:end], dtype=np.int64)[None, :], device=device
        )
        y = torch.tensor(
            np.asarray(data[start + 1 : end + 1], dtype=np.int64)[None, :],
            device=device,
        )
        _, loss = model(x, y)
        total += loss.item() * y.numel()
        count += y.numel()
    model.train(was_training)
    return {
        "loss": total / count,
        "scored_tokens": count,
        "total_targets": len(data) - 1,
        "complete": count == len(data) - 1,
        "protocol": "Kontekst har blok boshida yangilanadi.",
    }


def random_baseline_loss(vocab_size):
    return math.log(vocab_size)


def bigram_baseline_loss(train_path, val_path, vocab_size, dtype="uint16", alpha=0.1):
    """Oldingi bitta tokenga asoslangan model; sanash faqat train faylida."""
    train = np.asarray(
        np.memmap(project_path(train_path), dtype=dtype, mode="r"), dtype=np.int64
    )
    val = np.asarray(
        np.memmap(project_path(val_path), dtype=dtype, mode="r"), dtype=np.int64
    )
    keys, counts = np.unique(train[:-1] * vocab_size + train[1:], return_counts=True)
    pairs = dict(zip(keys.tolist(), counts.tolist()))
    totals = np.bincount(train[:-1], minlength=vocab_size)
    nll = 0.0
    for left, right in zip(val[:-1], val[1:]):
        p = (pairs.get(int(left) * vocab_size + int(right), 0) + alpha) / (
            totals[left] + alpha * vocab_size
        )
        nll -= math.log(p)
    return nll / max(1, len(val) - 1)
