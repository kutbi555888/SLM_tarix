"""Saqlangan dataset, tokenizer, checkpoint va asosiy fayllarni solishtiradi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import numpy as np
from src.paths import project_path, file_hash
from src.jsonl_io import read_jsonl, write_json
from src.checkpoint import read_checkpoint


def verify():
    meta = json.loads(project_path("dataset/meta.json").read_text(encoding="utf-8"))
    checkpoint = read_checkpoint("checkpoints/model.pt")
    checks = {}
    checks["tokenizer_mos"] = (
        file_hash("tokenizer/tokenizer.json")
        == meta["tokenizer_sha256"]
        == checkpoint["tokenizer_sha256"]
    )
    rows = {s: read_jsonl(f"data/final/{s}.jsonl") for s in ("train", "val", "test")}
    ids = {s: {r["id"] for r in docs} for s, docs in rows.items()}
    hashes = {s: {r["text_hash"] for r in docs} for s, docs in rows.items()}
    pairs = [("train", "val"), ("train", "test"), ("val", "test")]
    checks["hujjatlar_aralashmagan"] = all(not (ids[a] & ids[b]) for a, b in pairs)
    checks["aynan_bir_xil_matn_aralashmagan"] = all(
        not (hashes[a] & hashes[b]) for a, b in pairs
    )
    for split in rows:
        path = f"dataset/{split}.bin"
        checks[f"{split}_hash_mos"] = (
            file_hash(path)
            == meta[f"sha256_{split}"]
            == checkpoint["data_sha256"][split]
        )
        array = np.memmap(project_path(path), dtype=meta["dtype"], mode="r")
        checks[f"{split}_token_soni_mos"] = len(array) == meta[f"n_tokens_{split}"]
        checks[f"{split}_tokenlar_lugatda"] = bool(array.max() < meta["vocab_size"])
        checks[f"{split}_hujjat_soni_mos"] = len(rows[split]) == meta[f"n_docs_{split}"]
    reference = project_path("SOURCE_REFERENCE.json")
    if reference.exists():
        expected = json.loads(reference.read_text(encoding="utf-8"))["original_files"]
        for name in expected:
            checks[f"fayl:{name}"] = project_path(name).is_file()
    for name in ["checkpoints/train_log.jsonl", "checkpoints/last.pt", "ui/index.html"]:
        checks[f"fayl:{name}"] = project_path(name).is_file()
    report = {
        "ok": all(checks.values()),
        "checks": checks,
        "checkpoint_step": checkpoint["step"],
    }
    write_json("evaluation/verification.json", report)
    print(
        f"Tekshiruvlar: {sum(checks.values())}/{len(checks)}; natija: "
        + ("MUVAFFAQIYATLI" if report["ok"] else "XATO")
    )
    if not report["ok"]:
        raise ValueError(
            "Muvaffaqiyatsiz tekshiruvlar: "
            + ", ".join(k for k, v in checks.items() if not v)
        )
    return report


if __name__ == "__main__":
    verify()
