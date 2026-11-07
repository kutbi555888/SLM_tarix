"""Sinovlar uchun bir xil tasodifiy holat va kichik CPU resursi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
import torch
from src.seed import set_seed


@pytest.fixture(autouse=True)
def bir_xil_boshlanish():
    torch.set_num_threads(2)
    set_seed(42)
