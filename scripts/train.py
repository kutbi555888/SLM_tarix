"""Modelni o'qitadi yoki last.pt holatidan davom ettiradi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import json
import torch
from src.paths import project_path, file_hash
from src.model_config import load_config
from src.train_config import load_train_config
from src.model import OurLLM
from src.seed import set_seed
from src.dataset_builder import DatasetBuilder
from src.trainer import Trainer


def main():
    p = argparse.ArgumentParser(description="Tarixcha SLM o'qitish")
    p.add_argument("--config", default="configs/run_01.yaml")
    p.add_argument("--resume", default=None, help="Davom ettiriladigan last.pt fayli")
    p.add_argument("--out-dir", default=None, help="Natijalar uchun alohida papka")
    p.add_argument(
        "--stop-after",
        type=int,
        default=None,
        help="Jadvalni o'zgartirmasdan shu qadamdan so'ng to'xtatish",
    )
    p.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = p.parse_args()
    meta = json.loads(project_path("dataset/meta.json").read_text(encoding="utf-8"))
    if meta["tokenizer_sha256"] != file_hash("tokenizer/tokenizer.json"):
        raise ValueError("Tokenizer va dataset mos emas.")
    for split in ("train", "val", "test"):
        if meta[f"sha256_{split}"] != file_hash(f"dataset/{split}.bin"):
            raise ValueError(f"{split}.bin o'zgargan.")
    mc = load_config(args.config, meta["vocab_size"])
    tc = load_train_config(args.config)
    if args.out_dir is not None:
        tc.out_dir = args.out_dir
    torch.set_num_threads(tc.num_threads)
    set_seed(tc.seed)
    device = (
        ("cuda" if torch.cuda.is_available() else "cpu")
        if args.device == "auto"
        else args.device
    )
    model = OurLLM(mc)
    print(
        f"Qurilma: {device}; parametrlar: {model.num_parameters():,}; bir qadam: {tc.tokens_per_step(mc.block_size):,} token",
        flush=True,
    )
    Trainer(model, DatasetBuilder(), mc, tc, meta, device).train(
        args.resume, args.stop_after
    )


if __name__ == "__main__":
    main()
