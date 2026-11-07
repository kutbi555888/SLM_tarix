"""Tarix maqolalarini manba ma’lumotlari bilan yuklaydi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_downloader import DataDownloader

if __name__ == "__main__":
    DataDownloader().run()
