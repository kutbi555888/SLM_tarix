"""Matnni qaytarib tiklash mumkin bo'lgan bayt darajasidagi BPE tokenizer."""

from tokenizers import Tokenizer as HFTokenizer
from tokenizers import models, trainers, pre_tokenizers, decoders
from src.paths import project_path


class Tokenizer:
    def train(self, texts, vocab_size=4096, min_frequency=2):
        self.tokenizer = HFTokenizer(models.BPE())
        self.tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
        self.tokenizer.decoder = decoders.ByteLevel()
        trainer = trainers.BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=min_frequency,
            initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
            special_tokens=["<eos>"],
            show_progress=False,
        )
        self.tokenizer.train_from_iterator(texts, trainer)
        return self

    def save(self, path):
        p = project_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.tokenizer.save(str(p))

    def load(self, path):
        self.tokenizer = HFTokenizer.from_file(str(project_path(path)))
        return self

    def encode(self, text):
        return self.tokenizer.encode(text).ids

    def decode(self, ids):
        return self.tokenizer.decode(ids)

    def vocab_size(self):
        return self.tokenizer.get_vocab_size()

    def eos_id(self):
        return self.tokenizer.token_to_id("<eos>")
