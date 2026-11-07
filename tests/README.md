# tests papkasi

python -m pytest tests -q bilan ishga tushadi. test_model.py model va o‘rganishni; test_data.py tokenizer/qismlar/chegaralarni; test_checkpoint.py to‘xtatib tiklashni; test_inference.py matn yaratish va API ni tekshiradi. conftest.py bir xil tasodifiy boshlanish va CPU oqimlarini sozlaydi. Haqiqiy model bo‘lmasa API testi o‘tkazib yuboriladi; topshirilgan arxivda barcha testlar model bilan bajarilgan.
