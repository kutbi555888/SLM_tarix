"""Token tanlash va haqiqiy saqlangan modeldan foydalanish sinovlari."""

import pytest
import torch
from src.paths import project_path
from inference.sampling import sample_next_token


def test_eng_yuqori_token_tanlanadi():
    scores = torch.tensor([0.0, 1.0, 5.0, 2.0])
    assert sample_next_token(scores, [], temperature=0) == 2
    assert sample_next_token(scores, [], top_k=1) == 2
    assert sample_next_token(scores, [], top_p=0.01) == 2


def test_api_va_haqiqiy_model():
    if not project_path("checkpoints/model.pt").exists():
        pytest.skip("Asosiy model hali o'qitilmagan.")
    from fastapi.testclient import TestClient
    from deployment.app import app

    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "tayyor"
        page = client.get("/")
        assert page.status_code == 200 and "Tarixcha" in page.text
        params = {"prompt": "Amir Temur", "max_tokens": 5, "temperature": 0, "seed": 42}
        first = client.post("/generate", json=params)
        assert first.status_code == 200 and 1 <= first.json()["tokens_generated"] <= 5
        assert (
            client.post("/generate", json=params).json()["text"] == first.json()["text"]
        )
        assert (
            client.post("/generate", json={"prompt": "", "max_tokens": 5}).status_code
            == 422
        )
        assert client.post("/generate", json={"prompt": "   "}).status_code == 400
        assert (
            client.post(
                "/generate", json={"prompt": "Tarix", "max_tokens": 300}
            ).status_code
            == 422
        )
