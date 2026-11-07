"""Tokenizer o‘rganishidan oldin hujjatlarni train, val va testga ajratadi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.paths import read_yaml
from src.jsonl_io import read_jsonl, write_jsonl, write_json
from src.dataset_builder import split_documents

if __name__ == "__main__":
    cfg = read_yaml("configs/data.yaml")
    splits = split_documents(
        read_jsonl("data/final/tarix.jsonl"),
        cfg["val_ratio"],
        cfg["test_ratio"],
        cfg["seed"],
    )
    for name, rows in splits.items():
        write_jsonl(f"data/final/{name}.jsonl", rows)
    write_json(
        "data/final/splits.json", {k: [r["id"] for r in v] for k, v in splits.items()}
    )
    print("Hujjatlar bo'lindi:", {k: len(v) for k, v in splits.items()})
