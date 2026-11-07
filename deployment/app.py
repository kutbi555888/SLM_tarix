"""Bitta serverdan o'zbekcha sahifa va model API sini taqdim etadi."""

import os
from contextlib import asynccontextmanager
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from inference.engine import InferenceEngine
from src.paths import project_path


@asynccontextmanager
async def lifespan(app):
    torch.set_num_threads(int(os.getenv("SLM_THREADS", "2")))
    app.state.engine = InferenceEngine(
        os.getenv("CHECKPOINT_PATH", "checkpoints/model.pt"),
        os.getenv("TOKENIZER_PATH", "tokenizer/tokenizer.json"),
    )
    yield
    app.state.engine = None


app = FastAPI(
    title="Tarixcha SLM",
    description="O'zbekcha tarix matnini davom ettiruvchi o'quv modeli",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def qiymat_xatosi(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Kiritilgan qiymatlar noto'g'ri. Matn va sozlamalar chegaralarini tekshiring.",
            "fields": [str(e["loc"][-1]) for e in exc.errors()],
        },
    )


class GenerateRequest(BaseModel):
    prompt: str = Field(
        min_length=1, max_length=4000, description="Davom ettiriladigan matn"
    )
    max_tokens: int = Field(default=80, ge=1, le=256)
    temperature: float = Field(default=0.8, ge=0, le=2)
    top_k: int = Field(default=40, ge=0, le=65536)
    top_p: float = Field(default=0.95, gt=0, le=1)
    repetition_penalty: float = Field(default=1.1, ge=1, le=2)
    seed: int = Field(default=42, ge=0, le=2147483647)


@app.get("/")
def home():
    return FileResponse(project_path("ui/index.html"))


@app.get("/health")
def health():
    engine = getattr(app.state, "engine", None)
    return {
        "status": "tayyor" if engine else "yuklanmoqda",
        "model": "Tarixcha SLM",
        "parameters": engine.model.num_parameters() if engine else None,
    }


@app.post("/generate")
def generate(request: GenerateRequest):
    engine = getattr(app.state, "engine", None)
    if engine is None:
        raise HTTPException(503, "Model hali tayyor emas.")
    try:
        text, n, ms = engine.generate(**request.model_dump())
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"text": text, "tokens_generated": n, "latency_ms": round(ms, 2)}
