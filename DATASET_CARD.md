# Tarixcha ma’lumotlar to‘plami

## Manba va maqsad

- Manba: [wikimedia/wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia).
- Til va nusxa: `20231101.uz`, ya’ni 2023-yil 1-noyabrdagi o‘zbekcha to‘plam.
- Aniq manba holati: `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`.
- Manba turi: Wikipedia maqolalari; sun’iy yaratilgan TinyStories ma’lumoti emas.
- Mualliflar: o‘zbekcha Wikipedia ishtirokchilari; har bir maqolaning tarix sahifasi yozuvda berilgan.
- Ishlatish maqsadi: kichik modelga o‘zbekcha matnning davomini bashorat qilishni o‘rgatish.

## Haqiqiy tanlash natijasi

113 708 ta manba yozuvi ko‘rib chiqilgan, 600 ta tanlangan. Boshlang‘ich tanlangan matnlarda 3 022 553 belgi bo‘lgan. Har bir maqolaning sarlavhasida tarixga oid so‘z bo‘lishi yoki birinchi 2 000 belgisida kamida uchta mavzu so‘zi uchrashi talab qilinadi. Dastlabki 4 000 belgining harflari orasida kamida 90% lotin harflari bo‘lishi tekshiriladi.

Bu mavzuni taxminiy tanlash usuli. Barcha maqolalar faqat tarix haqida degan xulosa qilinmaydi: til, shahar, madaniyat va geografiya matnlari ham kirishi mumkin. To‘liq ro‘yxat va asl matnlar `data/raw/tarix.jsonl`da; qoidalar `configs/data.yaml`da.

## Tozalash va filtrlash

HTML belgilari olib tashlangan, Unicode hamda apostrof shakllari birxillashtirilgan, ortiqcha bo‘shliq va boshqaruv belgilaridan tozalangan. Matn tarjima qilinmagan yoki yangi faktlar bilan to‘ldirilmagan.

| Qoida | Chegara | Birinchi rad sababi sifatida sanalgan hujjatlar |
|---|---|---:|
| Eng qisqa matn | 400 belgi | 44 |
| Eng uzun matn | 100 000 belgi | 0 |
| Harflar ulushi | Kamida 0,40 | 0 |
| Takroriy qatorlar ulushi | Ko‘pi bilan 0,30 | 3 |

600 ta matn tozalangan; 47 tasi rad etilgan, 553 tasi qolgan. Bitta hujjatda bir nechta sabab bo‘lsa, umumiy statistikada birinchisi sanaladi; barcha sabablar `failed_rules`da saqlanadi. `data/filtered/audit.jsonl` barcha tekshiruvlarni, `rejected.jsonl` rad etilgan matnlarni saqlaydi.

Bo‘shliq va harf kattaligi birxillashtirilgan matnning SHA-256 nazorat qiymati orqali aynan bir xil nusxalar qidirilgan. Ushbu kichik to‘plamda bunday dublikat topilmagan. Mazmunan juda yaqin nusxalarni aniqlash hali qo‘shilmagan.

## Ajratish va tokenizer

| Qism | Hujjatlar | Tokenlar |
|---|---:|---:|
| O‘qitish — `train` | 499 | 828 698 |
| Nazorat — `val` | 27 | 27 518 |
| Yakuniy sinov — `test` | 27 | 26 215 |

Tasodifiy boshlang‘ich son 42. 5% nazorat va 5% yakuniy sinov uchun ajratilgan; butun hujjatlar bo‘lingan. Token ulushlari hujjat ulushlariga teng emas, chunki maqolalar turli uzunlikda.

Byte-level BPE tokenizer faqat `train` matnida o‘rgatilgan. U 4 096 tokenli lug‘at va `<eos>` hujjat tugashi belgisidan foydalanadi. `val` va `test` matnlari tokenizer lug‘atini o‘rgatishda qatnashmagan. Har hujjat oxiriga `<eos>` qo‘shilgan. `.bin` fayllar `uint16`, ya’ni har token raqami uchun 2 bayt formatida yozilgan.

## Yozuv maydonlari

| Maydon | Mazmuni |
|---|---|
| `id`, `title` | Maqola raqami va sarlavhasi |
| `text` | Matn |
| `url`, `history_url` | Maqola va mualliflar/tahrirlar tarixi |
| `source`, `revision`, `snapshot` | Manba va aniq nusxa |
| `license`, `attribution` | Litsenziya va mualliflik qaydi |
| `changes` | Matnga qilingan texnik o‘zgarishlar |
| `metrics`, `failed_rules`, `status` | Filtr o‘lchovlari, rad sabablari va natija |
| `text_hash` | Takrorni aniqlash uchun nazorat qiymati |

## Litsenziya

Hugging Face’dagi [manba kartasi](https://huggingface.co/datasets/wikimedia/wikipedia/blob/main/README.md) CC BY-SA 3.0 va GFDLni ko‘rsatadi; ayrim matnlar faqat Creative Commons shartlari ostida bo‘lishi mumkinligini ham aytadi. Ushbu matnlar nusxasi uchun **CC BY-SA 3.0** yo‘li ko‘rsatilgan.

Matnni ulashishda mualliflik qaydi, maqola manbasi va [litsenziya havolasi](https://creativecommons.org/licenses/by-sa/3.0/) saqlanadi. O‘zgartirilgan matn tarqatilganda o‘zgarishlar ko‘rsatiladi va tegishli ShareAlike sharti bajariladi. Ushbu arxivdagi tozalangan matnlar ham CC BY-SA 3.0 ostida beriladi. Mualliflar yoki Wikimedia loyihani qo‘llab-quvvatlaydi degan ma’no yo‘q.

Ma’lumot litsenziyasi butun dastur kodiga yoki model vaznlariga avtomatik bir xil litsenziya belgilamaydi. Kodning kelib chiqishi va litsenziya holati `LICENSE.md` hamda `THIRD_PARTY_NOTICES.md`da alohida yozilgan.

## Cheklovlar

Maqolalar qo‘lda to‘liq ko‘rib chiqilmagan; sanalar, shaxslar va voqealarda xatolar yoki tarafkashlik bo‘lishi mumkin. Shaxsiy ma’lumotni maxsus aniqlash filtri yo‘q. Ma’lumotdan ko‘chirib chiqarish ehtimoli mavjud. Kichik nazorat va test qismlari barcha o‘zbekcha tarix matnlarini ifodalamaydi. Fakt tekshirish, to‘liq mavzu auditi va mazmunan yaqin nusxalarni tozalash keyingi yaxshilash ishlaridir.
