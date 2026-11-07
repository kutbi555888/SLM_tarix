"""Matnning yozilishini tozalaydi, manba va litsenziya maydonlarini saqlaydi."""

import html
import re
import unicodedata
from src.jsonl_io import read_jsonl, write_jsonl, write_json


class DataCleaner:
    def clean_text(self, text):
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unicodedata.normalize("NFKC", text)
        # O'zbek apostrofining turli ko'rinishlarini bir xil shaklga keltiramiz.
        text = text.translate(str.maketrans({c: "'" for c in "‘’ʻʼ`"}))
        text = "".join(
            c
            for c in text
            if c in "\n\t" or not unicodedata.category(c).startswith("C")
        )
        text = re.sub(r"[ \t]+", " ", text)
        return re.sub(r"\n\s*\n+", "\n\n", text).strip()

    def run(self, input_path, output_path):
        source = read_jsonl(input_path)
        result = []
        for doc in source:
            text = self.clean_text(doc["text"])
            if text:
                result.append(
                    {
                        **doc,
                        "text": text,
                        "changes": "HTML va bo'shliqlar tozalandi; Unicode/apostrof birxillashtirildi.",
                    }
                )
        write_jsonl(output_path, result)
        stats = {
            "input": len(source),
            "empty_removed": len(source) - len(result),
            "output": len(result),
        }
        write_json("data/cleaned/statistics.json", stats)
        print("Tozalash:", stats)
        return stats
