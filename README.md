# Tarixcha SLM

**O‘zbekcha tarix matnlarini davom ettirish uchun kichik til modeli va uni noldan o‘qitishni o‘rganish loyihasi.** SLM — *Small Language Model*, ya’ni kichik til modeli. Bu yerda ma’lumotni olishdan boshlab modelni saqlash va mahalliy sahifada ishlatishgacha bo‘lgan bosqichlar alohida fayllarga ajratilgan.

Loyiha [davronbek-malikov/LLM_Model](https://github.com/davronbek-malikov/LLM_Model) tuzilmasi asosida moslashtirilgan. Mavjud kodlar saqlanib, kerakli joylari tuzatildi; sharhlar, xabarlar va qo‘llanmalar o‘zbekcha yozildi. Python kalit so‘zlari, kutubxona nomlari hamda mavjud fayl/API nomlari texnik moslik uchun asl ko‘rinishida qoldi.

## Avval nimani bilish kerak?

- Model matnning **keyingi tokenini** bashorat qiladi. Token — butun so‘z yoki uning bir bo‘lagi bo‘lishi mumkin.
- Bu savol-javobga maxsus o‘rgatilgan yordamchi emas. `Amir Temur` kabi jumla boshini yozib, davomini yaratish uchun ishlatiladi.
- Ma’lumot kichik, shuning uchun ravon va tarixiy jihatdan to‘g‘ri javoblar kafolatlanmaydi. Sifat xulosasi `MODEL_CARD.md`, o‘lchovlar `evaluation/results.json` ichida.
- ZIP arxivga katta natija fayllari ham kiradi. GitHubga esa `.gitignore` sabab ma’lumotlar, tokenizer va checkpoint fayllari odatda kirmaydi.

## Tayyor ma’lumot

TinyStories ishlatilmaydi. O‘zbekcha Wikipedia’ning `20231101.uz` nusxasidan tarixga aloqador so‘zlar orqali 600 maqola olingan. Tozalash va filtrlashdan keyin 553 ta qolgan:

| Qism | Hujjat | Token | Vazifasi |
|---|---:|---:|---|
| `train` | 499 | 828 698 | Model va tokenizer o‘rganadi |
| `val` | 27 | 27 518 | O‘qitish vaqtida yaxshiroq modelni tanlash |
| `test` | 27 | 26 215 | Tanlangan modelning yakuniy bahosi |

Hujjatlar avval bo‘lingan, tokenizer faqat `train` matnlarida o‘rgatilgan. Har bir yozuvda manba va litsenziya saqlangan. Tanlash avtomatik bo‘lgani uchun geografiya va madaniyatga oid matnlar ham uchraydi. Batafsil: [DATASET_CARD.md](DATASET_CARD.md).

## Model tuzilmasi

| Sozlama | Qiymat | Ma’nosi |
|---|---:|---|
| Parametr | 1 334 016 | O‘qitishda o‘zgaradigan sonlar |
| Lug‘at | 4 096 | Tokenizer taniydigan tokenlar |
| Kontekst | 128 token | Bir hisoblashda ko‘riladigan eng uzun matn |
| Qatlam | 4 | Ketma-ket Transformer bloklari |
| Vektor | 128 | Har bir tokenning sonli tasviri uzunligi |
| E’tibor boshi | 4 | Oldingi tokenlarni turli yo‘nalishda solishtirish |
| Dropout | 0,10 | O‘qitishda ayrim qiymatlarni vaqtincha o‘chirish |
| Asosiy o‘qitish | 800 qadam | Sozlangan vazn yangilanishlari soni |

Model faqat oldingi tokenlarga qaraydi. Kirish token jadvali bilan chiqish vazni birgalikda ishlatiladi. Bir optimizer qadami 8 × 2 × 128 = **2 048 token**ni qayta ishlaydi. 800 qadam — 1 638 400 token ko‘rish; paketlar tasodifiy tanlangani uchun bu barcha hujjatlarni aynan ikki marta to‘liq o‘qish degani emas.

## Windows 11 uchun o‘rnatish

ZIPni oching. VS Code’da `LLM_Model_UZ` papkasini ochib, terminalni shu papkada ishga tushiring. Python 3.11 yoki 3.12 kerak. CPU — kompyuterning asosiy protsessori; videokarta shart emas.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Quyidagi buyruqlarda `python` o‘rniga `.\.venv\Scripts\python.exe` yozishingiz mumkin. Virtual muhit faollashtirilgan bo‘lsa, `python`ning o‘zi yetarli.

Linux uchun:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

Colab’da loyiha papkasiga o‘ting, `pip install -r requirements.txt`ni bajaring. CUDA qo‘llab-quvvatlanadigan PyTorch mavjud bo‘lsa, uni CPU nashriga almashtirmang. `--device auto` mavjud GPUni avtomatik tanlaydi. GPUda ishlash ushbu topshirishda sinovdan o‘tkazilmagan.

## Tayyor modelni ishlatish

```bash
python evaluation/generate.py --prompt "Amir Temur" --max-tokens 80
python -m uvicorn deployment.app:app --host 127.0.0.1 --port 8000
```

Ikkinchi buyruqdan keyin brauzerda **http://127.0.0.1:8000** ni oching. `ui/index.html`ni alohida ikki marta bosib ochish yetarli emas: matn yaratish uchun server ishlashi kerak. `Ctrl+C` serverni to‘xtatadi.

## O‘zingiz qayta o‘qitish

Arxivdagi tayyor `dataset/*.bin` va `tokenizer/tokenizer.json` bilan boshlash uchun ma’lumotni qayta yuklash shart emas:

```bash
python scripts/train.py --config configs/run_01.yaml --out-dir checkpoints/mening_tajribam
python evaluation/evaluate.py --checkpoint checkpoints/mening_tajribam/model.pt --output evaluation/mening_natijam.json
python evaluation/generate.py --checkpoint checkpoints/mening_tajribam/model.pt --prompt "Buxoro shahri"
```

`--out-dir` yangi natijalarni boshqa papkaga yozadi. Eski `last.pt` turgan papkada tasodifan yangi o‘qitish boshlanmaydi. Modelning barcha 800 qadami tugagan bo‘lsa, shu sozlamada `--resume` qo‘shimcha qadam bajarmaydi.

O‘qitishni boshidan oxirigacha bajarish:

```bash
python scripts/run_all.py --skip-download --out-dir checkpoints/yangi_toliq_tajriba
```

Bu buyruq arxivdagi boshlang‘ich ma’lumotdan tozalash, filtrlash, bo‘lish, tokenizer va binar fayllarni qayta yaratadi, keyin o‘qitadi. **Boshqa tokenizer yaratilsa eski checkpoint bilan mos kelmasligi mumkin.** Tajribani alohida nusxada bajaring. Internetdan qayta olish uchun `--skip-download`ni olib tashlang; katta manba fayli tarmoq orqali o‘qilishi mumkin, 600 hujjat tanlash tarmoqda faqat 600 hujjat uzatiladi degani emas.

## To‘xtatish va davom ettirish

```bash
python scripts/train.py --out-dir checkpoints/davom_sinovi --stop-after 100
python scripts/train.py --out-dir checkpoints/davom_sinovi --resume checkpoints/davom_sinovi/last.pt
```

Checkpoint — o‘qitishning saqlangan holati. `model.pt` matn yaratish uchun ixcham vaznlar; `last.pt` esa vazn, optimizer, tasodifiy tanlov holatlari va qadamni saqlaydi. Davom ettirishda model tuzilmasi, ma’lumot, tokenizer va asosiy o‘qitish sozlamalari bir xil qolishi kerak. Bir xil CPU muhitida davom ettirish natijasi test bilan tekshirilgan; turli qurilmalar orasida aynan bir xil sonlar kafolatlanmaydi.

## Test va baholash

```bash
python -m pytest tests -q
python evaluation/evaluate.py
python scripts/verify_project.py
```

`pytest` — avtomatik tekshiruvlarni ishga tushiruvchi dastur. Testlar o‘rganish, kelajakni ko‘rmaslik, ma’lumot bo‘linishi, tokenizer, checkpointni tiklash hamda serverni tekshiradi. Testlarning o‘tishi matnning tarixiy jihatdan to‘g‘riligini tasdiqlamaydi.

`loss` — haqiqiy keyingi token bo‘yicha o‘rtacha xato; kichikroq bo‘lgani yaxshi. `perplexity = exp(loss)` — shu xatoning boshqa ko‘rinishi. Faqat bir xil tokenizer, ma’lumot va baholash usulida solishtiring. Yakuniy baholash `val` va `test`dagi barcha nishon tokenlarni hisoblaydi, `train` uchun esa birinchi 128 blokdan foydalanadi.

## Filtrdan o‘tgan va rad etilgan hujjatlar

```bash
python scripts/filter_data.py --examples 10
```

Notebook ichida:

```python
from src.jsonl_io import read_jsonl
from src.data_filter import show_filter_examples

filter_audit = read_jsonl("data/filtered/audit.jsonl")
passed_examples = show_filter_examples(filter_audit, status="passed", n=10, seed=42)
rejected_examples = show_filter_examples(filter_audit, status="rejected", n=10, seed=42)
```

`show_filter_examples is not defined` xatosi chiqsa, yuqoridagi import bajarilganini tekshiring. Notebook loyiha ildizida ishlasin. Qaysi filtr xato ishlaganini faqat hisob bilan emas, hujjatni o‘qib aniqlaysiz: kerakli matn rad etilganmi yoki sifatsiz matn o‘tganmi? Tafsilot: `LESSON_10_GUIDE.md`.

## Fayllar va keyingi ishlar

- [FAYLLAR_QOLLANMASI.md](FAYLLAR_QOLLANMASI.md) — har bir fayl vazifasi.
- [LESSON_10_GUIDE.md](LESSON_10_GUIDE.md) — bosqichlar va xatolarni tuzatish.
- [PROJECT_CHARTER.md](PROJECT_CHARTER.md) — maqsad va loyiha chegaralari.
- [MODEL_CARD.md](MODEL_CARD.md) — o‘qitilgan model va cheklovlar.
- [BAJARILGAN_VA_QOLGAN.md](BAJARILGAN_VA_QOLGAN.md) — tekshirilgan ishlar va qolgan vazifalar.
- [ATAMALAR.md](ATAMALAR.md) — ishlatilgan texnik atamalar izohi.
- [LICENSE.md](LICENSE.md) — kod va ma’lumot litsenziyasini ajratish.

Navbatdagi ish oldidan nusxa saqlash:

```bash
python scripts/export_project.py
```

Natija loyiha papkasi yonida ZIP bo‘lib yaratiladi. Ushbu buyruq `.git`, virtual muhit, kesh va maxfiy `.env`ni arxivlamaydi; kod, ma’lumot, model va hujjatlarni saqlaydi.
