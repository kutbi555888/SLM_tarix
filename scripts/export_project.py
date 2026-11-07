"""Kod, ma'lumot va modelning mavjud holatini ZIP nusxaga saqlaydi."""

from pathlib import Path
from datetime import datetime, timezone
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKIP = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    ".ruff_cache",
}


def export_project(output=None):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output = Path(output) if output else ROOT.parent / f"LLM_Model_UZ_{stamp}.zip"
    output = output.resolve()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if any(part in SKIP for part in relative.parts) or path.is_symlink():
                continue
            if (
                path.suffix in {".zip", ".pyc"}
                or path.name == "core"
                or path.name.startswith("core.")
            ):
                continue
            if path.name.startswith(".env") and path.name != ".env.example":
                continue
            if path.is_file() or path.is_dir() and not any(path.iterdir()):
                archive.write(path, Path(ROOT.name) / relative)
    with zipfile.ZipFile(output) as archive:
        broken = archive.testzip()
        if broken:
            raise ValueError(f"Arxiv tekshiruvidan o‘tmadi: {broken}")
    print(f"Arxiv saqlandi: {output}; hajmi {output.stat().st_size/1024**2:.2f} MiB")
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Loyihaning zaxira ZIP nusxasi")
    parser.add_argument("--output", help="ZIP uchun chiqish yo‘li")
    export_project(parser.parse_args().output)
