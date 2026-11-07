> Bu davom ettirishdan OLDINGI tarixiy holat. Joriy natija: BAJARILGAN_VA_QOLGAN.md. Quyidagi yetishmagan fayllar keyin qo‘shildi.

# Davom ettirish oldidan saqlangan holat

Bu yakuniy loyiha emas. Oldingi ishlarning tekshirilgan zaxira nusxasi.

## Mavjud qismlar

O‘zbekcha izohli src/, scripts/, inference/, evaluation/ va deployment/ kodlari; sozlamalar; ma’lumotlar va tokenizer. Model o‘qitilishi, testlar, sahifa va hujjatlarni tugatish qolgan.

## Asl loyiha bilan solishtirganda hali mavjud bo‘lmagan fayllar

- `DATASET_CARD.md`
- `LESSON_10_GUIDE.md`
- `README.md`
- `PROJECT_CHARTER.md`
- `checkpoints/model.pt`
- `tests/test_model.py`
- `ui/index.html`
- `evaluation/results.json`

`checkpoints/train_log.jsonl`, `checkpoints/last.pt` ham o‘qitishdan keyin hosil bo‘ladi. `.git` Git tomonidan yaratiladi.

## Mavjud fayllar

- `.dockerignore` (119 bayt)
- `.env.example` (268 bayt)
- `.gitignore` (401 bayt)
- `checkpoints/.gitkeep` (0 bayt)
- `configs/data.yaml` (737 bayt)
- `configs/run_01.yaml` (1234 bayt)
- `configs/smoke.yaml` (465 bayt)
- `data/cleaned/.gitkeep` (0 bayt)
- `data/cleaned/statistics.json` (58 bayt)
- `data/cleaned/tarix.jsonl` (3363544 bayt)
- `data/filtered/.gitkeep` (0 bayt)
- `data/filtered/audit.jsonl` (3442925 bayt)
- `data/filtered/rejected.jsonl` (64107 bayt)
- `data/filtered/statistics.json` (125 bayt)
- `data/filtered/tarix.jsonl` (3378818 bayt)
- `data/final/.gitkeep` (0 bayt)
- `data/final/splits.json` (7582 bayt)
- `data/final/statistics.json` (162 bayt)
- `data/final/tarix.jsonl` (3423611 bayt)
- `data/final/test.jsonl` (110217 bayt)
- `data/final/train.jsonl` (3201215 bayt)
- `data/final/val.jsonl` (112179 bayt)
- `data/raw/.gitkeep` (0 bayt)
- `data/raw/tarix.jsonl` (3371966 bayt)
- `data/source_manifest.json` (1111 bayt)
- `dataset/.gitkeep` (0 bayt)
- `dataset/meta.json` (570 bayt)
- `dataset/test.bin` (52430 bayt)
- `dataset/train.bin` (1657396 bayt)
- `dataset/val.bin` (55036 bayt)
- `deployment/Dockerfile` (601 bayt)
- `deployment/__init__.py` (40 bayt)
- `deployment/app.py` (1902 bayt)
- `deployment/requirements.txt` (173 bayt)
- `evaluation/__init__.py` (66 bayt)
- `evaluation/evaluate.py` (2160 bayt)
- `evaluation/generate.py` (830 bayt)
- `evaluation/perplexity.py` (2158 bayt)
- `inference/__init__.py` (49 bayt)
- `inference/engine.py` (2481 bayt)
- `inference/sampling.py` (1315 bayt)
- `railway.json` (219 bayt)
- `requirements.txt` (261 bayt)
- `scripts/build_dataset.py` (610 bayt)
- `scripts/build_model.py` (950 bayt)
- `scripts/clean_data.py` (282 bayt)
- `scripts/deduplicate_data.py` (302 bayt)
- `scripts/design_model.py` (950 bayt)
- `scripts/download_data.py` (261 bayt)
- `scripts/filter_data.py` (628 bayt)
- `scripts/run_all.py` (1148 bayt)
- `scripts/split_data.py` (762 bayt)
- `scripts/train.py` (1816 bayt)
- `scripts/train_tokenizer.py` (707 bayt)
- `src/__init__.py` (57 bayt)
- `src/attention.py` (1137 bayt)
- `src/checkpoint.py` (1538 bayt)
- `src/data_cleaner.py` (1321 bayt)
- `src/data_downloader.py` (2896 bayt)
- `src/data_filter.py` (2850 bayt)
- `src/dataset_builder.py` (3084 bayt)
- `src/deduplicator.py` (1043 bayt)
- `src/jsonl_io.py` (1138 bayt)
- `src/lr_schedule.py` (458 bayt)
- `src/mlp.py` (569 bayt)
- `src/model.py` (2421 bayt)
- `src/model_config.py` (2102 bayt)
- `src/paths.py` (704 bayt)
- `src/seed.py` (277 bayt)
- `src/tokenizer.py` (1341 bayt)
- `src/train_config.py` (1658 bayt)
- `src/trainer.py` (7127 bayt)
- `src/transformer_block.py` (648 bayt)
- `tokenizer/.gitkeep` (0 bayt)
- `tokenizer/tokenizer.json` (263277 bayt)
- `ui/.gitignore` (48 bayt)
