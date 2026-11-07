"""Modelni qanday o'qitish kerakligini belgilaydigan sozlamalar."""

from dataclasses import dataclass, fields
from src.paths import read_yaml


@dataclass
class TrainConfig:
    batch_size: int = 8
    grad_accum_steps: int = 2
    max_steps: int = 800
    warmup_steps: int = 40
    lr_max: float = 0.0005
    min_lr_ratio: float = 0.1
    weight_decay: float = 0.1
    beta1: float = 0.9
    beta2: float = 0.95
    grad_clip: float = 1.0
    log_interval: int = 20
    eval_interval: int = 100
    eval_iters: int = 10
    checkpoint_interval: int = 100
    seed: int = 42
    precision: str = "auto"
    num_threads: int = 2
    out_dir: str = "checkpoints"

    def check(self):
        for name in (
            "batch_size",
            "grad_accum_steps",
            "max_steps",
            "log_interval",
            "eval_interval",
            "eval_iters",
            "checkpoint_interval",
            "num_threads",
        ):
            v = getattr(self, name)
            if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
                raise ValueError(f"{name} musbat butun son bo'lsin.")
        if not 0 <= self.warmup_steps < self.max_steps:
            raise ValueError("warmup_steps max_steps dan kichik bo'lsin.")
        if self.lr_max <= 0 or self.grad_clip <= 0 or not 0 < self.min_lr_ratio <= 1:
            raise ValueError("O'rganish tezligi va gradient chegarasi noto'g'ri.")
        if self.precision not in {"auto", "fp32", "fp16", "bf16"}:
            raise ValueError("precision qiymati noto'g'ri.")

    def tokens_per_step(self, block_size):
        return self.batch_size * self.grad_accum_steps * block_size


def load_train_config(path):
    values = read_yaml(path)
    cfg = TrainConfig(
        **{f.name: values[f.name] for f in fields(TrainConfig) if f.name in values}
    )
    cfg.check()
    return cfg
