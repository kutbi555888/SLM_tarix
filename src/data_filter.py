"""Uzunlik, harflar va takroriy qatorlar bo'yicha tekshirish; rad sababi yo'qolmaydi."""

from collections import Counter
import random
from src.jsonl_io import read_jsonl, write_jsonl, write_json


def alphabetic_ratio(text):
    return sum(c.isalpha() for c in text) / max(1, len(text))


def repeated_line_ratio(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    counts = Counter(lines)
    # Takrorlangan qatorlarning barcha nusxalari sanaladi.
    return sum(n for n in counts.values() if n > 1) / max(1, len(lines))


def inspect_document(doc, cfg):
    text = doc["text"]
    metrics = {
        "chars": len(text),
        "alpha_ratio": alphabetic_ratio(text),
        "repeated_line_ratio": repeated_line_ratio(text),
    }
    reasons = []
    if len(text) < cfg["min_chars"]:
        reasons.append("min_chars")
    if len(text) > cfg["max_chars"]:
        reasons.append("max_chars")
    if metrics["alpha_ratio"] < cfg["min_alpha_ratio"]:
        reasons.append("alpha_ratio")
    if metrics["repeated_line_ratio"] > cfg["max_repeated_line_ratio"]:
        reasons.append("repeated_lines")
    return {
        **doc,
        "metrics": metrics,
        "failed_rules": reasons,
        "status": "rejected" if reasons else "passed",
    }


def show_filter_examples(records, status, n=10, seed=42):
    """Har guruhdan mavjud bo'lgan ko'pi bilan n ta to'liq matnni chiqaradi."""
    if status not in {"passed", "rejected"} or n < 0:
        raise ValueError("status passed/rejected, n esa manfiy bo'lmagan son bo'lsin.")
    pool = [r for r in records if r["status"] == status]
    chosen = random.Random(seed).sample(pool, min(n, len(pool)))
    label = "O'TGAN" if status == "passed" else "RAD ETILGAN"
    print(f"{label}: jami {len(pool)}; ko'rsatilmoqda {len(chosen)}")
    if not pool:
        print("Bu guruhda hujjat yo'q.")
    for row in chosen:
        print("\n", row.get("title", row.get("id", "Hujjat")))
        print("Ko'rsatkichlar:", row["metrics"], "Rad sabablari:", row["failed_rules"])
        print(row["text"])
    return chosen


class DataFilter:
    def run(self, input_path, output_path, cfg, examples=0):
        audit = [inspect_document(doc, cfg) for doc in read_jsonl(input_path)]
        passed = [r for r in audit if r["status"] == "passed"]
        rejected = [r for r in audit if r["status"] == "rejected"]
        write_jsonl(output_path, passed)
        write_jsonl("data/filtered/rejected.jsonl", rejected)
        write_jsonl("data/filtered/audit.jsonl", audit)
        # Bitta hujjat umumiy hisobda faqat birinchi sababi bilan sanaladi.
        first_reasons = dict(Counter(r["failed_rules"][0] for r in rejected))
        stats = {
            "input": len(audit),
            "output": len(passed),
            "rejected": len(rejected),
            "first_reasons": first_reasons,
        }
        write_json("data/filtered/statistics.json", stats)
        print("Filtrlash:", stats)
        if examples:
            show_filter_examples(audit, "passed", examples)
            show_filter_examples(audit, "rejected", examples)
        return stats
