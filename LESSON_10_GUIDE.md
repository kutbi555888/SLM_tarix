# Loyihani bosqichma-bosqich ishlatish

Avval `README.md`dagi o‘rnatishni bajaring. Barcha buyruqlar loyiha ildizidagi terminalda ishlatiladi. Tayyor ZIPda ma’lumot, tokenizer va binar fayllar bor; ularni qayta yaratish shart emas. Quyidagi ketma-ketlik jarayonni o‘rganish yoki yangi ma’lumotga o‘tish uchun berilgan.

## 1. Manbani olish

```bash
python scripts/download_data.py
```

`configs/data.yaml` manba, til, aniq nusxa va mavzu so‘zlarini belgilaydi. Dastur `data/raw/tarix.jsonl`ga matn va manbasini yozadi. `data/source_manifest.json` ko‘rilgan/tanlangan hujjatlar sonini qayd qiladi. Ommaviy manba uchun maxfiy token majburiy emas. Internet cheklangan muhitda ZIPdagi tayyor ma’lumot bilan davom eting.

## 2. Tozalash

```bash
python scripts/clean_data.py
```

HTML, ortiqcha bo‘shliq va apostrof shakllari tartibga keltiriladi. Asl manba metama’lumotlari yo‘qolmaydi. Natija `data/cleaned/tarix.jsonl`ga yoziladi. Tozalash tarjima yoki faktni tuzatish emas.

## 3. Filtrlash va misollarni o‘qish

```bash
python scripts/filter_data.py --examples 10
```

Dastur filtrdan o‘tgan 10 ta va rad etilgan 10 ta matnni, ko‘rsatkichlari hamda sabablarini chiqaradi. Guruhda 10 tadan kam bo‘lsa, mavjudlarini ko‘rsatadi. `audit.jsonl`dagi to‘liq matnlar orqali tekshirish mumkin.

| Rad sababi | Mazmuni | Qo‘lda nima tekshiriladi? |
|---|---|---|
| `min_chars` | Matn juda qisqa | Qisqa bo‘lsa ham foydali maqolami? |
| `max_chars` | Matn juda uzun | Foydali matnni bo‘laklash ma’qulmi? |
| `alpha_ratio` | Harflar ulushi kam | Sana yoki jadval sabab foydali matn rad etildimi? |
| `repeated_lines` | Bir xil qatorlar ko‘p | Mazmunli ro‘yxatmi yoki keraksiz takrormi? |

Faqat statistikadan «filtr xato» deb bo‘lmaydi. Kerakli matnni rad etsa, bu noto‘g‘ri rad etish; sifatsiz matnni o‘tkazsa, bu noto‘g‘ri qabul qilish. O‘qilgan misol va sababni yozib, shundan keyin chegarani o‘zgartiring. Notebookdagi funksiya uchun `from src.data_filter import show_filter_examples` importi kerak.

## 4. Takrorlarni kamaytirish va ajratish

```bash
python scripts/deduplicate_data.py
python scripts/split_data.py
```

Birinchi buyruq bir xil matn nusxalarini tekshiradi. Ikkinchisi butun hujjatlarni `train.jsonl`, `val.jsonl`, `test.jsonl`ga ajratadi. `splits.json`da hujjat raqamlari yoziladi. Tokenizerni bundan oldin barcha hujjatlarga o‘rgatish nazorat ma’lumoti aralashishiga olib kelishi mumkin.

## 5. Tokenizer va token fayllari

```bash
python scripts/train_tokenizer.py --config configs/run_01.yaml
python scripts/build_dataset.py --config configs/run_01.yaml
```

Tokenizer faqat `train` matnidan lug‘at o‘rganadi. Keyin barcha qismlar shu tokenizer bilan raqamlarga aylantiriladi. `dataset/meta.json` lug‘at hajmi, tokenlar soni va fayllarning SHA-256 nazorat qiymatlarini saqlaydi. Yangi tokenizer yoki yangi binar fayl eski checkpointga mos kelmasa, dastur xato bilan to‘xtaydi. Bunday vaziyatda yangi o‘qitishni alohida natijalar papkasida boshlang.

## 6. Modelni tekshirish

```bash
python scripts/design_model.py
python scripts/build_model.py
python -m pytest tests/test_model.py tests/test_data.py tests/test_checkpoint.py -q
```

Model kodi noldan vazn yaratadi. `build_model.py` parametrlar sonini formula va haqiqiy model orqali hisoblaydi. Bu model o‘qitildi degani emas. Xotira hisobida faqat vazn, gradient va AdamW holatlari bor; aktivatsiyalar va PyTorchning boshqa xarajatlari qo‘shimcha.

## 7. Tezkor sinov

```bash
python scripts/train.py --config configs/smoke.yaml --out-dir checkpoints/tezkor_yangi
python evaluation/generate.py --checkpoint checkpoints/tezkor_yangi/model.pt --prompt "Buxoro"
```

Bu atigi 12 qadamlik kichik sinov; maqsad kod zanjirini tekshirish. Undan sifatli matn kutilmaydi. Asosiy tokenizer va `.bin` fayllar bilan ishlaydi, kontekst 64 token bo‘ladi.

