"""Yo'llarni loyiha joylashgan papkadan hisoblaydi."""

from pathlib import Path
import hashlib
import yaml

ROOT = Path(__file__).resolve().parents[1]


def project_path(path):
    """Nisbiy yo'lni loyiha ildiziga bog'laydi; mutlaq yo'l o'zgarmaydi."""
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def read_yaml(path):
    with project_path(path).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def file_hash(path):
    """SHA-256: fayl o'zgarganini aniqlash uchun nazorat qiymati."""
    h = hashlib.sha256()
    with project_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
