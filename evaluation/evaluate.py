"""Train namunasi, validation va yakuniy test xatoligini hisoblaydi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import json
import torch
from src.paths import project_path, file_hash
from src.jsonl_io import write_json
from src.checkpoint import read_checkpoint
from inference.engine import InferenceEngine
from evaluation.perplexity import (
    full_split_loss,
    perplexity,
    random_baseline_loss,
    bigram_baseline_loss,
)


def main():
    p = argparse.ArgumentParser(description="Modelni baholash")
    p.add_argument("--checkpoint", default="checkpoints/model.pt")
    p.add_argument("--output", default="evaluation/results.json")
    args = p.parse_args()
    torch.set_num_threads(2)
    meta = json.loads(project_path("dataset/meta.json").read_text(encoding="utf-8"))
    engine = InferenceEngine(args.checkpoint)
    saved = read_checkpoint(args.checkpoint)
    for split in ("train", "val", "test"):
        digest = file_hash(f"dataset/{split}.bin")
        if digest != meta[f"sha256_{split}"] or digest != saved["data_sha256"][split]:
            raise ValueError(f"{split}: baholash ma'lumoti checkpoint bilan mos emas.")
    metrics = {}
    for split in ("train", "val", "test"):
        metrics[split] = full_split_loss(
            engine.model,
            f"dataset/{split}.bin",
            engine.config.block_size,
            engine.device,
            meta["dtype"],
            max_blocks=128 if split == "train" else None,
        )
        metrics[split]["perplexity"] = perplexity(metrics[split]["loss"])
        print(split, metrics[split], flush=True)
    baseline = {
        "random": random_baseline_loss(meta["vocab_size"]),
        "bigram_val": bigram_baseline_loss(
            "dataset/train.bin", "dataset/val.bin", meta["vocab_size"], meta["dtype"]
        ),
    }
    prompts = ["Amir Temur", "Buxoro shahri", "Tarixni o'rganish"]
    samples = []
    for prompt in prompts:
        text, n, ms = engine.generate(prompt, max_tokens=60, seed=42)
        samples.append(
            {"prompt": prompt, "text": text, "tokens_generated": n, "latency_ms": ms}
        )
    report = {
        "model": "Tarixcha SLM",
        "parameters": engine.model.num_parameters(),
        "checkpoint_step": engine.step,
        "checkpoint_sha256": file_hash(args.checkpoint),
        "dataset": meta,
        "metrics": metrics,
        "baselines": baseline,
        "generation_samples": samples,
        "human_quality_review": "Hali sifat bo'yicha qo'lda baholanmagan.",
        "purpose": "O'quv tajribasi; fakt tekshiruvchi yoki tayyor suhbat yordamchisi emas.",
    }
    write_json(args.output, report)
    print("Hisobot saqlandi:", args.output)


if __name__ == "__main__":
    main()
