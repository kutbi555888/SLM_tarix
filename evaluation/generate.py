"""Boshlang'ich matndan davomini yaratadi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import torch
from inference.engine import InferenceEngine

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Matn yaratish")
    p.add_argument("--prompt", default="Amir Temur")
    p.add_argument("--checkpoint", default="checkpoints/model.pt")
    p.add_argument("--max-tokens", type=int, default=80)
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    torch.set_num_threads(2)
    text, n, ms = InferenceEngine(args.checkpoint).generate(
        args.prompt, args.max_tokens, args.temperature, seed=args.seed
    )
    print(text)
    print(f"Yangi tokenlar: {n}; kutish vaqti: {ms:.1f} ms")
