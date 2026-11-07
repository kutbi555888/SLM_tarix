"""Model va tokenizer bir marta yuklanadi; so'rovlar shu nusxadan foydalanadi."""

import time
import threading
import torch
from src.paths import project_path, file_hash
from src.model import OurLLM
from src.model_config import ModelConfig
from src.tokenizer import Tokenizer
from src.checkpoint import read_checkpoint
from inference.sampling import sample_next_token


class InferenceEngine:
    def __init__(
        self,
        checkpoint_path="checkpoints/model.pt",
        tokenizer_path="tokenizer/tokenizer.json",
        device="cpu",
    ):
        self.device = torch.device(device)
        payload = read_checkpoint(checkpoint_path, self.device)
        if file_hash(tokenizer_path) != payload["tokenizer_sha256"]:
            raise ValueError(
                "Tokenizer checkpoint yaratilgan tokenizer bilan mos emas."
            )
        self.config = ModelConfig(**payload["model_config"])
        self.model = OurLLM(self.config).to(self.device)
        self.model.load_state_dict(payload["model_state"])
        self.model.eval()
        self.tokenizer = Tokenizer().load(tokenizer_path)
        self.eos_id = self.tokenizer.eos_id()
        self.step = payload["step"]
        self.lock = threading.Lock()

    @torch.inference_mode()
    def generate(
        self,
        prompt,
        max_tokens=80,
        temperature=0.8,
        top_k=40,
        top_p=0.95,
        repetition_penalty=1.1,
        seed=42,
    ):
        if not prompt.strip():
            raise ValueError("Boshlang'ich matn bo'sh bo'lmasin.")
        if not 1 <= max_tokens <= 256:
            raise ValueError("max_tokens 1–256 oralig'ida bo'lsin.")
        ids = self.tokenizer.encode(prompt)
        if not ids:
            raise ValueError("Matndan token hosil bo'lmadi.")
        generated = list(ids)
        rng = torch.Generator(device=self.device).manual_seed(seed)
        start = time.perf_counter()
        with self.lock:
            for _ in range(max_tokens):
                x = torch.tensor(
                    [generated[-self.config.block_size :]], device=self.device
                )
                logits, _ = self.model(x)
                token = sample_next_token(
                    logits[0, -1],
                    generated,
                    temperature,
                    top_k,
                    top_p,
                    repetition_penalty,
                    rng,
                )
                generated.append(token)
                if token == self.eos_id:
                    break
        return (
            self.tokenizer.decode(generated),
            len(generated) - len(ids),
            (time.perf_counter() - start) * 1000,
        )


def resolve_checkpoint(explicit=None):
    path = project_path(explicit or "checkpoints/model.pt")
    if not path.exists():
        raise FileNotFoundError("Model yo'q. Avval scripts/train.py ni bajaring.")
    return path


def default_engine():
    return InferenceEngine(resolve_checkpoint())
