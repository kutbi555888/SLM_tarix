"""To'xtatib tiklash uzluksiz o'qitish bilan bir xil natija berishini tekshiradi."""

from dataclasses import replace
import pytest
import torch
from src.model import OurLLM
from src.model_config import ModelConfig
from src.train_config import TrainConfig
from src.trainer import Trainer
from src.seed import set_seed
from src.checkpoint import read_checkpoint


class SinovMalumoti:
    def get_batch(self, path, batch_size, block_size, generator, dtype):
        start = torch.randint(24, (batch_size, 1), generator=generator)
        x = (start + torch.arange(block_size)[None, :]) % 32
        return x, (x + 1) % 32


def test_checkpoint_davomi_bir_xil(tmp_path):
    mc = ModelConfig(
        vocab_size=32, block_size=8, n_embd=16, n_layer=1, n_head=2, dropout=0.2
    )
    cfg = TrainConfig(
        batch_size=2,
        grad_accum_steps=2,
        max_steps=4,
        warmup_steps=1,
        eval_iters=1,
        log_interval=2,
        eval_interval=2,
        checkpoint_interval=2,
        precision="fp32",
    )
    meta = {
        "dtype": "uint16",
        "tokenizer_sha256": "sinov",
        "sha256_train": "a",
        "sha256_val": "b",
        "sha256_test": "c",
    }

    def yarat(out, seed=42, metadata=None):
        set_seed(seed)
        return Trainer(
            OurLLM(mc),
            SinovMalumoti(),
            mc,
            replace(cfg, out_dir=str(tmp_path / out)),
            metadata or meta,
            "cpu",
        )

    full = yarat("uzluksiz")
    full.train()
    half = yarat("bolingan")
    half.train(stop_after=2)
    resumed = yarat("bolingan", 999)
    resumed.train(resume=tmp_path / "bolingan/last.pt")
    for name, value in full.model.state_dict().items():
        torch.testing.assert_close(
            value, resumed.model.state_dict()[name], atol=0, rtol=0
        )
    assert read_checkpoint(tmp_path / "bolingan/last.pt")["step"] == 4
    assert "optimizer_state" not in read_checkpoint(tmp_path / "bolingan/model.pt")
    wrong = yarat("xato", metadata={**meta, "sha256_train": "ozgargan"})
    with pytest.raises(ValueError, match="Dataset"):
        wrong.resume(tmp_path / "bolingan/last.pt")
