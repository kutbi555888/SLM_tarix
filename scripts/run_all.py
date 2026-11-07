"""Bosqichlarni bitta buyruq bilan ketma-ket bajaradi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import subprocess
from src.paths import ROOT

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Ma'lumotdan tayyor modelgacha")
    p.add_argument("--config", default="configs/run_01.yaml")
    p.add_argument("--out-dir", default=None, help="Yangi o'qitish natijalari papkasi")
    p.add_argument(
        "--skip-download",
        action="store_true",
        help="Arxivdagi boshlang'ich ma'lumotlardan foydalanish",
    )
    p.add_argument(
        "--prepare-only",
        action="store_true",
        help="O'qitmasdan token fayllarigacha tayyorlash",
    )
    args = p.parse_args()
    jobs = [] if args.skip_download else [["scripts/download_data.py"]]
    jobs += [
        [f"scripts/{name}.py"]
        for name in ("clean_data", "filter_data", "deduplicate_data", "split_data")
    ]
    jobs += [
        ["scripts/train_tokenizer.py", "--config", args.config],
        ["scripts/build_dataset.py", "--config", args.config],
    ]
    if not args.prepare_only:
        job = ["scripts/train.py", "--config", args.config]
        if args.out_dir is not None:
            job += ["--out-dir", args.out_dir]
        jobs.append(job)
    for job in jobs:
        print("Bosqich:", " ".join(job), flush=True)
        subprocess.run([sys.executable, *job], cwd=ROOT, check=True)
