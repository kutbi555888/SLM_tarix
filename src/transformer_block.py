"""Bitta blok: normallashtirish, attention, qoldiq qo'shish va MLP."""

from torch import nn
from src.attention import CausalSelfAttention
from src.mlp import FeedForward


class TransformerBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.ffn = FeedForward(config)

    def forward(self, x):
        # Qoldiq ulanish oldingi tasvirni saqlaydi va gradient o'tishini yengillashtiradi.
        x = x + self.attn(self.ln_1(x))
        return x + self.ffn(self.ln_2(x))
