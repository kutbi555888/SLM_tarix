"""Model tuzilmasi va uning tekshiruvlari; o'qitish algoritmi bu faylda emas."""

from dataclasses import dataclass, asdict, fields
from src.paths import read_yaml


@dataclass
class ModelConfig:
    vocab_size: int = 4096
    block_size: int = 128
    n_embd: int = 128
    n_layer: int = 4
    n_head: int = 4
    dropout: float = 0.1
    ffn_mult: int = 4
    tie_weights: bool = True

    def check(self):
        for name in (
            "vocab_size",
            "block_size",
            "n_embd",
            "n_layer",
            "n_head",
            "ffn_mult",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} musbat butun son bo'lishi kerak.")
        if self.n_embd % self.n_head:
            raise ValueError("n_embd n_head ga qoldiqsiz bo'linishi kerak.")
        if not 0 <= self.dropout < 1:
            raise ValueError("dropout 0 va 1 oralig'ida, 1 dan kichik bo'lsin.")
        if not isinstance(self.tie_weights, bool):
            raise ValueError("tie_weights true yoki false bo'lishi kerak.")

    def head_dim(self):
        return self.n_embd // self.n_head

    def to_dict(self):
        return asdict(self)

    def estimate_parameters(self):
        # Ikki norm, attention va MLP ning vaznlari hamda biaslari sanaladi.
        d, m = self.n_embd, self.ffn_mult
        block = (4 + 2 * m) * d * d + (9 + m) * d
        total = self.vocab_size * d + self.block_size * d + self.n_layer * block + 2 * d
        if not self.tie_weights:
            total += self.vocab_size * d
        return {"total": total, "per_block": block}

    def estimate_training_memory_mb(self):
        # Vazn, gradient va AdamW ning ikkita holati: taxminan 16 bayt/parametr.
        # Aktivatsiyalar, vaqtinchalik hisoblar va qurilma xarajatlari qo'shimcha.
        return self.estimate_parameters()["total"] * 16 / 1024**2


def load_config(path, vocab_size=None):
    values = read_yaml(path)
    cfg = ModelConfig(
        **{f.name: values[f.name] for f in fields(ModelConfig) if f.name in values}
    )
    if vocab_size is not None:
        cfg.vocab_size = vocab_size
    cfg.check()
    return cfg
