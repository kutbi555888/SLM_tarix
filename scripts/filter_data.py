"""Filtrdan o‘tgan va rad etilgan matnlarni ajratadi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from src.paths import read_yaml
from src.data_filter import DataFilter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Matnlarni filtrlash va qo'lda tekshirish"
    )
    parser.add_argument(
        "--examples",
        type=int,
        default=0,
        help="Har guruhdan chiqariladigan matnlar soni",
    )
    args = parser.parse_args()
    DataFilter().run(
        "data/cleaned/tarix.jsonl",
        "data/filtered/tarix.jsonl",
        read_yaml("configs/data.yaml"),
        args.examples,
    )
