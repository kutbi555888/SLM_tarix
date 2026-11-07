# Atamalarni sodda tushunish

| Atama | Ma’nosi |
|---|---|
| SLM | Kichik til modeli; keyingi matn bo‘lagini taxmin qiladi |
| Token | Matnning raqam bilan ifodalangan bo‘lagi |
| Tokenizer | Matnni token raqamlariga va yana matnga aylantiruvchi dastur |
| BPE | Ko‘p uchraydigan bo‘laklarni birlashtirib lug‘at hosil qilish usuli |
| Byte-level | Boshlang‘ich birliklar baytlar bo‘lishi; UTF-8 matndagi belgilar qamrab olinadi |
| `<eos>` | Hujjat tugaganini bildiradigan maxsus token |
| Dataset | Modelga beriladigan ma’lumotlar to‘plami |
| Train | Model o‘rganadigan qism |
| Validation, val | O‘qitish vaqtida natijani kuzatish qismi |
| Test | Yakunda alohida baholanadigan qism |
| Transformer | Tokenlar orasidagi aloqalarni e’tibor mexanizmi bilan hisoblaydigan tuzilma |
| Decoder-only | Oldingi tokenlardan kelib chiqib matnni davom ettiradigan tuzilma |
| Causal mask | Modelning hali kelmagan tokenlarni ko‘rishini to‘sadigan qoida |
| Attention | Qaysi oldingi tokenlardan ko‘proq ma’lumot olishni hisoblash |
| Embedding | Token raqamini sonlar vektoriga aylantirish |
| MLP | Vektorni chiziqli qatlamlar va chiziqli bo‘lmagan o‘zgarish orqali qayta ishlash |
| LayerNorm | Vektor qiymatlarini me’yorlashtirish qatlami |
| GELU | Murakkab bog‘lanishlarni o‘rganishga yordam beradigan chiziqli bo‘lmagan funksiya |
| Parametr, vazn | Model o‘qitishda o‘zgartiradigan son |
| Weight tying | Ikki joyda bitta vazn jadvalidan foydalanish |
| Batch | Bir hisoblashda olingan matnlar paketi |
| Block size | Model bir paytda ko‘ra oladigan tokenlar soni |
| Loss | Haqiqiy keyingi token bilan model bashorati o‘rtasidagi xato |
| Cross-entropy | Haqiqiy token ehtimoliga asoslangan xato hisoblash usuli |
| Gradient | Xatoni kamaytirish uchun vaznni qaysi tomonga o‘zgartirishni bildiradi |
| Optimizer, AdamW | Gradient asosida vaznlarni yangilaydigan algoritm |
| Learning rate, LR | Vaznlarni yangilash qadami kattaligi |
| Warmup | O‘rganish tezligini boshida asta oshirish |
| Cosine schedule | O‘rganish tezligini kosinus shaklida pasaytirish |
| Gradient accumulation | Bir necha kichik paket gradientini yig‘ib, keyin vaznni yangilash |
| Gradient clipping | Juda katta gradientni belgilangan chegaragacha kamaytirish |
| Weight decay | Juda katta vaznlarni cheklashga yordam beradigan kamaytirish |
| Dropout | O‘qitishda ayrim qiymatlarni tasodifiy vaqtincha o‘chirish |
| Step | Optimizerning bitta vazn yangilashi |
| Epoch | Ma’lumotni bir marta to‘liq ko‘rib chiqish; tasodifiy oynalar bilan stepga aynan tenglashtirilmaydi |
| Checkpoint | Model va o‘qitishning saqlangan holati |
| Resume | Saqlangan holatdan davom ettirish |
| Seed | Tasodifiy tanlovning boshlang‘ich soni |
| RNG state | Tasodifiy son generatorining ayni holati |
| Inference | O‘qitilgan modelni yangi matn yaratish uchun ishlatish |
| Logits | Keyingi tokenlar uchun hali ehtimolga aylantirilmagan sonli baholar |
| Softmax | Baholarni yig‘indisi birga teng ehtimollarga aylantirish |
| Temperature | Token tanlashdagi tasodifiylik darajasi |
| Top-k | Eng yuqori baholi k ta token orasidan tanlash |
| Top-p | Jami ehtimoli p chegarasiga yetadigan tokenlar orasidan tanlash |
| Repetition penalty | Oldin ishlatilgan tokenlarning yana tanlanish bahosini kamaytirish |
| Perplexity | `exp(loss)`; bir xil baholash sharoitida kichikroq qiymat yaxshi |
| Baseline | Natijani solishtirish uchun sodda boshlang‘ich usul |
| Bigram | Keyingi tokenni faqat oldingi bitta tokenga qarab taxmin qilish |
| Latency | So‘rov boshlanishidan javob tayyor bo‘lishigacha o‘tgan vaqt |
| Throughput | Bir soniyada qayta ishlangan tokenlar soni |
| CPU / GPU | Asosiy protsessor / parallel hisoblash uchun grafik protsessor |
| CUDA | Mos NVIDIA videokartalarida hisoblash muhiti |
| FP32 / FP16 / BF16 | Sonlarni turli bit aniqligida saqlash va hisoblash shakllari |
| API | Dasturlar o‘zaro so‘rov va javob almashadigan interfeys |
| Endpoint | Serverdagi muayyan vazifaga tegishli URL, masalan `/generate` |
| JSONL | Har qatori alohida JSON obyekt bo‘lgan matn fayli |
| YAML | Sozlamalarni o‘qish oson bo‘lgan ko‘rinishda yozish formati |
| SHA-256 | Fayl yoki matn o‘zgarganini solishtirishga xizmat qiluvchi nazorat qiymati |
| Deduplication | Takroriy hujjatlarni olib tashlash |
| Data leakage | Sinov ma’lumoti o‘qitishga aralashib, bahoni sun’iy yaxshilashi |
| CC BY-SA | Muallifni ko‘rsatish va tegishli o‘zgartirilgan nusxalarni bir xil shartlarda tarqatish litsenziyasi |
| Attribution | Muallif va manbani qayd etish |
| Docker | Dastur va muhitni konteyner ko‘rinishida ishga tushirish vositasi |
| Git / commit | Fayllar o‘zgarishlarini saqlash tizimi / saqlangan o‘zgarish holati |
