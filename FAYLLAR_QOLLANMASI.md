# Har bir fayl nima qiladi?

Python va sozlama nomlari dastur mosligi uchun asl ko‘rinishda; izohlar o‘zbekcha. Binar fayllarni matn muharririda ochish shart emas.

| Fayl | Vazifa |
|---|---|
| `.dockerignore` | Docker yig‘ishda keraksiz fayllarni tashqarida qoldiradi. |
| `.env.example` | Server va model yo‘llari uchun maxfiy qiymatsiz namuna. |
| `.gitignore` | Qayta yaratiladigan katta fayllar, kesh va sirlarni Gitdan chiqaradi. |
| `ATAMALAR.md` | Atamalarni sodda tushunish — / Atama / Ma’nosi / |
| `BAJARILGAN_VA_QOLGAN.md` | Bajarilgan va qolgan ishlar — Bajarilgan |
| `DATASET_CARD.md` | Tarixcha ma’lumotlar to‘plami — Manba va maqsad |
| `DAVOM_ETTIRISH_HOLATI.md` | Bu davom ettirishdan OLDINGI tarixiy holat. Joriy natija: BAJARILGAN_VA_QOLGAN.md. Quyidagi yetishmagan fayllar keyin qo‘shildi. — Davom ettirish oldidan saqlangan holat |
| `FAYLLAR_QOLLANMASI.md` | Ushbu fayl: har bir loyiha faylining vazifasi. |
| `FILE_INVENTORY.json` | Arxivlash oldidagi fayllar, hajmlar va SHA-256 qiymatlari; o‘zini sanamaydi. |
| `LESSON_10_GUIDE.md` | Loyihani bosqichma-bosqich ishlatish — Avval `README.md`dagi o‘rnatishni bajaring. Barcha buyruqlar loyiha ildizidagi terminalda ishlatiladi. Tayyor ZIPda ma’lumot, tokenizer va binar fayllar bor; ularni qayta yaratish shart emas. Quyidagi ketma-ketlik jarayon |
| `LICENSE.md` | Kod va ma’lumot litsenziyasi — Kod |
| `MODEL_CARD.md` | Tarixcha SLM — model kartasi — **Holati:** o‘qitish va ishlatish zanjiri ishlaydi, ammo mazmunli va ravon matn yaratish sifati hali yetarli emas. Bu o‘quv tajribasi checkpointidir. |
| `PROJECT_CHARTER.md` | Loyiha pasporti — **Nomi:** Tarixcha SLM. **Maqsad:** o‘zbekcha tarixga aloqador matnlar orqali kichik til modelining to‘liq o‘quv jarayonini tushunarli ko‘rsatish. |
| `README.md` | Tarixcha SLM — **O‘zbekcha tarix matnlarini davom ettirish uchun kichik til modeli va uni noldan o‘qitishni o‘rganish loyihasi.** SLM — *Small Language Model*, ya’ni kichik til modeli. Bu yerda ma’lumotni olishdan boshlab modelni saqlash va mahalliy sahifada i |
| `SOURCE_REFERENCE.json` | Asl GitHub manzili, commit va fayllar ro‘yxati. |
| `THIRD_PARTY_NOTICES.md` | Tashqi manbalar qaydi — / Manba / Ushbu loyihadagi o‘rni / |
| `checkpoints/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `checkpoints/README.md` | checkpoints papkasi — model.pt — eng yaxshi nazorat xatosidagi ixcham model; best.pt — o‘sha holatning to‘liq nusxasi; last.pt — oxirgi qadamning to‘liq nusxasi. train_log.jsonl — o‘qitish/baholash jurnali. Davom ettirish uchun last.pt ishlatiladi. Bular faqat |
| `checkpoints/best.pt` | Eng yaxshi modelning optimizer va tasodifiy holatlar bilan to‘liq nusxasi. |
| `checkpoints/last.pt` | Oxirgi qadam; o‘qitishni tiklash uchun to‘liq holat. |
| `checkpoints/model.pt` | Matn yaratish uchun eng yaxshi nazorat natijasidagi model vaznlari. |
| `checkpoints/train_log.jsonl` | O‘qitish qadamlari, xato, gradient va tezlikning haqiqiy jurnali. |
| `configs/README.md` | configs papkasi — Sozlamalar: data.yaml manba va filtrlarni, run_01.yaml asosiy model/o‘qitishni, smoke.yaml 12 qadamlik tezkor sinovni belgilaydi. Kalitlarni tarjima qilmang: Python kodi ularni shu nomlar bilan o‘qiydi. Batafsil ma’nolar README.md va ATAMALAR |
| `configs/data.yaml` | Ma’lumot manbasi, mavzu, filtr va ajratish sozlamalari. |
| `configs/run_01.yaml` | 800 qadamlik asosiy model va o‘qitish sozlamalari. |
| `configs/smoke.yaml` | 12 qadamlik kichik ishlash sinovi. |
| `data/README.md` | data papkasi — Matnlar va manbalar. raw — asl nusxa; cleaned — tozalangan; filtered — filtr natijasi va rad sabablari; final — takrorsiz va ajratilgan hujjatlar. source_manifest.json tanlash qoidalari va sonlarni saqlaydi. Matnlar CC BY-SA 3.0 shartlari ostida |
| `data/cleaned/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `data/cleaned/README.md` | data/cleaned papkasi — tarix.jsonl: Unicode, apostrof, HTML va bo‘shliqlar tozalangan matnlar. statistics.json kirgan/chiqqan sonlarni saqlaydi. changes maydoni o‘zgarishlarni qayd etadi. Litsenziya: CC BY-SA 3.0; asl manbalar har yozuvda. |
| `data/cleaned/statistics.json` | Shu bosqichning kirish/chiqish va rad/takror sonlari. |
| `data/cleaned/tarix.jsonl` | Tozalangan maqolalar, o‘zgarishlar va manbalar. |
| `data/filtered/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `data/filtered/README.md` | data/filtered papkasi — tarix.jsonl: filtrdan o‘tganlar; rejected.jsonl: rad etilganlar; audit.jsonl: barcha hujjat va tekshiruvlar; statistics.json: umumiy sonlar. python scripts/filter_data.py --examples 10 orqali ikki guruhdan misollar o‘qing. Litsenziya: C |
| `data/filtered/audit.jsonl` | Filtr natijalari; o‘tgan/rad etilgan matnlar va sabablar. |
| `data/filtered/rejected.jsonl` | Filtr natijalari; o‘tgan/rad etilgan matnlar va sabablar. |
| `data/filtered/statistics.json` | Shu bosqichning kirish/chiqish va rad/takror sonlari. |
| `data/filtered/tarix.jsonl` | Filtr natijalari; o‘tgan/rad etilgan matnlar va sabablar. |
| `data/final/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `data/final/README.md` | data/final papkasi — tarix.jsonl: aynan bir xil nusxalar tekshirilgan to‘plam. train.jsonl o‘qitish, val.jsonl nazorat, test.jsonl yakuniy sinov uchun. splits.json hujjat raqamlarini saqlaydi. statistics.json dublikatlar hisobini beradi. Tokenizer faqat train. |
| `data/final/splits.json` | Har bir qismdagi hujjat identifikatorlari. |
| `data/final/statistics.json` | Shu bosqichning kirish/chiqish va rad/takror sonlari. |
| `data/final/tarix.jsonl` | Takrorsiz hujjatlar yoki nomi ko‘rsatilgan train/val/test qismi. |
| `data/final/test.jsonl` | Takrorsiz hujjatlar yoki nomi ko‘rsatilgan train/val/test qismi. |
| `data/final/train.jsonl` | Takrorsiz hujjatlar yoki nomi ko‘rsatilgan train/val/test qismi. |
| `data/final/val.jsonl` | Takrorsiz hujjatlar yoki nomi ko‘rsatilgan train/val/test qismi. |
| `data/raw/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `data/raw/README.md` | data/raw papkasi — tarix.jsonl: mavzu so‘zlari orqali tanlangan 600 asl maqola. Har qatorda bitta hujjat, manba URLi, sarlavha, litsenziya va mualliflar tarixi bor. Bu bosqichda mahalliy tozalash bajarilmagan. |
| `data/raw/tarix.jsonl` | Asl maqolalar, manbalar va litsenziya. |
| `data/source_manifest.json` | Manba nusxasi, mavzu qoidalari va tanlash sonlari. |
| `dataset/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `dataset/README.md` | dataset papkasi — train.bin, val.bin, test.bin matn tokenlarining uint16 raqamlari: har raqam 2 bayt. Bular matn muharririda o‘qilmaydi. meta.json format, hujjat/token sonlari va SHA-256 nazorat qiymatlarini saqlaydi. Ushbu fayllar faqat o‘z tokenizer/tokenize |
| `dataset/meta.json` | Token formati, hajmlar va tokenizer/dataset SHA-256 nazorat qiymatlari. |
| `dataset/test.bin` | Yakuniy sinov uchun token raqamlari; uint16. |
| `dataset/train.bin` | Model o‘rganadigan token raqamlari; uint16. |
| `dataset/val.bin` | O‘qitishda nazorat uchun token raqamlari; uint16. |
| `deployment/Dockerfile` | Model va mahalliy sahifani CPU konteynerida ishga tushirish retsepti. |
| `deployment/README.md` | deployment papkasi — app.py FastAPI serveri: / sahifa, /health tayyorlik, /generate matn yaratish. requirements.txt faqat ishlatish kutubxonalarini belgilaydi; Dockerfile CPU PyTorch bilan konteyner yaratadi. Model va tokenizer fayllari kerak. .env.example soz |
| `deployment/__init__.py` | Mahalliy API va brauzer sahifasi. |
| `deployment/app.py` | Bitta serverdan o'zbekcha sahifa va model API sini taqdim etadi. |
| `deployment/requirements.txt` | Faqat ishlatish/server uchun kutubxonalar; torch Dockerfileda o‘rnatiladi. |
| `evaluation/README.md` | evaluation papkasi — evaluate.py modelni baholaydi; perplexity.py xato hisoblari va sodda taqqoslash usullarini saqlaydi; generate.py terminaldan matn yaratadi. results.json haqiqiy o‘lchovlar; test_results.xml va test_run.txt avtomatik test dalillari; verific |
| `evaluation/__init__.py` | Model xatoligi va matn yaratish namunalari orqali baholash. |
| `evaluation/environment.json` | Amalda ishlatilgan Python va kutubxona versiyalari. |
| `evaluation/evaluate.py` | Train namunasi, validation va yakuniy test xatoligini hisoblaydi. |
| `evaluation/generate.py` | Boshlang'ich matndan davomini yaratadi. |
| `evaluation/perplexity.py` | O'rtacha token xatosi, perplexity va sodda taqqoslash modellari. |
| `evaluation/results.json` | Model xatosi, perplexity, taqqoslash usullari va yaratilgan matnlar. |
| `evaluation/test_results.xml` | Avtomatik testlarning mashina o‘qiydigan natijasi. |
| `evaluation/test_run.txt` | Test dasturining asl terminal chiqishi; 13 test va kutubxona ogohlantirishi. |
| `evaluation/verification.json` | Fayllar mavjudligi, nazorat qiymatlari va qismlar ajralganligi tekshiruvi. |
| `inference/README.md` | inference papkasi — engine.py model/tokenizerni bir marta yuklaydi va matn yaratadi. sampling.py keyingi tokenni tanlash, tasodifiylik, top-k, top-p hamda takror jazosi qoidalarini bajaradi. __init__.py papkani Python moduli qiladi. Model oldingi matnning oxir |
| `inference/__init__.py` | O‘qitilgan modeldan yangi matn yaratish. |
| `inference/engine.py` | Model va tokenizer bir marta yuklanadi; so'rovlar shu nusxadan foydalanadi. |
| `inference/sampling.py` | Model bergan sonli baholardan keyingi tokenni tanlaydi. |
| `railway.json` | Railway yig‘ish va tayyorlik so‘rovi konfiguratsiyasi; joylash tekshirilmagan. |
| `requirements.txt` | Ma’lumot tayyorlash, o‘qitish, API va test kutubxonalari. |
| `scripts/README.md` | scripts papkasi — Jarayonni terminaldan boshqarish buyruqlari. Har fayl boshidagi o‘zbekcha izoh uning vazifasini aytadi. run_all.py to‘liq ketma-ketlik; train.py o‘qitish/tiklash; verify_project.py tayyor natija mosligi; export_project.py ZIP nusxa. Bosqichla |
| `scripts/build_dataset.py` | Hujjatlarni train.bin, val.bin va test.bin token fayllariga aylantiradi. |
| `scripts/build_model.py` | Model tuzilmasi, aniq parametrlar va eng kam vazn xotirasini ko'rsatadi. |
| `scripts/clean_data.py` | Boshlang‘ich matnlarni tozalaydi. |
| `scripts/deduplicate_data.py` | Normallashtirilgan takrorlarni chiqarib tashlaydi. |
| `scripts/design_model.py` | Model tuzilmasi, aniq parametrlar va eng kam vazn xotirasini ko'rsatadi. |
| `scripts/download_data.py` | Tarix maqolalarini manba ma’lumotlari bilan yuklaydi. |
| `scripts/export_project.py` | Kod, ma'lumot va modelning mavjud holatini ZIP nusxaga saqlaydi. |
| `scripts/filter_data.py` | Filtrdan o‘tgan va rad etilgan matnlarni ajratadi. |
| `scripts/run_all.py` | Bosqichlarni bitta buyruq bilan ketma-ket bajaradi. |
| `scripts/split_data.py` | Tokenizer o‘rganishidan oldin hujjatlarni train, val va testga ajratadi. |
| `scripts/train.py` | Modelni o'qitadi yoki last.pt holatidan davom ettiradi. |
| `scripts/train_tokenizer.py` | BPE lug‘atini faqat train matnlaridan o‘rgatadi. |
| `scripts/verify_project.py` | Saqlangan dataset, tokenizer, checkpoint va asosiy fayllarni solishtiradi. |
| `src/README.md` | src papkasi — Asosiy qayta ishlatiladigan Python kodlari. Ma’lumot, tokenizer, model qatlamlari, o‘qitish va checkpoint alohida modullarga ajratilgan. Har fayl boshida vazifasi o‘zbekcha yozilgan. Qaysi fayl nima qilishi FAYLLAR_QOLLANMASI.mdda, atamalar ATAMA |
| `src/__init__.py` | Tarixcha SLM uchun qayta foydalaniladigan qismlar. |
| `src/attention.py` | Tokenlar o'zidan oldingi tokenlardan kerakli ma'lumotni oladi. |
| `src/checkpoint.py` | Model, optimizer, tasodifiy holatlar va keyingi qadamni saqlash/tiklash. |
| `src/data_cleaner.py` | Matnning yozilishini tozalaydi, manba va litsenziya maydonlarini saqlaydi. |
| `src/data_downloader.py` | Hugging Face'dan o'zbekcha tarix matnlari va ularning manbalarini oladi. |
| `src/data_filter.py` | Uzunlik, harflar va takroriy qatorlar bo'yicha tekshirish; rad sababi yo'qolmaydi. |
| `src/dataset_builder.py` | Hujjatni avval bo'ladi; keyin tokenlarni binar fayllarga yozadi. |
| `src/deduplicator.py` | Bir xil matnlar train va nazorat to'plamlariga tarqalib ketishini kamaytiradi. |
| `src/jsonl_io.py` | JSONL faylda har bir qator bitta hujjatni saqlaydi. |
| `src/lr_schedule.py` | O'rganish tezligi avval oshadi, so'ng kosinus bo'yicha pasayadi. |
| `src/mlp.py` | Har bir token vektorini alohida qayta ishlaydigan ikki chiziqli qatlam. |
| `src/model.py` | Keyingi tokenni bashorat qiluvchi kichik, faqat decoder asosidagi Transformer. |
| `src/model_config.py` | Model tuzilmasi va uning tekshiruvlari; o'qitish algoritmi bu faylda emas. |
| `src/paths.py` | Yo'llarni loyiha joylashgan papkadan hisoblaydi. |
| `src/seed.py` | Tasodifiy tanlovlarni bir xil boshlang'ich holatga keltiradi. |
| `src/tokenizer.py` | Matnni qaytarib tiklash mumkin bo'lgan bayt darajasidagi BPE tokenizer. |
| `src/train_config.py` | Modelni qanday o'qitish kerakligini belgilaydigan sozlamalar. |
| `src/trainer.py` | Paket olish, loss, gradient, optimizer, baholash va saqlashni birlashtiradi. |
| `src/transformer_block.py` | Bitta blok: normallashtirish, attention, qoldiq qo'shish va MLP. |
| `tests/README.md` | tests papkasi — python -m pytest tests -q bilan ishga tushadi. test_model.py model va o‘rganishni; test_data.py tokenizer/qismlar/chegaralarni; test_checkpoint.py to‘xtatib tiklashni; test_inference.py matn yaratish va API ni tekshiradi. conftest.py bir xil ta |
| `tests/conftest.py` | Sinovlar uchun bir xil tasodifiy holat va kichik CPU resursi. |
| `tests/test_checkpoint.py` | To'xtatib tiklash uzluksiz o'qitish bilan bir xil natija berishini tekshiradi. |
| `tests/test_data.py` | Matn yo'qolmasligi, qismlar ajralishi va paket chegaralarini tekshiradi. |
| `tests/test_inference.py` | Token tanlash va haqiqiy saqlangan modeldan foydalanish sinovlari. |
| `tests/test_model.py` | Model shakli, kelajakdan ma'lumot sizmasligi va o'rganishini tekshiradi. |
| `tokenizer/.gitkeep` | Bo‘sh papkani Gitda saqlash uchun belgi; dastur kodi emas. |
| `tokenizer/README.md` | tokenizer papkasi — tokenizer.json — faqat train matnlarida o‘rgatilgan byte-level BPE lug‘ati va birlashtirish qoidalari. Lug‘at 4096 token, <eos> raqami 0. Bu fayl checkpoint va dataset bilan birga saqlanishi kerak. Eski checkpointga mos bo‘lmagan tokenizer  |
| `tokenizer/tokenizer.json` | Train matnida o‘rgatilgan 4096 tokenli BPE lug‘ati va qoidalari. |
| `ui/.gitignore` | UI joylash xizmatining mahalliy sozlamalarini Gitdan chiqaradi. |
| `ui/README.md` | ui papkasi — index.html — o‘zbekcha mahalliy veb-sahifa. python -m uvicorn deployment.app:app --host 127.0.0.1 --port 8000 bilan serverni ishga tushiring, keyin http://127.0.0.1:8000 ni oching. Sahifa /generate APIga so‘rov yuboradi. Alohida tashqi skript yoki |
| `ui/index.html` | O‘zbekcha veb-sahifa: matn kiritish, sozlash va natija. |
