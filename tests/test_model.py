"""Model shakli, kelajakdan ma'lumot sizmasligi va o'rganishini tekshiradi."""

import math
import pytest
import torch
from src.model import OurLLM
from src.model_config import ModelConfig


def kichik_sozlama(**values):
    args = dict(
        vocab_size=32, block_size=8, n_embd=16, n_layer=2, n_head=2, dropout=0.0
    )
    args.update(values)
    return ModelConfig(**args)


@pytest.mark.parametrize("tied", [True, False])
def test_parametrlar_va_shakl(tied):
    cfg = kichik_sozlama(tie_weights=tied)
    model = OurLLM(cfg)
    x = torch.randint(32, (2, 8))
    logits, loss = model(x, x)
    assert logits.shape == (2, 8, 32)
    assert math.isfinite(loss.item()) and 2 < loss.item() < 5
    assert model.num_parameters() == cfg.estimate_parameters()["total"]
    assert (model.lm_head.weight is model.token_embedding.weight) == tied


def test_kelajak_tokeni_oldingiga_tasir_qilmaydi():
    model = OurLLM(kichik_sozlama()).eval()
    x = torch.randint(32, (1, 8))
    altered = x.clone()
    altered[:, 4:] = (altered[:, 4:] + 1) % 32
    with torch.no_grad():
        a, _ = model(x)
        b, _ = model(altered)
    torch.testing.assert_close(a[:, :4], b[:, :4], atol=1e-6, rtol=1e-6)


def test_bitta_paketni_organadi():
    model = OurLLM(kichik_sozlama())
    x = torch.arange(8)[None, :].repeat(2, 1)
    y = (x + 1) % 32
    optimizer = model.configure_optimizers(0, 0.02)
    initial = model(x, y)[1].item()
    for _ in range(40):
        optimizer.zero_grad()
        loss = model(x, y)[1]
        loss.backward()
        optimizer.step()
    assert model(x, y)[1].item() < initial * 0.2


def test_notogri_tuzilma_rad_etiladi():
    with pytest.raises(ValueError):
        OurLLM(kichik_sozlama(n_head=3))
    with pytest.raises(ValueError):
        OurLLM(kichik_sozlama())(torch.zeros(1, 9, dtype=torch.long))
