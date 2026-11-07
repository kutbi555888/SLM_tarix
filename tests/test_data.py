"""Matn yo'qolmasligi, qismlar ajralishi va paket chegaralarini tekshiradi."""

import math
import numpy as np
import torch
from src.tokenizer import Tokenizer
from src.dataset_builder import DatasetBuilder, split_documents
from src.deduplicator import document_hash
from src.data_filter import inspect_document, show_filter_examples
from src.model import OurLLM
from src.model_config import ModelConfig
from evaluation.perplexity import full_split_loss


def test_tokenizer_matnni_qaytaradi(tmp_path):
    tok = Tokenizer().train(["Tarix va madaniyat. O'zbek tili."], vocab_size=300)
    text = "O‘zbekcha, g‘oya, 123, 🙂, Ж — sinov!"
    assert tok.decode(tok.encode(text)) == text
    path = tmp_path / "tokenizer.json"
    tok.save(path)
    assert Tokenizer().load(path).decode(tok.encode(text)) == text


def test_qismlar_aralashmaydi():
    rows = [{"id": str(i), "text": f"hujjat {i}"} for i in range(40)]
    splits = split_documents(rows)
    ids = [{r["id"] for r in splits[s]} for s in ("train", "val", "test")]
    assert not (ids[0] & ids[1] or ids[0] & ids[2] or ids[1] & ids[2])
    assert len(set.union(*ids)) == 40
    assert splits == split_documents(rows)


def test_oxirgi_paket_olinadi(tmp_path):
    path = tmp_path / "tokens.bin"
    np.arange(7, dtype=np.uint16).tofile(path)
    x, y = DatasetBuilder().get_batch(path, 100, 5, torch.Generator().manual_seed(42))
    assert {int(v) for v in x[:, 0]} == {0, 1}
    assert torch.equal(y, x + 1)


def test_filtr_sababi_va_namunasi(capsys):
    cfg = {
        "min_chars": 20,
        "max_chars": 1000,
        "min_alpha_ratio": 0.4,
        "max_repeated_line_ratio": 0.3,
    }
    row = inspect_document({"text": "123", "id": "a"}, cfg)
    assert row["status"] == "rejected" and set(row["failed_rules"]) == {
        "min_chars",
        "alpha_ratio",
    }
    chosen = show_filter_examples([row], "rejected", 10)
    assert len(chosen) == 1 and "123" in capsys.readouterr().out
    assert document_hash(" TARIX   va MADANIYAT ") == document_hash(
        "tarix va madaniyat"
    )


def test_baholash_oxirgi_qisqa_bolakni_ham_sanaydi(tmp_path):
    path = tmp_path / "tokens.bin"
    np.arange(10, dtype=np.uint16).tofile(path)
    model = OurLLM(
        ModelConfig(
            vocab_size=16, block_size=4, n_embd=8, n_layer=1, n_head=2, dropout=0.0
        )
    )
    with torch.no_grad():
        for p in model.parameters():
            p.zero_()
    result = full_split_loss(model, path, 4, "cpu")
    assert result["scored_tokens"] == 9 and result["complete"]
    assert abs(result["loss"] - math.log(16)) < 1e-6
