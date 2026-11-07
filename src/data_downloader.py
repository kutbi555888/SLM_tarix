"""Hugging Face'dan o'zbekcha tarix matnlari va ularning manbalarini oladi."""

from datetime import datetime, timezone
import unicodedata
from datasets import load_dataset
from src.paths import read_yaml
from src.jsonl_io import write_jsonl, write_json


def latin_ratio(text):
    """Harflarning qancha qismi lotin yozuvida ekanini hisoblaydi."""
    letters = [c for c in text if c.isalpha()]
    return sum("LATIN" in unicodedata.name(c, "") for c in letters) / max(
        1, len(letters)
    )


def is_history(item, cfg):
    """Sarlavha yoki kirish qismidagi tarixga oid so'zlar bilan tanlaydi."""
    title = item.get("title", "").casefold()
    body = item.get("text", "")[:2000].casefold()
    title_match = any(word in title for word in cfg["title_keywords"])
    body_matches = sum(word in body for word in cfg["body_keywords"])
    return title_match or body_matches >= cfg["min_body_matches"]


class DataDownloader:
    def run(self, output_path="data/raw/tarix.jsonl", config_path="configs/data.yaml"):
        cfg = read_yaml(config_path)
        source = load_dataset(
            cfg["dataset_name"],
            name=cfg["dataset_config"],
            revision=cfg["revision"],
            split=cfg["split"],
            streaming=True,
        )
        records = []
        scanned = 0
        for item in source:
            scanned += 1
            text = item.get("text")
            if (
                isinstance(text, str)
                and is_history(item, cfg)
                and latin_ratio(text[:4000]) >= cfg["min_latin_ratio"]
            ):
                records.append(
                    {
                        "id": str(item["id"]),
                        "title": item["title"],
                        "url": item["url"],
                        "text": text,
                        "source": cfg["dataset_name"],
                        "revision": cfg["revision"],
                        "snapshot": cfg["dataset_config"],
                        "license": "CC-BY-SA-3.0",
                        "attribution": "O'zbekcha Wikipedia ishtirokchilari; mualliflar maqola tarixida",
                        "history_url": item["url"] + "?action=history",
                    }
                )
            if scanned % 2000 == 0:
                print(
                    f"Ko'rilgan: {scanned}; tarix uchun tanlangan: {len(records)}",
                    flush=True,
                )
            if len(records) >= cfg["max_documents"] or scanned >= cfg["max_scanned"]:
                break
        if len(records) < 30:
            raise ValueError(
                "Kamida 30 maqola kerak. max_scanned yoki mavzu so'zlarini tekshiring."
            )
        write_jsonl(output_path, records)
        report = {
            "source": cfg,
            "scanned": scanned,
            "selected": len(records),
            "characters": sum(len(r["text"]) for r in records),
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            "note": "Mavzu so'zlari bilan tanlangan; qo'lda to'liq tekshirilmagan.",
        }
        write_json("data/source_manifest.json", report)
        print(
            f"Yuklandi: {len(records)} ta maqola; manba va litsenziya har bir yozuvda saqlandi."
        )
        return report
