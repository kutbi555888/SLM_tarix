"""Model tuzilmasi, aniq parametrlar va eng kam vazn xotirasini ko'rsatadi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import json
from src.paths import project_path
from src.model_config import load_config
from src.model import OurLLM

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/run_01.yaml")
    args = p.parse_args()
    meta = project_path("dataset/meta.json")
    vocab = json.loads(meta.read_text())["vocab_size"] if meta.exists() else None
    cfg = load_config(args.config, vocab)
    model = OurLLM(cfg)
    print("Tuzilma:", cfg.to_dict())
    print("Aniq parametrlar:", model.num_parameters())
    print("Formula bo'yicha:", cfg.estimate_parameters())
    print(
        "Vazn, gradient, AdamW uchun eng kam MiB:",
        round(cfg.estimate_training_memory_mb(), 2),
    )
    print("Aktivatsiyalar va boshqa xotira bu hisobga qo'shilmagan.")
