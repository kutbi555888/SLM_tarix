"""BPE lug‘atini faqat train matnlaridan o‘rgatadi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from src.paths import read_yaml
from src.jsonl_io import read_jsonl
from src.tokenizer import Tokenizer

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Tokenizer o'qitish")
    p.add_argument("--config", default="configs/run_01.yaml")
    args = p.parse_args()
    cfg = read_yaml(args.config)
    rows = read_jsonl("data/final/train.jsonl")
    tok = Tokenizer().train((r["text"] for r in rows), vocab_size=cfg["vocab_size"])
    tok.save("tokenizer/tokenizer.json")
    print("Haqiqiy lug'at hajmi:", tok.vocab_size())
