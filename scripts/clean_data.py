"""Boshlang‘ich matnlarni tozalaydi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_cleaner import DataCleaner

if __name__ == "__main__":
    DataCleaner().run("data/raw/tarix.jsonl", "data/cleaned/tarix.jsonl")
