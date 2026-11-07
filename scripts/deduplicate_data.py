"""Normallashtirilgan takrorlarni chiqarib tashlaydi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.deduplicator import Deduplicator

if __name__ == "__main__":
    Deduplicator().run("data/filtered/tarix.jsonl", "data/final/tarix.jsonl")
