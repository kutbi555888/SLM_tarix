"""Hujjatlarni train.bin, val.bin va test.bin token fayllariga aylantiradi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from src.paths import read_yaml
from src.tokenizer import Tokenizer
from src.dataset_builder import DatasetBuilder

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Token fayllarini yaratish")
    p.add_argument("--config", default="configs/run_01.yaml")
    args = p.parse_args()
    cfg = read_yaml(args.config)
    DatasetBuilder(Tokenizer().load("tokenizer/tokenizer.json")).run(cfg["block_size"])
