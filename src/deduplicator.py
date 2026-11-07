"""Bir xil matnlar train va nazorat to'plamlariga tarqalib ketishini kamaytiradi."""

import hashlib
import re
from src.jsonl_io import read_jsonl, write_jsonl, write_json


def document_hash(text):
    normalized = re.sub(r"\s+", " ", text).strip().casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class Deduplicator:
    def run(self, input_path, output_path):
        source = read_jsonl(input_path)
        seen, unique = set(), []
        for row in source:
            key = document_hash(row["text"])
            if key in seen:
                continue
            seen.add(key)
            unique.append({**row, "text_hash": key})
        write_jsonl(output_path, unique)
        stats = {
            "input": len(source),
            "duplicates": len(source) - len(unique),
            "output": len(unique),
            "method": "Bo'shliqlar va harf kattaligi birxillashtirilgan SHA-256; yaqin dublikatlar tekshirilmagan.",
        }
        write_json("data/final/statistics.json", stats)
        print("Takrorlarni olib tashlash:", stats)
        return stats
