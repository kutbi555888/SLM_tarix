"""JSONL faylda har bir qator bitta hujjatni saqlaydi."""

import json
from src.paths import project_path


def read_jsonl(path, limit=None):
    rows = []
    with project_path(path).open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            if not isinstance(item, dict) or not isinstance(item.get("text"), str):
                raise ValueError(
                    f"{path}, {line_number}-qator: text matn bo'lishi kerak."
                )
            rows.append(item)
            if limit is not None and len(rows) >= limit:
                break
    return rows


def write_jsonl(path, records):
    path = project_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_json(path, value):
    path = project_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
