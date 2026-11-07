"""Keyingi tokenni bashorat qiluvchi kichik, faqat decoder asosidagi Transformer."""

import torch
from torch import nn
from torch.nn import functional as F
from src.transformer_block import TransformerBlock


class OurLLM(nn.Module):
    def __init__(self, config):
        super().__init__()
        config.check()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.n_embd)
        self.position_embedding = nn.Embedding(config.block_size, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList(
            TransformerBlock(config) for _ in range(config.n_layer)
        )
        self.ln_f = nn.LayerNorm(config.n_embd)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        self.apply(self._init_weights)
        if config.tie_weights:
            self.lm_head.weight = self.token_embedding.weight

    def _init_weights(self, layer):
        if isinstance(layer, (nn.Linear, nn.Embedding)):
            nn.init.normal_(layer.weight, mean=0.0, std=0.02)
            if isinstance(layer, nn.Linear) and layer.bias is not None:
                nn.init.zeros_(layer.bias)

    def num_parameters(self):
        # parameters() umumiy vaznni o'zi bir marta sanaydi; yana ayirmaymiz.
        return sum(p.numel() for p in self.parameters())

    def forward(self, idx, targets=None):
        if idx.ndim != 2 or not 1 <= idx.shape[1] <= self.config.block_size:
            raise ValueError(
                "Kirish (batch, vaqt) shaklida va kontekst chegarasida bo'lsin."
            )
        positions = torch.arange(idx.shape[1], device=idx.device)
        x = self.dropout(self.token_embedding(idx) + self.position_embedding(positions))
        for block in self.blocks:
            x = block(x)
        logits = self.lm_head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), targets.reshape(-1)
            )
        return logits, loss

    def configure_optimizers(self, weight_decay, lr, betas=(0.9, 0.95)):
        # Matritsalar uchun vaznni kamaytirish; bias va norm koeffitsiyentlariga qo'llanmaydi.
        groups = [
            {
                "params": [p for p in self.parameters() if p.ndim >= 2],
                "weight_decay": weight_decay,
            },
            {
                "params": [p for p in self.parameters() if p.ndim < 2],
                "weight_decay": 0.0,
            },
        ]
        return torch.optim.AdamW(groups, lr=lr, betas=betas)