## 8. Asosiy o‘qitish va tiklash

```bash
python scripts/train.py --config configs/run_01.yaml --out-dir checkpoints/mening_tajribam
```

Kiritilgan tokenlar `x`, bir token surilgan keyingi tokenlar `y` bo‘ladi. Model sonli baho beradi; loss hisoblanadi; gradient olinadi; AdamW vaznlarni yangilaydi. Belgilangan vaqtda nazorat xatosi hisoblanadi va holat saqlanadi.

- `model.pt` — nazorat xatosi eng kichik bo‘lgan modelning ixcham vaznlari.
- `best.pt` — o‘sha qadamning to‘liq o‘qitish holati.
- `last.pt` — oxirgi saqlangan qadamning to‘liq holati.
- `train_log.jsonl` — qadam, loss, o‘rganish tezligi, gradient va tezlik jurnali.

Tiklash:

```bash
python scripts/train.py --config configs/run_01.yaml --out-dir checkpoints/mening_tajribam --resume checkpoints/mening_tajribam/last.pt
```

`model.pt` optimizer holatiga ega emas; undan shu usulda o‘qitishni davom ettirib bo‘lmaydi. `max_steps`, o‘rganish tezligi va paket sozlamalarini tiklash o‘rtasida almashtirmang. Qo‘shimcha yangi tajriba uchun alohida sozlama va natijalar papkasi ishlating. Bu loyihada oldingi vaznlardan yangi jadval bilan qo‘shimcha moslashtirish uchun maxsus buyruq hali yo‘q.

## 9. Yakuniy baholash

```bash
python evaluation/evaluate.py --checkpoint checkpoints/mening_tajribam/model.pt --output evaluation/mening_natijam.json
```

Hisobot loss, perplexity, sodda taqqoslash usullari va yaratilgan matnlarni saqlaydi. Nazorat va testdagi har bir nishon token bir marta baholanadi; kontekst har blok boshida yangilanadi. Train bahosi faqat birinchi 128 blokning namunasi. Turli baholash usullarining sonlarini to‘g‘ridan-to‘g‘ri solishtirmang. Test natijasiga qarab sozlamalarni qayta-qayta tanlashdan saqlaning: yangi tajribada asosiy tanlov uchun `val` ishlatiladi.

## 10. Matn yaratish va server

```bash
python evaluation/generate.py --prompt "Tarixni o'rganish" --temperature 0.8 --max-tokens 80
python -m uvicorn deployment.app:app --host 127.0.0.1 --port 8000
```

Server `/health` orqali holatni, `/generate` orqali matn yaratishni taqdim etadi; `/` o‘zbekcha sahifani ochadi. UI sahifasi shu serverdan foydalanadi. Kod har bir so‘rovga modelni qayta yuklamaydi. Uzun matnning oxirgi 128 tokeni kontekst sifatida olinadi.

Docker ishlatish uchun loyiha ildizida:

```bash
docker build -f deployment/Dockerfile -t tarixcha-slm .
docker run --rm -p 8000:8000 tarixcha-slm
```

Docker build bajarishdan oldin `checkpoints/model.pt`, `tokenizer/tokenizer.json` va `ui/index.html` mavjud bo‘lsin. Docker va Railway joylash bu topshirishda avtomatik tasdiqlangan sinov hisoblanmaydi; tekshirish holati `BAJARILGAN_VA_QOLGAN.md`da berilgan.

## Ko‘p uchraydigan xatolar

| Xato | Amal |
|---|---|
| `ModuleNotFoundError` | Buyruq kerakli virtual muhit Python’i bilan bajarilganini va requirements o‘rnatilganini tekshiring |
| `show_filter_examples is not defined` | Funksiyani import qiling va import yozilgan katakni bajaring |
| `Tokenizer ... mos emas` | Bir tajribaning tokenizer, binar fayl va checkpointlarini birga ishlating |
| `Bu papkada o‘qitilgan model bor` | `--resume` yoki yangi `--out-dir` tanlang |
| `model.pt` topilmadi | Avval o‘qiting yoki to‘g‘ri `--checkpoint` yo‘lini bering |
| Xotira yetishmaydi | Yangi tajribada `batch_size`, so‘ng zarur bo‘lsa `block_size`ni kamaytiring |
| Server bilan aloqa yo‘q | Uvicorn ishlayotganini va sahifa server URLidan ochilganini tekshiring |
| Matn mazmunsiz | O‘qitish xatosi bilan mazmun sifatini ajrating; bu juda kichik tajriba modeli |

## Ishni yo‘qotmasdan davom ettirish

`python scripts/export_project.py` bilan yangi ZIP oling. Muhim o‘zgarishlardan oldin eski ZIPni saqlang. Git kod tarixini saqlaydi, lekin `.gitignore`dagi ma’lumot va checkpointlarni o‘zi saqlamaydi. ZIPni ulashishdan oldin unda shaxsiy ma’lumot yoki maxfiy kalit yo‘qligini tekshiring.
