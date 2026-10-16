# 🌿 Animore — Hayvonot Olami Portali

O'zbekiston va butun dunyo hayvonot olami, ularning o'xshash turlaridan qanday farqlanishi, real akustik tovushlari, O'zbekiston va Xalqaro Qizil kitob maqomi hamda Animore AI aqlli yordamchisiga ega bo'lgan himoyalangan (yopiq) veb-portal.

---

## 🌟 Asosiy Imkoniyatlar va Talablar Ijrosi

1. **Yopiq Tizim va Google Hisobi Bilan Kirish:**
   - Sayt to'liq yopiq tizim (`Gatekeeper middleware`): Tizimga kirmagan hech bir foydalanuvchi hayvonlar bazasini ko'ra olmaydi, avtomatik ravishda `/login` sahifasiga yo'naltiriladi.
   - Google Sign-In (OAuth 2.0 / Google Identity Services) orqali yoki tezkor Demo hisoblar (Foydalanuvchi / Administrator) orqali 1 ta tugma bilan kirish.
2. **Noyob Split-Hero Vizual Dizayni:**
   - **Chap tomon:** Yam-yashil voha va o'tloqzor tabiat foni. Pastki qismida yoqimli va chaqqon Quyon (*Lepus*), yuqori moviy osmonda esa qanot qoqib parvoz qilayotgan Qaldirg'och (*Hirundo rustica*).
   - **O'ng tomon:** Oltin quyoshli Afrika savannasi foni, akatsiya daraxti ostida sokin dam olib yotgan viqorli sherlar (*Panthera leo*).
   - **Markazda:** AI Bionik Neon ajratuvchi va kirish paneli.
3. **AI Animatsiya Bilan Saytga Kirish:**
   - Biometrik neyron to'rlar, glowing rings va bio-matritsa yuklanishi bilan futuristik kirish splash animatsiyasi.
4. **Orqa Fonga Mos Yozuvlar (Typography & Contrast):**
   - Frosted glass substrat (`backdrop-filter: blur(16px)`), matn soyalari (`text-shadow`), yuqori kontrastli neon zumrad, tilla rang va sof oq shriftlar — har qanday rasm ustida ham juda aniq va qulay o'qiladi.
5. **Hayvonlarning O'xshash Turlaridan Qanday Farqlanishi:**
   - Har bir hayvon kartasida *"O'xshash turlaridan farqi"* bloki (masalan: Gepard va Qoplon farqi, Sher va Yo'lbars farqi, Quyon va Krolik farqi, Qaldirg'och va Qorayaloq farqi, Jayron va Sayg'oq farqi).
   - Maxsus `/compare` interaktiv laboratoriyasi: istalgan 2 ta hayvonni tanlab, yonma-yon solishtirish jadvali, rasmlari va farqlovchi belgilarini ko'rish.
6. **Hayvonlarning Real Tovushlari (Web Audio Sintezi & Audio Player):**
   - Sherning haybatli o'kirishi (roar), qaldirg'ochning quvnoq sayrashi (chirp/trill), quyon signallari (thump), bo'rining uvillashi (howl), burgut qichqirig'i (screech), delfin tovushlari.
   - Web Audio API sintezatori yordamida audio fayl bo'lmaganda ham 100% holatda real tovush chiqariladi va to'lqinli ekvalayzer animatsiyasi ishlaydi.
7. **O'zbekiston va Xalqaro Qizil Kitob:**
   - O'zbekiston Qizil kitobi maqomi (1-toifa, 2-toifa, 3-toifa, yo'qolgan turlar) va IUCN Xalqaro maqomi (CR, EN, VU, NT, LC).
   - Maxsus `/redbook` bo'limi va filtrlar.
8. **Animore AI Yordamchisi:**
   - Zoologiya va tabiat bo'yicha integratsiyalangan chat yordamchisi (`/ai-chat` va barcha sahifalardagi suzuvchi tugma).
   - Gemini API kaliti kiritilsa Gemini orqali ishlaydi, kalitsiz ham o'rnatilgan aqlli biologik bilim moduli orqali o'zbek tilida savol-javob beradi.
9. **Admin Panel (`/admin`):**
   - Yangi hayvon qo'shish va tahrirlash (tavsifi, o'xshash turlardan farqi, qizil kitob maqomi).
   - Kompyuterdan rasm yuklash va preview qilish.
   - Kompyuterdan audio yuklash va eshitib ko'rish.
   - Foydalanuvchilar ro'yxati va tizim sozlamalari (Google Client ID, Gemini API Key).

---

## 🚀 Ishga Tushirish Yo'riqnomasi

### 1. Loyiha papkasiga o'tish:
```powershell
cd "C:\Users\423-COMP-05\.gemini\antigravity\scratch\hayvonlar_olami"
```

### 2. Serverni ishga tushirish:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

### 3. Brauzerda ochish:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

- Agar hali kirmagan bo'lsangiz, avtomatik ravishda chiroyli **Split Hero** (chapda maysazorda quyon va qaldirg'och, o'ngda savannada yotgan sherlar) kirish sahifasi ochiladi.
- Tizimni sinash uchun **"👤 Foydalanuvchi (Google)"** yoki **"🛡️ Administrator"** tugmasini bosing yoki o'z Google hisobingiz bilan kiring!
