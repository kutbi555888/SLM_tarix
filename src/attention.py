"""Tokenlar o'zidan oldingi tokenlardan kerakli ma'lumotni oladi."""

import torch.nn as nn
from torch.nn import functional as F


class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.n_head = config.n_head
        self.head_dim = config.head_dim()
        self.dropout = config.dropout
        self.qkv_proj = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.out_proj = nn.Linear(config.n_embd, config.n_embd)
        self.resid_dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        b, t, c = x.shape
        # Q — nimani qidirish; K — nimaga mos kelish; V — uzatiladigan ma'lumot.
        q, k, v = self.qkv_proj(x).chunk(3, dim=-1)
        q, k, v = [
            a.view(b, t, self.n_head, self.head_dim).transpose(1, 2) for a in (q, k, v)
        ]
        # is_causal=True kelajak tokenlarini berkitadi. Baholashda dropout 0.
        out = F.scaled_dot_product_attention(
            q, k, v, is_causal=True, dropout_p=self.dropout if self.training else 0.0
        )
        out = out.transpose(1, 2).contiguous().view(b, t, c)
        return self.resid_dropout(self.out_proj(out))
