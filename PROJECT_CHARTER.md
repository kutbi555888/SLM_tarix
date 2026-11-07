# Loyiha pasporti

**Nomi:** Tarixcha SLM. **Maqsad:** o‘zbekcha tarixga aloqador matnlar orqali kichik til modelining to‘liq o‘quv jarayonini tushunarli ko‘rsatish.

Loyiha ma’lumotni olish, tozalash, filtrlash, takrorlarni chiqarish, qismlarga ajratish, tokenizer yaratish, Transformer modelini o‘qitish, holatini saqlash, baholash va mahalliy sahifada ishlatishni qamrab oladi.

## Qabul qilish mezonlari

1. Asl GitHub tuzilmasidagi fayllar va rasmda ko‘rsatilgan loyiha papkalari mavjud.
2. Sharhlar, qo‘llanmalar va foydalanuvchi xabarlari o‘zbekcha.
3. TinyStories o‘rniga manbasi va litsenziyasi yozilgan kichik o‘zbekcha to‘plam ishlatilgan.
4. Tokenizer faqat o‘qitish qismidan o‘rgangan; nazorat va test hujjatlari alohida.
5. Haqiqiy o‘qitilgan `model.pt`, davom ettirish holati va o‘qitish jurnali mavjud.
6. Model, ma’lumot, checkpoint va matn yaratish testlari bajarilgan.
7. Baholash natijalari o‘lchangan; to‘qima sifat ko‘rsatkichlari berilmagan.
8. Mahalliy ishlatish va yangi tajriba boshlash buyruqlari ko‘rsatilgan.

## Chegaralar

Bu kichik tajriba uchun yozilgan loyiha. U tayyor tarixchi yordamchi, katta suhbat modeli yoki tekshirilgan bilim bazasi emas. Internetdagi ommaviy xizmatga joylash, foydalanuvchi hisoblari va katta yuklamani boshqarish ushbu mahalliy namuna doirasiga kirmaydi. Docker fayli beriladi, lekin Docker ishlashi alohida tekshirilmasa tasdiqlangan deb hisoblanmaydi.

CPU asosiy tekshirish qurilmasidir. CUDA mavjud bo‘lsa kod undan foydalanishi mumkin, lekin boshqa qurilmada tezlik va natija farqlanadi. Tafsilotlar `BAJARILGAN_VA_QOLGAN.md`da.

## Kelib chiqish

Asos: https://github.com/davronbek-malikov/LLM_Model, olingan commit: `e7b94c9858dc24f8e275e5794362c011a9a35a78`. Ushbu moslashtirishda asl TinyStories checkpointi va ma’lumoti ishlatilmadi. GitHubga o‘zgartirish yuborilmagan; yakuniy natija alohida ZIP shaklida topshiriladi.
