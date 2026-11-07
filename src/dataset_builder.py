"""Hujjatni avval bo'ladi; keyin tokenlarni binar fayllarga yozadi."""

import json
import random
import numpy as np
import torch
from src.paths import project_path, file_hash
from src.jsonl_io import read_jsonl, write_jsonl, write_json


def split_documents(documents, val_ratio=0.05, test_ratio=0.05, seed=42):
    if len(documents) < 20 or not (0 < val_ratio + test_ratio < 0.5):
        raise ValueError("Kamida 20 hujjat va to'g'ri ajratish ulushlari kerak.")
    if val_ratio <= 0 or test_ratio <= 0:
        raise ValueError("Validation va test ulushlari musbat bo'lishi kerak.")
    rows = list(documents)
    random.Random(seed).shuffle(rows)
    nv, nt = max(1, int(len(rows) * val_ratio)), max(1, int(len(rows) * test_ratio))
    return {"val": rows[:nv], "test": rows[nv : nv + nt], "train": rows[nv + nt :]}


class DatasetBuilder:
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer
        self.arrays = {}

    def encode_to_bin(self, documents, output_path, dtype):
        path = project_path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with path.open("wb") as f:
            for row in documents:
                ids = self.tokenizer.encode(row["text"]) + [self.tokenizer.eos_id()]
                np.asarray(ids, dtype=dtype).tofile(f)
                count += len(ids)
        return count

    def run(self, block_size=128):
        vocab = self.tokenizer.vocab_size()
        dtype = "uint16" if vocab <= 65536 else "uint32"
        meta = {
            "vocab_size": vocab,
            "dtype": dtype,
            "eos_id": self.tokenizer.eos_id(),
            "block_size": block_size,
            "tokenizer_sha256": file_hash("tokenizer/tokenizer.json"),
        }
        for split in ("train", "val", "test"):
            rows = read_jsonl(f"data/final/{split}.jsonl")
            count = self.encode_to_bin(rows, f"dataset/{split}.bin", dtype)
            if count <= block_size:
                raise ValueError(
                    f"{split}: {count} token juda kam; ko'proq hujjat oling."
                )
            meta[f"n_docs_{split}"] = len(rows)
            meta[f"n_tokens_{split}"] = count
            meta[f"sha256_{split}"] = file_hash(f"dataset/{split}.bin")
        write_json("dataset/meta.json", meta)
        print("Dataset tayyor:", meta)
        return meta

    def get_batch(self, bin_path, batch_size, block_size, generator, dtype="uint16"):
        key = (str(project_path(bin_path)), dtype)
        if key not in self.arrays:
            self.arrays[key] = np.memmap(key[0], dtype=dtype, mode="r")
        data = self.arrays[key]
        if len(data) <= block_size:
            raise ValueError(
                "Token fayli kontekst uzunligidan kamida bitta token uzun bo'lsin."
            )
        # Oxirgi y tokeni ham mavjud bo'lgan barcha boshlanishlar ruxsat etiladi.
        starts = torch.randint(
            len(data) - block_size, (batch_size,), generator=generator
        ).tolist()
        x = np.stack([data[i : i + block_size].astype(np.int64) for i in starts])
        y = np.stack(
            [data[i + 1 : i + block_size + 1].astype(np.int64) for i in starts]
        )
        return torch.from_numpy(x), torch.from_numpy(y)
