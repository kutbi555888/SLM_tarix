# Tarixcha SLM — model kartasi

**Holati:** o‘qitish va ishlatish zanjiri ishlaydi, ammo mazmunli va ravon matn yaratish sifati hali yetarli emas. Bu o‘quv tajribasi checkpointidir.

## Tuzilma va o‘qitish

- 1 334 016 parametr, 4 Transformer bloki, 128 o‘lchamli token vektori, 4 e’tibor boshi.
- Lug‘at 4 096 token, kontekst 128 token; `<eos>` hujjat tugashi belgisi.
- 800 optimizer qadami, har qadamda 2 048 token; jami 1 638 400 token ko‘rish.
- CPU, 2 oqim, FP32 aniqlik; seed 42. Muhit versiyalari `evaluation/environment.json`da.
- O‘qitish 100-qadamda to‘xtatildi va `last.pt`dan 800-qadamgacha davom ettirildi.
- Eng yaxshi saqlangan model: 800-qadam. Asl GitHub checkpointi ishlatilmagan.
- Ma’lumot: 499 ta o‘qitish, 27 ta nazorat, 27 ta yakuniy test hujjati. Batafsil `DATASET_CARD.md`da.

## Haqiqiy o‘lchovlar

| Qism | Loss — xato | Perplexity | Baholangan nishon tokenlar |
|---|---:|---:|---:|
| train | 5.3725 | 215.41 | 16,384 |
| val | 5.6645 | 288.45 | 27,517 |
| test | 5.5414 | 255.04 | 26,214 |

Train — dastlabki 128 blokdan namuna; val va test — barcha nishon tokenlar. Kontekst har 128 tokenlik blok boshida qayta boshlanadi. Shu sabab jurnalning tasodifiy oynalar bahosi bilan yakuniy hisobot qiymati biroz farq qiladi. Loss kichikroq bo‘lsa yaxshiroq; perplexity = exp(loss).

O‘qitish jurnalidagi bir xil nazorat oynalarida xato **8,3361 → 5,7016** bo‘lgan. Yakuniy nazorat loss **5.6645**. Barcha tokenlar teng ehtimolli usulda loss **8.3178**; faqat oldingi bitta tokenga qaraydigan bigram usulida nazorat loss **5.3332** (perplexity **207.10**).

**Natija talqini:** Transformer tasodifiy taxmindan yaxshiroq, lekin ushbu tajribada sodda bigram usulidan yomonroq. Uni yuqori sifatli tarix modeli deb baholashga asos yo‘q. To‘liq taqqoslash bir xil tokenizer va nazorat to‘plamida bajarilgan; blok boshida kontekst qisqarishi usullar orasida kichik protokol farqini qoldiradi.

## Matn yaratish sifati

`evaluation/results.json`dagi uchta matn avtomatik yordamchi tomonidan o‘qildi: buzilgan so‘zlar, takrorlar va tugallanmagan jumlalar bor. Bu rasmiy inson ekspertizasi emas. Tarixiy faktlar tekshirilmagan. O‘qitishni ko‘paytirish, sifatliroq/ko‘proq ma’lumot va nazorat tajribalari talab qilinadi; yaxshilanish oldindan kafolatlanmaydi.

60 token yaratish o‘lchovlari shu CPU muhitida taxminan 248–344 ms bo‘ldi. Bu bitta mahalliy sinov, umumiy tezlik kafolati emas. Latency — so‘rov hisoblanishi uchun ketgan vaqt. Bir vaqtdagi ko‘p so‘rovlar sinovdan o‘tkazilmagan.

## Saqlangan fayllar

`checkpoints/model.pt` — matn yaratish vaznlari; `best.pt` — eng yaxshi nazorat natijasining to‘liq o‘qitish holati; `last.pt` — oxirgi qadam holati; `train_log.jsonl` — haqiqiy o‘qitish jurnali. Model bilan birga aynan unga mos `tokenizer/tokenizer.json` ishlatiladi. Nazorat qiymatlari `dataset/meta.json` va checkpointda saqlangan.

## Tekshirish dalillari

13 ta avtomatik test o‘tdi. To‘xtatib tiklangan kichik o‘qitish va uzluksiz o‘qitish vaznlari aynan teng bo‘ldi. Tokenizer matnni tiklash, kelajak tokenlarini ko‘rmaslik, ma’lumot chegaralari va haqiqiy checkpoint orqali API so‘rovlari tekshirildi. `evaluation/test_results.xml`, `test_run.txt`, `verification.json` dalillarni saqlaydi.

## Qolgan yaxshilashlar

Mazmuniy sifatni oshirish va tarixiy faktlarni ekspert bilan baholash; mazmunan yaqin dublikatlarni aniqlash; CUDA/Colab T4 va Docker muhitida sinov; zarur bo‘lsa savol-javob uchun alohida moslashtirish. Sifat cheklovlari bartaraf etilmaguncha model javobini tarixiy manba sifatida ishlatish to‘g‘ri emas.

Litsenziya va manbalar `LICENSE.md`, `DATASET_CARD.md`, `THIRD_PARTY_NOTICES.md`da.
