"""O'rganish tezligi avval oshadi, so'ng kosinus bo'yicha pasayadi."""

import math


def get_lr(step, config):
    if step < config.warmup_steps:
        return config.lr_max * (step + 1) / max(1, config.warmup_steps)
    progress = (step - config.warmup_steps) / max(
        1, config.max_steps - config.warmup_steps - 1
    )
    progress = min(1.0, max(0.0, progress))
    factor = config.min_lr_ratio + (1 - config.min_lr_ratio) * 0.5 * (
        1 + math.cos(math.pi * progress)
    )
    return config.lr_max * factor
