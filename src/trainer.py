"""Paket olish, loss, gradient, optimizer, baholash va saqlashni birlashtiradi."""

import json
import time
from contextlib import nullcontext
from dataclasses import asdict
import torch
from src.paths import project_path
from src.checkpoint import (
    atomic_save,
    capture_rng,
    restore_rng,
    read_checkpoint,
    export_model,
)
from src.lr_schedule import get_lr


class Trainer:
    def __init__(
        self, model, dataset_builder, model_config, train_config, meta, device
    ):
        self.model = model.to(device)
        self.builder = dataset_builder
        self.mc = model_config
        self.cfg = train_config
        self.meta = meta
        self.device = torch.device(device)
        self.generator = torch.Generator().manual_seed(train_config.seed)
        self.optimizer = model.configure_optimizers(
            train_config.weight_decay,
            train_config.lr_max,
            (train_config.beta1, train_config.beta2),
        )
        requested = train_config.precision
        self.dtype = torch.float32
        if self.device.type == "cuda" and requested != "fp32":
            self.dtype = (
                torch.bfloat16
                if (
                    requested == "bf16"
                    or requested == "auto"
                    and torch.cuda.is_bf16_supported()
                )
                else torch.float16
            )
        self.scaler = torch.amp.GradScaler(
            "cuda", enabled=self.device.type == "cuda" and self.dtype == torch.float16
        )
        self.out = project_path(train_config.out_dir)
        self.out.mkdir(parents=True, exist_ok=True)

    def autocast(self):
        return (
            torch.autocast("cuda", dtype=self.dtype)
            if self.device.type == "cuda" and self.dtype != torch.float32
            else nullcontext()
        )

    def batch(self, split, generator):
        x, y = self.builder.get_batch(
            f"dataset/{split}.bin",
            self.cfg.batch_size,
            self.mc.block_size,
            generator,
            self.meta["dtype"],
        )
        return x.to(self.device), y.to(self.device)

    @torch.no_grad()
    def estimate_loss(self):
        was_training = self.model.training
        self.model.eval()
        result = {}
        # Har baholashda bir xil nazorat oynalari: o'sishlarni taqqoslash osonroq.
        for index, split in enumerate(("train", "val")):
            gen = torch.Generator().manual_seed(self.cfg.seed + 100 + index)
            total = 0.0
            for _ in range(self.cfg.eval_iters):
                x, y = self.batch(split, gen)
                with self.autocast():
                    _, loss = self.model(x, y)
                total += loss.item()
            result[split] = total / self.cfg.eval_iters
        self.model.train(was_training)
        return result

    def payload(self, step, best):
        return {
            "step": step,
            "best_val_loss": best,
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "model_config": self.mc.to_dict(),
            "train_config": asdict(self.cfg),
            "scaler_state": self.scaler.state_dict(),
            "rng": capture_rng(),
            "batch_rng": self.generator.get_state(),
            "tokenizer_sha256": self.meta["tokenizer_sha256"],
            "data_sha256": {
                s: self.meta[f"sha256_{s}"] for s in ("train", "val", "test")
            },
        }

    def resume(self, path):
        payload = read_checkpoint(path, self.device)
        if "optimizer_state" not in payload:
            raise ValueError("Davom ettirish uchun model.pt emas, last.pt kerak.")
        if payload["model_config"] != self.mc.to_dict():
            raise ValueError("Model tuzilmasi checkpoint bilan mos emas.")
        if payload["tokenizer_sha256"] != self.meta["tokenizer_sha256"]:
            raise ValueError("Tokenizer o'zgargan.")
        if payload["data_sha256"] != {
            s: self.meta[f"sha256_{s}"] for s in ("train", "val", "test")
        }:
            raise ValueError(
                "Dataset o'zgargan; eski o'qitishni davom ettirib bo'lmaydi."
            )
        for key in (
            "max_steps",
            "warmup_steps",
            "lr_max",
            "min_lr_ratio",
            "batch_size",
            "grad_accum_steps",
            "seed",
            "weight_decay",
            "beta1",
            "beta2",
            "grad_clip",
            "precision",
        ):
            if payload["train_config"][key] != getattr(self.cfg, key):
                raise ValueError(
                    f"Davom ettirishda {key} eski qiymatida bo'lishi kerak."
                )
        self.model.load_state_dict(payload["model_state"])
        self.optimizer.load_state_dict(payload["optimizer_state"])
        self.scaler.load_state_dict(payload["scaler_state"])
        self.generator.set_state(payload["batch_rng"].cpu())
        restore_rng(payload["rng"])
        return payload["step"], payload["best_val_loss"]

    def train(self, resume=None, stop_after=None):
        cfg = self.cfg
        if stop_after is not None and stop_after < 1:
            raise ValueError("To'xtash qadami musbat bo'lishi kerak.")
        log_path = self.out / "train_log.jsonl"
        start, best = self.resume(resume) if resume else (0, float("inf"))
        if not resume and (self.out / "last.pt").exists():
            raise FileExistsError(
                "Bu papkada o'qitilgan model bor. --resume bering yoki out_dir ni almashtiring."
            )

        def log(record):
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        if start == 0:
            initial = self.estimate_loss()
            log(
                {
                    "event": "boshlanish",
                    "step": 0,
                    "eval": initial,
                    "parameters": self.model.num_parameters(),
                }
            )
            print("Boshlang'ich loss:", initial, flush=True)
        self.model.train()
        end = (
            min(cfg.max_steps, stop_after) if stop_after is not None else cfg.max_steps
        )
        t0 = time.perf_counter()
        since_log = 0
        for index in range(start, end):
            lr = get_lr(index, cfg)
            for group in self.optimizer.param_groups:
                group["lr"] = lr
            self.optimizer.zero_grad(set_to_none=True)
            total_loss = 0.0
            for _ in range(cfg.grad_accum_steps):
                x, y = self.batch("train", self.generator)
                with self.autocast():
                    _, loss = self.model(x, y)
                if not torch.isfinite(loss):
                    raise FloatingPointError(
                        "Loss chekli son emas; o'qitish to'xtatildi."
                    )
                self.scaler.scale(loss / cfg.grad_accum_steps).backward()
                total_loss += loss.item() / cfg.grad_accum_steps
            self.scaler.unscale_(self.optimizer)
            norm = torch.nn.utils.clip_grad_norm_(
                self.model.parameters(), cfg.grad_clip, error_if_nonfinite=True
            )
            self.scaler.step(self.optimizer)
            self.scaler.update()
            step = index + 1
            since_log += 1
            if step % cfg.log_interval == 0 or step == end:
                speed = (
                    since_log
                    * cfg.tokens_per_step(self.mc.block_size)
                    / max(1e-9, time.perf_counter() - t0)
                )
                log(
                    {
                        "event": "oqitish",
                        "step": step,
                        "loss": total_loss,
                        "lr": lr,
                        "grad_norm": float(norm),
                        "tokens_per_sec": speed,
                    }
                )
                print(
                    f"Qadam {step}/{cfg.max_steps} | loss {total_loss:.4f} | token/soniya {speed:.0f}",
                    flush=True,
                )
                t0 = time.perf_counter()
                since_log = 0
            if step % cfg.eval_interval == 0 or step == end:
                metrics = self.estimate_loss()
                log({"event": "baholash", "step": step, "eval": metrics})
                print("Nazorat:", metrics, flush=True)
                if metrics["val"] < best:
                    best = metrics["val"]
                    payload = self.payload(step, best)
                    atomic_save(payload, self.out / "best.pt")
                    export_model(payload, self.out / "model.pt")
            if step % cfg.checkpoint_interval == 0 or step == end:
                atomic_save(self.payload(step, best), self.out / "last.pt")
        print(
            f"Saqlangan joy: {self.out}; eng yaxshi nazorat loss: {best:.4f}",
            flush=True,
        )
        return best
