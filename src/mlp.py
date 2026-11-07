"""Har bir token vektorini alohida qayta ishlaydigan ikki chiziqli qatlam."""

from torch import nn


class FeedForward(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, config.ffn_mult * config.n_embd),
            nn.GELU(),  # Chiziqli bo'lmagan o'zgarish murakkab bog'lanishni o'rganishga yordam beradi.
            nn.Linear(config.ffn_mult * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout),
        )

    def forward(self, x):
        return self.net(x)
