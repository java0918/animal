import os
import sqlite3
import json
from database import init_db, get_connection, insert_animal, update_animal

ANIMALS_DATA = [
    {
        "name_uz": "Sher (Arslon)",
        "name_latin": "Panthera leo",
        "name_en": "Lion",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Katta tuyoqlilar, zebra, antilopa)",
        "habitat": "Afrika savannalari, ochiq butazorlar, o'tloqlar",
        "lifespan": "10 - 14 yil (tabiatda), 20 yilgacha (qo'riqxonalarda)",
        "speed": "80 km/soat (qisqa masofada)",
        "weight": "150 - 250 kg (erkagi), 120 - 180 kg (urg'ochisi)",
        "description": "Sher — mushuksimonlar oilasiga mansub eng yirik va qudratli yirtqichlardan biri. 'Hayvonlar qiroli' deb ataladi. Ular boshqa barcha mushuksimonlardan farqli ravishda 'prayd' deb ataluvchi ijtimoiy to'dalarda yashaydilar. Erkak sherlarning bo'ynidagi qalin va salobatli yol ularni dushmanlaridan himoya qiladi va ulug'vor ko'rsatadi.",
        "uz_red_book_status": "0 (Yo'qolib ketgan tur)",
        "uz_red_book_desc": "O'tmishda Markaziy Osiyo va O'zbekiston hududlarida (Amudaryo to'qaylarida) Turon arslonlari yashagan, ammo XX asr boshlariga kelib to'liq qirilib ketgan.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Yashash muhitining qisqarishi va brakonyerlik tufayli soni kamayib bormoqda.",
        "similar_species": "Yo'lbars (Panthera tigris), Leopard (Panthera pardus), Gepard (Acinonyx jubatus)",
        "differences": """1. YO'LBARSDAN FARQI: Sherlar savanna va ochiq maydonlarda jamoa (prayd) bo'lib yashaydi; yo'lbarslar esa qalin o'rmonlarda yolg'iz hayot kechiradi va suvda suzishni yaxshi ko'radi. Erkak sherda hashamatli yol bor, yo'lbarsda esa yo'l-yo'l chiziqli mo'yna bo'ladi.
2. LEOPARDDAN FARQI: Leopard tanasida dog'lar (rozetkalar) bo'ladi, daraxtga o'ljasini olib chiqadi va ancha kichikroq (60-90 kg). Sher daraxtga kam chiqadi va vazni deyarli 2-3 barobar og'ir.
3. GEPARDDAN FARQI: Gepard nozik qomatli, yuzida 'ko'z yoshi chizig'i' bor va tirnoqlari ichiga kirmaydi; sher esa bahaybat suyakli, tirnoqlari to'liq ichkariga tortiladi va jag' kuchi beqiyos darajada ustun.""",
        "sound_file": "/static/audio/lion_roar.mp3",
        "sound_description": "Sherning haybatli o'kirishi (roar) 8 kilometr masofagacha eshitiladi. Bu tovush orqali ular o'z hududini belgilaydi va prayd a'zolarini chaqiradi.",
        "sound_type": "lion",
        "image_url": "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1575550959106-5a7defe28b56?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Sherlar kuniga 18-20 soatgacha uxlashadi yoki dam olishadi.",
            "Praydda o'ljaning 85-90% qismini urg'ochi sherlar ovlaydi, lekin birinchi bo'lib erkak sher yeydi.",
            "Sherlarning ko'rish qobiliyati tunda insonga qaraganda 6 barobar kuchliroqdir."
        ]
    },
    {
        "name_uz": "Quyon (Yovvoyi quyon / Qum tovushqoni)",
        "name_latin": "Lepus tolai / Lepus europaeus",
        "name_en": "Hare / Rabbit",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (O't-o'lanlar, butalar po'stlog'i, ildizlar)",
        "habitat": "Cho'llar, dashtlar, to'qayzorlar, yashil maysazorlar va qirlar",
        "lifespan": "4 - 8 yil",
        "speed": "60 - 70 km/soat (chaqqon ilon izi sakrashlar)",
        "weight": "1.5 - 4.5 kg",
        "description": "Tovushqonlar (quyonlar) — chaqqon, sezgir va quloqlari juda rivojlangan sutemizuvchi hayvon. O'zbekistonning barcha hududlarida, ayniqsa cho'l va to'qay mintaqalarida uchraydi. Xavf tug'ilganda chaqmoqdek tezlik bilan yo'nalishini keskin o'zgartirib yugura oladi.",
        "uz_red_book_status": "Kiritilmagan (Keng tarqalgan)",
        "uz_red_book_desc": "O'zbekiston tabiatida soni barqaror, cho'l va dasht ekotizimida muhim ozuqa zanjiri bo'g'ini hisoblanadi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xavf ostida emas). Dunyo bo'ylab populyatsiyasi keng tarqalgan.",
        "similar_species": "Xonaki quyon (Oryctolagus cuniculus / Krolik), Pixa (Pika)",
        "differences": """1. XONAKI QUYON (KROLIK)DAN FARQI: Tovushqon (zayats) in qazmaydi, yer ustidagi maysalarda yotadi; krolik esa yer ostida chuqur murakkab inlar qazib yashaydi.
2. BOLALARI TUG'ILISHI: Tovushqon bolalari ko'zlari ochiq, tanasi to'liq yung bilan qoplangan va tug'ilishi bilanoq yugura oladigan bo'lib dunyoga keladi. Krolik bolalari esa ko'zi yumuq, yungsiz va mutlaqo ojiz tug'iladi.
3. TANA TUZILISHI: Tovushqonlarning orqa oyoqlari va quloqlari kroliknikidan ancha uzun va qudratli, tezlikda krolikdan ancha ustun.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Quyonlar odatda jim yuradi, lekin xavf sezganda orqa oyoqlarini yerga qattiq urib signal beradi, qattiq qo'rqqanda ingichka qiyqiriq (thumping & squeak) chiqaradi.",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1591382696684-38c427c7547a?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1535268647677-300dbf3d78d1?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Quyonlarning ko'rish burchagi deyarli 360 darajani tashkil qiladi, ya'ni ular boshini burmasdan orqasini ko'ra oladilar.",
            "Quyonlarning tishlari butun umri davomida to'xtovsiz o'sadi, shuning uchun ular qattiq po'stloqlarni kemirib turishadi.",
            "Qochayotganda 3 metrgacha balandlikka va 5 metrgacha uzunlikka sakray oladi."
        ]
    },
    {
        "name_uz": "Qaldirg'och (Qishloq qaldirg'ochi)",
        "name_latin": "Hirundo rustica",
        "name_en": "Barn Swallow",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Hasharotxo'r (Chivinlar, pashshalar, mayda qo'ng'izlar)",
        "habitat": "Ochiq dala, qishloqlar, daryo bo'ylari, inson uylari ayvonlari",
        "lifespan": "4 - 8 yil",
        "speed": "50 - 75 km/soat (havoda parvoz)",
        "weight": "16 - 22 gramm",
        "description": "Qaldirg'och — bahor elchisi, o'zining ayrisimon uzun dumi va chaqqon parvozi bilan mashhur ko'chmanchi qush. Moviy-qora yaltiroq pati, qizg'ish peshonasi va oppoq ko'kragi bor. Insonlar yashaydigan joylarga yaqin yerda loy va o't poyalaridan mustahkam in quradi.",
        "uz_red_book_status": "Kiritilmagan",
        "uz_red_book_desc": "O'zbekistonda keng tarqalgan, bahorda uchib kelib ko'payadi, kuzda issiq o'lkalarga uchib ketadi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xavf yo'q). Global miqyosda juda ko'p sonli turlardan biri.",
        "similar_species": "Qorayaloq (Apus apus / Swift), Shahar qaldirg'ochi (Delichon urbicum)",
        "differences": """1. QORAYALOQ (SWIFT)DAN FARQI: Qaldirg'och simlarga yoki shoxlarga bemalol qo'na oladi, chunki oyoq panjalari mustahkam. Qorayaloq esa tekis yerdan o'zi ucha olmaydi, oyoqlari juda qisqa bo'lib faqat vertikal devorlarga tirmashadi.
2. DUM VA QANOT TUZILISHI: Qaldirg'ochning dumi chuqur ayrilgan ('vilka' shaklida) va ingichka uzun patlari bor. Qorayaloqning qanotlari o'roqsimon (yarim oy) uzunroq va tanasi qoramtir-kulrang.
3. IN QURISHI: Qaldirg'och inini ochiq kosa shaklida loydan yasaydi; shahar qaldirg'ochi esa faqat kichik teshikli yopiq sharsimon in quradi.""",
        "sound_file": "/static/audio/swallow_song.mp3",
        "sound_description": "Qaldirg'ochning jarangdor va yoqimli sayrashi (chirp-trill). Ular havoda hasharot ovlayotganda yoki inida o'tirganda quvnoq chuldirashadi.",
        "sound_type": "swallow",
        "image_url": "https://images.unsplash.com/photo-1555661530-68c8e9894ae6?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1549608276-5786777e6587?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1522926197415-e55c256df0df?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Qaldirg'ochlar havoda uchib ketayotib suv ustidan sirg'alib suv ichishga qodir yagona qushlardan biridir.",
            "Ular har yili Afrika va Janubiy Osiyodan Markaziy Osiyo va Yevropaga 10 000 km dan ortiq masofani bosib o'tib qaytib kelishadi.",
            "Bitta qaldirg'och oilasi yoz fasli davomida 1 milliontagacha zararli hasharot va chivinlarni yo'q qiladi."
        ]
    },
    {
        "name_uz": "Qor qoploni (Ilbirs)",
        "name_latin": "Panthera uncia / Uncia uncia",
        "name_en": "Snow Leopard",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Tog' echkilari, arxarlar, sug'urlar, kakliklar)",
        "habitat": "Tyan-Shan va Pomir-Oloyning baland qoyali tog'lari (3000-5000 metr)",
        "lifespan": "15 - 18 yil (tabiatda), 22 yilgacha (tutqunlikda)",
        "speed": "65 km/soat (tik qoyalarda chaqqon sakrash)",
        "weight": "35 - 55 kg",
        "description": "Qor qoploni (Ilbirs) — Markaziy Osiyo baland tog'larining afsonaviy 'ruhi' hisoblangan o'ta kamyob va ulug'vor yirtqich. Uning uzun qalin dumi tik qoyalarda sakraganda muvozanat saqlovchi rol o'ynaydi va sovuq tunlarda burni hamda panjalarini isitish uchun adyol vazifasini o'taydi. O'zbekistonning eng qattiq muhofaza qilinadigan ramziy hayvoni.",
        "uz_red_book_status": "1 (Yo'qolib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I-ilovasiga kiritilgan. G'issar, Chotqol va Zomin davlat qo'riqxonalarida qat'iy muhofaza qilinadi. Respublika hududida 80-100 tagina saqlanib qolgan.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Global populyatsiyasi 4000-6500 donani tashkil qiladi.",
        "similar_species": "Oddiy qoplon (Panthera pardus), Gepard (Acinonyx jubatus), Silovsin (Lynx)",
        "differences": """1. ODDIY QOPLON (LEOPARD)DAN FARQI: Qor qoplonining yungi ancha qalin, tutunsimon kulrang-oq rangda (qorga moslashgan), oddiy leopardniki esa yorqin sarg'ish.
2. DUMNING TUZILISHI: Ilbirsning dumi deyarli tana uzunligiga teng (1 metr) va o'ta qalin yung bilan qoplangan; boshqa hech qaysi mushuksimonda bunday baquvvat dum yo'q.
3. OVOZ VA O'KIRISH: Ilbirs bo'g'iz tuzilishi sababli sher yoki yo'lbars kabi baland o'kira olmaydi — u faqat mayin pishqiradi va past xirillaydi.""",
        "sound_file": "/static/audio/lion_roar.mp3",
        "sound_description": "Qor qoplonining o'ziga xos xirillashi va chaqiruv pishqirig'i.",
        "sound_type": "lion",
        "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1575550959106-5a7defe28b56?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Qor qoploni bir sakrashda 15 metrgacha masofani (tik jarliklar uzra) zabt eta oladi — bu barcha sutemizuvchilar ichida mutlaq rekord!",
            "Keng va junli panjalari xuddi qor chang'isi kabi ishlaydi va chuqur qorga botib ketishiga yo'l qo'ymaydi.",
            "Ular shunchalik ehtiyotkor va yashirin yashaydiki, mahalliy xalq ularni 'tog' sharpalari' deb ataydi."
        ]
    },
    {
        "name_uz": "Gepard",
        "name_latin": "Acinonyx jubatus",
        "name_en": "Cheetah",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Jayronlar, impalalar, quyonlar, mayda tuyoqlilar)",
        "habitat": "Afrika savannalari, o'tmishda Ustyurt va Qizilqum cho'llari",
        "lifespan": "10 - 12 yil",
        "speed": "110 - 120 km/soat (sayyoramizdagi eng tezyurar quruqlik jonivori)",
        "weight": "35 - 65 kg",
        "description": "Gepard — Yerdagi eng tezyurar quruqlik jonzoti. 0 dan 100 km/soat tezlikka atigi 3 soniyada erisha oladi (sportkar avtomobillaridan ham tezroq). Aerodinamik ingichka tana, keng o'pka va yurak, hamda ichiga kirmaydigan tirnoqlari unga yuqori tezlikda o'tkir burilishlar yasash imkonini beradi.",
        "uz_red_book_status": "0 (Yo'qolib ketgan)",
        "uz_red_book_desc": "Osiyo gepardi (Acinonyx jubatus raddei) XX asrning 60-70-yillariga qadar Ustyurt platosi va Qoraqalpog'iston cho'llarida yashagan. Hozirda O'zbekiston tabiatida to'liq yo'qolib ketgan.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Butun dunyo bo'yicha yovvoyi tabiatda 7000 dan kam gepard qolgan.",
        "similar_species": "Leopard (Panthera pardus), Yaguar, Qor qoploni",
        "differences": """1. LEOPARDDAN FARQI: Gepardning yuzida ko'z burchagidan og'ziga tushgan qora 'ko'z yoshi chizig'i' bor (quyosh nuridan saqlaydi); leopardda bunday chiziq yo'q.
2. TIRNOQLARI: Gepardning tirnoqlari butsa tishlari kabi doimo ochiq turadi va ichkariga tortilmaydi; boshqa barcha mushuksimonlarda tirnoqlar to'liq barmoq ichiga kiradi.
3. TANA TUZILISHI: Gepard ingichka oyoqli, nozik qomatli va tezlikka moslashgan; leopard esa qalin muskulli, og'ir suyakli va pinhona poylashga moslashgan.""",
        "sound_file": "/static/audio/lion_roar.mp3",
        "sound_description": "Gepardlar o'kirmaydi, balki xuddi qushlar kabi jarangdor chirillaydi va xonaki mushuk kabi xurillaydi (purr).",
        "sound_type": "lion",
        "image_url": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1517825738774-7de9363ef735?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Gepard maksimal tezlikda chopganda bir sakrashda 7 metr masofani bosib o'tadi va chopish vaqtining yarmini havoda parvoz qilib o'tkazadi.",
            "Yuqori tezlikdagi quvishdan so'ng gepardning tana harorati 41°C ga yetadi va u dam olmasdan ovqat yeyolmaydi.",
            "Ko'z ostidagi qora chiziqlar quyosh nurining ko'zga aks etishini to'sib, kunduzgi ovda durbin kabi yordam beradi."
        ]
    },
    {
        "name_uz": "Jayron (Qoraquyruq ohu)",
        "name_latin": "Gazella subgutturosa",
        "name_en": "Goitered Gazelle",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (Cho'l shuvog'i, sho'ra, saksovul novdalari)",
        "habitat": "Qizilqum cho'li, Ustyurt platosi, Qarshi va Qizilqum dashtlari",
        "lifespan": "8 - 12 yil",
        "speed": "65 km/soat",
        "weight": "20 - 35 kg",
        "description": "Jayron — O'zbekiston cho'llarining eng nozik, go'zal va tezkor antilopasi. O'zbek xalq og'zaki ijodida go'zallik va nafislik timsoli. Bo'ynidagi bo'rtib turuvchi hiqildoq ('bo'qoq') sababli 'bo'qoqli g'azol' deb ham ataladi. Ular suvsiz sho'r cho'llarda yashashga ajoyib tarzda moslashgan.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Buxoro viloyatidagi 'Jayron' ixtisoslashgan ekomarkazida ko'paytiriladi va muhofaza qilinadi.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif maqomda). Cho'llarning o'zlashtirilishi tufayli yashash joylari kamaygan.",
        "similar_species": "Sayg'oq (Saiga tatarica), Dzeren, Qoraquyruq kiyik",
        "differences": """1. SAYG'OQDAN FARQI: Jayronning burni nozik va oddiy ohu kabi tekis; sayg'oqda esa xartumsimon shishgan g'alati burun bo'ladi.
2. SHOX TUZILISHI: Jayronning faqat erkaklarida qora, lirasimon chiroyli shoxlar bo'ladi, urg'ochilari odatda shoxsiz; sayg'oqning shoxlari esa sarg'ish-shaffof va to'g'riroq.
3. DUM HARAKATI: Jayron chopganda qora kalta dumini tik ko'taradi (shuning uchun qoraquyruq deyiladi), oq tanasida bu uzoqdan signal mayoqchasi kabi ko'rinadi.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Xavf tug'ilganda erkak jayronning bo'ynidagi bo'rtmadan chiqadigan xirillagan ogohlantiruvchi tovush.",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Jayronlar haftalab suv ichmasdan yashashi mumkin, tanasi kerakli namlikni faqat tonggi shudring va cho'l o'tlaridan oladi.",
            "Ular sho'r dengiz yoki sho'rxok suvlarni ham ichishga qodir kam sonli sutemizuvchilardandir.",
            "Yangi tug'ilgan jayron bolasi hayotining ilk kunlarida qum ustida harakatsiz yotadi va yirtqichlar uni 1 metr masofadan ham payqay olmaydi."
        ]
    },
    {
        "name_uz": "Oddiy Bo'ri",
        "name_latin": "Canis lupus",
        "name_en": "Grey Wolf",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Tuyoqlilar, kiyiklar, quyonlar, kemiruvchilar)",
        "habitat": "Tog'lar, cho'llar, to'qaylar va ochiq dashtlar",
        "lifespan": "8 - 14 yil",
        "speed": "55 - 60 km/soat (uzoq masofaga charchamay yuguradi)",
        "weight": "30 - 60 kg",
        "description": "Bo'ri — itlar oilasining eng yirik, aqlli va ijtimoiy jihatdan mukammal tashkillashgan vakili. Ular qat'iy intizomli to'dalarda (alfa juftlik boshchiligida) yashaydilar. Bo'rilar nihoyatda chidamli bo'lib, o'ljasini kunlab ta'qib qilishga qodir. Tabiat sanitari sifatida kasal va zaif hayvonlarni yo'qotib, ekotizim muvozanatini saqlaydi.",
        "uz_red_book_status": "Kiritilmagan (Keng tarqalgan)",
        "uz_red_book_desc": "O'zbekiston hududida barqaror populyatsiyaga ega, ammo tog' va cho'l ekotizimlarida o'rganilmoqda.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Global miqyosda xavf ostida emas).",
        "similar_species": "Shoqol (Canis aureus), Chiyobori, Tulki (Vulpes vulpes), Uy iti",
        "differences": """1. SHOQOLDAN FARQI: Shoqol bo'ridan 2-3 barobar kichik (10-15 kg), dumi kaltaroq va asosan o'laksa va qoldiqlarni yeydi; bo'ri esa yirik va qudratli ovchi.
2. ITDAN FARQI: Bo'rining dumi doimo pastga osilib turadi (it kabi yuqoriga qayrilmaydi). Bo'rining ko'zlari doimo qiya va qahrli och sariq rangda bo'ladi.
3. IZLAR: Bo'rining izi to'g'ri bir chiziq bo'ylab cho'ziladi va oldingi ikki barmog'i itnikidan ancha oldinga chiqib turadi.""",
        "sound_file": "/static/audio/wolf_howl.mp3",
        "sound_description": "To'da a'zolarini chaqiruvchi va hududni belgilovchi cho'ziq, vahimali bo'ri uvillashi (howl).",
        "sound_type": "wolf",
        "image_url": "https://images.unsplash.com/photo-1564865878688-9a244444042a?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1590422749897-47036da0b0e0?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Bo'rilar to'xtamasdan bir kechada 70 kilometrgacha masofani yugurib o'ta oladilar.",
            "Uvillash orqali bo'rilar nafaqat o'z joyini bildiradi, balki to'daning qancha a'zosi borligi haqida ma'lumot uzatadi.",
            "Bo'rilar umrining oxirigacha bir juft bilan yashaydigan sadoqatli hayvonlardir."
        ]
    },
    {
        "name_uz": "Tyanshan Qo'ng'ir Ayig'i (Oq tirnoqli ayiq)",
        "name_latin": "Ursus arctos isabellinus",
        "name_en": "Tien Shan Brown Bear",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Hammaxo'r (O'tlar, yong'oqlar, mevalar, sug'urlar, ildizlar)",
        "habitat": "Tyan-Shan va Pomir-Oloy tog' tizmalari, archazorlar va alp o'tloqlari",
        "lifespan": "25 - 35 yil",
        "speed": "50 km/soat",
        "weight": "150 - 300 kg",
        "description": "Tyanshan qo'ng'ir ayig'i — oddiy qo'ng'ir ayiqning Markaziy Osiyo tog'larida yashovchi o'ziga xos kenja turi. Uning eng muhim belgisi — oldingi baquvvat panjalaridagi yorqin oq yoki sarg'ish rangli uzun tirnoqlaridir (shuning uchun xalq orasida 'oq tirnoqli ayiq' deb ataladi). Qish faslida qoyalar kovaklarida chuqur uyquga ketadi.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. Chotqol, Zomin, G'issar qo'riqxonalarida muhofaza qilinadi.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif maqomda). Yashash hududlarining bo'linishi xavf tug'dirmoqda.",
        "similar_species": "Sibir qo'ng'ir ayig'i, Gritsli ayiq, Oq ayiq (Ursus maritimus)",
        "differences": """1. SIBIR AYIG'IDAN FARQI: Tyanshan ayig'i ancha och rangli (sarg'ish-och malla) va bo'yi ixchamroq.
2. TIRNOQLARI: Uning tirnoqlari boshqa ayiqlarnikidan farqli ravishda och sarg'ish-oq rangda bo'lib, tog' toshlarini qazish va sug'ur inlarini buzish uchun moslashgan.
3. OZUQASI: Ratsionining 80% qismini o'simliklar (archamevalar, yong'oq, olma, o'tlar) tashkil qiladi, yirtqichlik kam qiladi.""",
        "sound_file": "/static/audio/bear_growl.mp3",
        "sound_description": "Ayiqning vahimali bo'g'iq o'kirishi va irillashi (growl & roar).",
        "sound_type": "bear",
        "image_url": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Tyanshan ayig'ining qishki uyqusi 4 oydan 6 oygacha davom etadi, bu davrda u hech narsa yemaydi va ichmaydi.",
            "Uning hid bilish qobiliyati eng yaxshi itlarnikidan 7 barobar o'tkirroqdir.",
            "Ayiqlar yong'oq va archa mevalarini o'rmon bo'ylab tarqatib, tog' o'rmonlarining tabiiy qayta tiklanishiga beqiyos hissa qo'shadilar."
        ]
    },
    {
        "name_uz": "Buxoro Bug'usi (Xongul)",
        "name_latin": "Cervus hanglu bactrianus",
        "name_en": "Bactrian Deer / Bukhara Deer",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (To'qay o'simliklari, qamish, jiyda, terak barglari)",
        "habitat": "Amudaryo va Zarafshon bo'yidagi to'qayzorlar",
        "lifespan": "12 - 16 yil",
        "speed": "50 km/soat",
        "weight": "160 - 240 kg",
        "description": "Buxoro bug'usi (Xongul — 'qirollik kiyigi') — Markaziy Osiyo to'qayzorlarining chinakam marvaridi. Uning hashamatli shoxlari 5 tagacha tarmoqlanadi. XX asr o'rtalarida daryo bo'yi to'qaylarining kesilishi va brakonyerlik natijasida deyarli butunlay yo'qolib ketish yoqasiga kelgan edi. Tabiatni muhofaza qilish choralari tufayli bugun ularning soni qayta tiklanmoqda.",
        "uz_red_book_status": "2 (Kamayib borayotgan, tiklanayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. 'Zarafshon' va 'Quyi Amudaryo' biosfera rezervatlarida saqlanmoqda.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xalqaro Qizil ro'yxatda soni ko'payganligi sababli xavf darajasi pasaytirilgan).",
        "similar_species": "Oddiy qizil bug'u (Cervus elaphus), Yelik (Capreolus), Kiyik",
        "differences": """1. YELIKDAN FARQI: Yelik ancha kichik (25-35 kg), shoxlari kalta va to'g'ri; Xongul esa bahaybat (200 kg dan ortiq) va shoxlari ulkan shoxlangan.
2. RANGI: Buxoro bug'usi kulrang-qumrang tusda bo'lib, to'qay qamishlari orasida ko'rinmaydi; Yevropa kiyiklari esa yorqin malla-qizil bo'ladi.
3. SUZISH MAHORATI: Buxoro bug'ulari jo'shqin Amudaryo to'lqinlarini bemalol suzib o'tib, orollar orasida ko'chib yuradi.""",
        "sound_file": "/static/audio/deer_bell.mp3",
        "sound_description": "Erkak bug'uning kuzgi to'y mavsumidagi jarangdor va haybatli na'rasi (deer roar/rutting call).",
        "sound_type": "deer",
        "image_url": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1484406566174-9da000fda645?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Erkak bug'ular har bahorda o'z shoxlarini tashlab yuboradi va yoz davomida yangi, yanada bahaybat shoxlar o'sib chiqadi.",
            "Xongul so'zi qadimiy fors-tojik tilidan tarjima qilinganda 'Qirollik daryosi ohu'si degan ma'noni anglatadi.",
            "Bug'u bolalari dastlabki oylarda oq xolli teriga ega bo'lib, oftob tushgan to'qay maysalariga mukammal singib ketadi."
        ]
    },
    {
        "name_uz": "Burgut (Oltin burgut)",
        "name_latin": "Aquila chrysaetos",
        "name_en": "Golden Eagle",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Yirtqich (Quyonlar, sug'urlar, tulkilar, toshbaqalar, yosh kiyiklar)",
        "habitat": "Tog' cho'qqilari, tik qoyalar, ochiq balandliklar va cho'l qirlari",
        "lifespan": "25 - 35 yil (tutqunlikda 50 yilgacha)",
        "speed": "240 - 320 km/soat (o'ljaga shung'ish parvozi)",
        "weight": "3.5 - 6.5 kg, qanot kengligi 2 - 2.4 metr",
        "description": "Oltin burgut — qushlar olamining eng qudratli, jasur va tezyurar qanotli yirtqichlaridan biri. Boshining orqasidagi oltinrang patlari unga xos mahobat beradi. O'ljasiga sho'ng'igan paytda poyezd tezligidan ham tezroq (320 km/soat) uchadi. O'zbekistonda qadimdan ovchilik san'atida (sayyodlik) burgut boqish an'anasi mavjud.",
        "uz_red_book_status": "2 (Zaif, kamyob tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Tog' va adir hududlarida uya qurishi qat'iy muhofaza qilinadi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xalqaro ro'yxatda barqaror).",
        "similar_species": "Bolg'atuxum (Qoraqush), Qirg'iy, Lochin (Falco peregrinus), Tasqara",
        "differences": """1. LOCHINDAN FARQI: Lochin ixchamroq, qanotlari o'tkir uchli va asosan osmondagi uchar qushlarni tutadi; Burgut esa bahaybat va yer ustidagi yirik sutemizuvchilarni (quyon, hatto tulki va kiyikni) ovlaydi.
2. PANJA KUCHI: Burgut panjasining qisish kuchi inson qo'lidan 10 barobar kuchliroq bo'lib, o'ljasining suyaklarini osongina sindiradi.
3. KO'RISH QUDRATI: Burgut 3-4 kilometr balandlikdan turib o'tlar orasidagi mitti tovushqonni aniq ko'ra oladi.""",
        "sound_file": "/static/audio/eagle_cry.mp3",
        "sound_description": "Burgutning baland tog'lar uzra aks-sado beruvchi o'tkir va jarangdor qiyqirishi (eagle screech).",
        "sound_type": "eagle",
        "image_url": "https://images.unsplash.com/photo-1611689342806-0863700ce8e4?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1549608276-5786777e6587?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Burgut ko'zlari bir vaqtning o'zida ham to'g'riga, ham yon tomonga qaray oladi va odam ilg'amaydigan ultrabinafsha nurlarni ko'radi.",
            "Burgutlar o'z juftiga butun umr sodiq qolishadi va bir xil inni o'nlab yillar davomida ta'mirlab ishlatishadi.",
            "Qadimda O'zbekiston va Markaziy Osiyo ovchilari bitta burgut bilan butun qishloqni go'sht va qimmatbaho mo'yna bilan ta'minlay olganlar."
        ]
    },
    {
        "name_uz": "Delfin (Afalina)",
        "name_latin": "Tursiops truncatus",
        "name_en": "Bottlenose Dolphin",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Baliqlar, kalmarlar, qisqichbaqasimonlar)",
        "habitat": "Iliq dengizlar va okeanlar, qirg'oq zonalari",
        "lifespan": "30 - 50 yil",
        "speed": "35 km/soat",
        "weight": "150 - 300 kg, uzunligi 2 - 3.5 metr",
        "description": "Delfin — suv muhitida yashaydigan, ammo baliq bo'lmagan, yuksak intellektli sutemizuvchi. Ular o'pka orqali atmosfera havosidan nafas oladi, bolalarini sut bilan boqadi va ultratovushli exolokatsiya yordamida suv ostida atrofdagi barcha narsani 'ko'radi'.",
        "uz_red_book_status": "Kiritilmagan (Dengiz turi)",
        "uz_red_book_desc": "O'zbekistonda dengiz yo'qligi sababli O'zbekiston Qizil kitobida yo'q, xalqaro ahamiyatga ega tur.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xalqaro Qizil kitobda, ayrim mahalliy populyatsiyalari esa xavf ostida).",
        "similar_species": "Akula (Shark - Baliq), Kosatka (Orca), Tyulen",
        "differences": """1. BALIQLAR VA AKULALARDAN FARQI: Akula baliq bo'lib jabra bilan nafas oladi va sovuqqonli; delfin esa issiqqonli sutemizuvchi bo'lib, o'pka bilan nafas oladi va bolalaydi.
2. DUMNING HARAKATI: Baliqlarning dumi chapga-o'ngga vertikal harakat qiladi; delfinlarning dumi esa faqat yuqoriga-pastga gorizontal harakatlanadi.
3. AQLIY DARAJASI: Delfinlar ko'zguda o'zini taniydi, har biriga xos 'ism' hushtagi bor va murakkab his-tuyg'ularga ega.""",
        "sound_file": "/static/audio/dolphin_click.mp3",
        "sound_description": "Delfinlarning exolokatsion chertishlari (clicks) va o'zaro suhbat hushtaklari (whistles).",
        "sound_type": "dolphin",
        "image_url": "https://images.unsplash.com/photo-1607153333879-c1a05d2586b8?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1570481662006-a3a1374699e8?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Delfinlar uxlayotganda miyasining faqat bitta yarim shari dam oladi, ikkinchi yarmi esa nafas olishni va xavfni nazorat qilib turadi.",
            "Har bir delfinning o'ziga xos individual hushtak-ovozli 'ismi' bo'lib, to'dadagi boshqa delfinlar uni shu ism bilan chaqiradi.",
            "Ular cho'kayotgan odamlarni suv yuzasiga chiqarib qutqargan ko'plab voqealar fanga ma'lum."
        ]
    },
    {
        "name_uz": "Sayg'oq (Sayga kiyigi)",
        "name_latin": "Saiga tatarica",
        "name_en": "Saiga Antelope",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (Sho'ra, shuvoq, lola, cho'l efemerlari)",
        "habitat": "Ustyurt platosi, Qoraqalpog'iston va Qizilqum cho'llari",
        "lifespan": "6 - 10 yil",
        "speed": "75 - 80 km/soat (cho'lda uzoq masofalarga charchamay chopadi)",
        "weight": "30 - 50 kg",
        "description": "Sayg'oq — qadimiy muzlik davridan (mamontlar davridan) omon qolgan noyob cho'l antilopasi. Uning eng hayratlanarli belgisi — pastga osilib turadigan egiluvchan, shishgan xartumsimon tumshug'idir. Ushbu noyob xartum yozda cho'l changini filtrlab tozalaydi, qishda esa muzdek havoni o'pkaga yetguncha isitib beradi. Ustyurt kengliklarida ulkan podalar bo'lib ko'chib yuradi.",
        "uz_red_book_status": "1 (Yo'qolib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. Shoxlari uchun noqonuniy ov va chegara to'siqlari tufayli soni qattiq kamaygan, davlat muhofazasiga olingan.",
        "iucn_status": "CR",
        "iucn_desc": "Critically Endangered (Kritik xavf ostida). Jahon miqyosida qat'iy muhofaza etiladigan relikt tur.",
        "similar_species": "Jayron (Gazella subgutturosa), Dzeren, Yelik",
        "differences": """1. JAYRONDAN FARQI: Sayg'oqning pastga bukilgan shishgan yumshoq xartumi bor; jayronda esa nozik va to'g'ri ohu burni bo'ladi.
2. SHOXLARI: Sayg'oq shoxlari sarg'ish-shaffof, qator halqali va lirasimon; jayron shoxlari esa to'q qora va orqaga qayrilgan bo'ladi.
3. YURISH USLUBI: Sayg'oq boshini pastga egib 'yo'rg'a' usulida sakramay tezoqar poyezddek chopadi; jayron esa baland sakrab chaqqon yo'nalish o'zgartiradi.""",
        "sound_file": "/static/audio/deer_bell.mp3",
        "sound_description": "Sayg'oqning xartumsimon burni orqali chiqaradigan o'ziga xos xirillagan chaqiruv tovushi.",
        "sound_type": "deer",
        "image_url": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Sayg'oqlar mamontlar va junli karkidonlar bilan bir davrda yashagan bo'lib, o'sha muzlik davridan omon chiqqan kam sonli relikt sutemizuvchilardandir.",
            "Ularning xartumsimon burni ichidagi murakkab shilliq qavat changni to'liq ushlab qoluvchi mukammal respirator filtrlash tizimidir.",
            "Urg'ochi sayg'oqlar deyarli har doim egizak bolalaydi va butun poda bir haftaning ichida yalpi bolalab ulguradi."
        ]
    },
    {
        "name_uz": "Amur yo'lbarsi (Sibir yo'lbarsi)",
        "name_latin": "Panthera tigris altaica",
        "name_en": "Amur Tiger / Siberian Tiger",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Yovvoyi to'ng'iz, bug'u, yelik, ayiqlar)",
        "habitat": "Sharqiy Sibir, Tayga ignabargli va aralash o'rmonlari",
        "lifespan": "15 - 20 yil",
        "speed": "60 km/soat",
        "weight": "180 - 300 kg (ba'zan 320 kg gacha)",
        "description": "Amur yo'lbarsi — sayyoramizdagi barcha mushuksimonlarning eng yirigi va qudratlisi. Qalin qor va -40°C gacha bo'lgan qahraton sovuqda yashashga to'liq moslashgan: uning qorni ostida 5 sm qalinlikdagi yog' qatlami va qalin ipakdek qishki mo'ynasi mavjud. Suvda suzishni nihoyatda yaxshi ko'radi.",
        "uz_red_book_status": "0 (O'tmishdoshi Turon yo'lbarsi qirilib ketgan)",
        "uz_red_book_desc": "O'zbekistonning Amudaryo va Sirdaryo to'qaylarida o'tmishda yashagan Turon yo'lbarsi (Panthera tigris virgata) Amur yo'lbarsining eng yaqin genetik egizagi bo'lgan.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered (Yo'qolib ketish xavfi ostida). Tabiatda 550 tagina saqlanib qolgan.",
        "similar_species": "Bengal yo'lbarsi, Sher (Panthera leo), Qor qoploni",
        "differences": """1. SHERDAN FARQI: Sher savanna praydida to'da bo'lib yashaydi; yo'lbars mutlaq yolg'iz ovchi hisoblanadi. Yo'lbars suvda zo'r suzadi va cho'milishni yaxshi ko'radi, sher esa suvdan qochadi.
2. BENGAL YO'LBARSIDAN FARQI: Amur yo'lbarsi Bengal yo'lbarsiga nisbatan yirikroq, juni ochroq sarg'ish va ancha qalin, qornida qalin yog' qatlami bor.
3. MO'YNASI: Hech qaysi ikki yo'lbarsning qora chiziqlari bir xil bo'lmaydi — bu xuddi inson barmoq izi kabi betakrordir.""",
        "sound_file": "/static/audio/lion_roar.mp3",
        "sound_description": "Yo'lbarsning o'rmon bo'ylab vahimali gulduragan past chastotali o'kirishi.",
        "sound_type": "lion",
        "image_url": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1549480017-d76466a4b7e8?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Yo'lbarsning nafaqat yungi, balki terisining o'zi ham qora yo'l-yo'l chiziqlarga ega.",
            "Yo'lbars bir sakrashda 10 metr uzunlikka va 3 metr balandlikka sakray oladi.",
            "Tungi ko'rish qobiliyati odamnikidan 6 barobar kuchliroq bo'lib, o'ljasini qorong'uda bexato mo'ljallaydi."
        ]
    },
    {
        "name_uz": "Afrika fili",
        "name_latin": "Loxodonta africana",
        "name_en": "African Bush Elephant",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (O't-o'lanlar, daraxt po'stlog'i, shoxlar, mevalar - kuniga 180 kg)",
        "habitat": "Afrika savannalari, daryo vodiylari va siyrak o'rmonlar",
        "lifespan": "60 - 70 yil",
        "speed": "40 km/soat",
        "weight": "4 000 - 7 000 kg (4 - 7 tonna), bo'yi 3.5 - 4 metr",
        "description": "Afrika fili — Yer yuzida quruqlikda yashovchi eng bahaybat va yuksak aql-idrokli sutemizuvchi jonivor. Uning xartumi 40 000 dan ortiq mushak tolasidan iborat bo'lib, ham mitti ignani yerdan terish, ham 300 kilogrammlik yog'och xodani ko'tarishga qodir. Bahaybat quloqlari orqali tana haroratini jaziramada sovutadi.",
        "uz_red_book_status": "Kiritilmagan (Afrika endemigi)",
        "uz_red_book_desc": "O'zbekiston tabiatida uchramaydi, xalqaro ahamiyatga ega quruqlik giganti.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered (Yo'qolib ketish xavfi ostida). Fil suyagi uchun brakonyerlik va yashash maydonlarining qisqarishi xavf tug'dirmoqda.",
        "similar_species": "Osiyo fili (Elephas maximus), Mamont (qirilib ketgan)",
        "differences": """1. OSIYO FILIDAN FARQI: Afrika filining quloqlari ulkan bo'lib Afrika xaritasiga o'xshaydi; Osiyo filining quloqlari ancha kichikroq.
2. XARTUM UCHI: Afrika fili xartumining uchida 2 ta harakatchan ushlagich 'barmoq' bor; Osiyo filida esa faqat 1 ta yuqori 'barmoq' mavjud.
3. FIL TISHLARI: Afrika filida erkak va urg'ochilarining ikkalasida ham uzun fil tishlari (qalqon tish) bo'ladi; Osiyo filida esa urg'ochilarida tish deyarli bo'lmaydi.""",
        "sound_file": "/static/audio/bear_growl.mp3",
        "sound_description": "Filning xartum orqali chiqaradigan jarangdor karnaysimon hayqirig'i va infratovushlari.",
        "sound_type": "bear",
        "image_url": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1581852017103-68ac65503977?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Fillarning homiladorlik davri deyarli 22 oy (deyarli 2 yil) davom etadi — bu hayvonot olamida eng uzun davr.",
            "Ular inson qulog'i ilg'amaydigan seysmik to'lqinlar va infratovushlar orqali oyoqlari bilan 10 km uzoqlikdagi xabarlarni eshitishadi.",
            "Fillar o'z yaqinlari o'lganda motam tutuvchi va ko'zguda o'z aksini taniydigan yuksak hissiyotli jonivorlardir."
        ]
    },
    {
        "name_uz": "Jirafa",
        "name_latin": "Giraffa camelopardalis",
        "name_en": "Giraffe",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (Akatsiya barglari, yosh novdalar, mevalar)",
        "habitat": "Afrika savannalari va ochiq butazorlar",
        "lifespan": "25 yil",
        "speed": "55 km/soat",
        "weight": "800 - 1 500 kg, bo'yi 5 - 6 metr",
        "description": "Jirafa — dunyodagi eng baland sutemizuvchi hayvon. Uning bo'yi 6 metrgacha yetadi, shundan bo'yin uzunligining o'zi 2 metrni tashkil qiladi. Qiziq tomoni shundaki, ularning bo'ynida ham xuddi inson yoki sichqon kabi atigi 7 dona umurtqa suyagi bor. Uning 45-50 sm lik to'q binafsharang tili tikanli akatsiya barglarini bemalol uzib olish imkonini beradi.",
        "uz_red_book_status": "Kiritilmagan (Eksotik tur)",
        "uz_red_book_desc": "O'zbekiston tabiatida uchramaydi, Afrika savannalarining ramziy go'zali.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). So'nggi 30 yilda soni 40% ga kamaygan.",
        "similar_species": "Okapi (Okapia johnstoni), Katta antilopalar",
        "differences": """1. OKAPIDAN FARQI: Okapi jirafaning eng yaqin qarindoshi bo'lsa-da, bo'yni qisqa, o'rmonda yashaydi va tanasining orqa tomonida zebra kabi qora-oq chiziqlar bor.
2. TILI: Jirafaning tili nihoyatda uzun (yarim metr) va quyosh nurlaridan kuymasligi uchun to'q binafsharang melanin pigmentiga ega.
3. UYQU: Jirafalar kuniga atigi 30 daqiqadan 2 soatgacha tik turgan holda qisqa-qisqa mizg'ib uxlaydilar.""",
        "sound_file": "/static/audio/deer_bell.mp3",
        "sound_description": "Jirafalar deyarli jim yuradi, ammo tunda o'zaro past ohangli g'o'ng'illash (humming) tovushlari chiqaradi.",
        "sound_type": "deer",
        "image_url": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1574870111867-089730e5a72b?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Jirafaning yuragi 11 kg og'irlikka ega va 2 metr balandlikdagi miyaga qon yetkazib berish uchun odamnikidan 2 barobar yuqori qon bosimini hosil qiladi.",
            "Har bir jirafaning tanasidagi dog'lar naqshi xuddi inson barmoq izi kabi mutlaqo individual va betakrordir.",
            "Yangi tug'ilgan jirafa bolasi tug'ilish payti 2 metr balandlikdan yerga tushadi va yarim soatdan so'ng oyoqqa turib yuguradi."
        ]
    },
    {
        "name_uz": "Ko'k kit (Moviy kit)",
        "name_latin": "Balaenoptera musculus",
        "name_en": "Blue Whale",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Planktonxo'r (Asosan mayda qisqichbaqasimon krillar - kuniga 4 tonna)",
        "habitat": "Dunyo okeanlari (Arktikadan Antarktikagacha bo'lgan ochiq suvlar)",
        "lifespan": "80 - 90 yil (ba'zida 110 yilgacha)",
        "speed": "30 - 50 km/soat",
        "weight": "150 - 200 tonna (uzunligi 30 - 33 metr)",
        "description": "Ko'k kit — Yer sayyorasida qachonlardir yashagan barcha mavjudotlar (hatto eng bahaybat dinozavrlar) ichida ham eng ulkan va eng og'ir jonzotdir. Uning tili bitta filning og'irligiga (3 tonna), yuragi esa kichik avtomobil hajmiga teng. Baliq emas, balki haqiqiy sutemizuvchi bo'lib, o'pka bilan nafas oladi va bolalarini kuniga yuzlab litr yog'li sut bilan boqadi.",
        "uz_red_book_status": "Kiritilmagan (Okean giganti)",
        "uz_red_book_desc": "O'zbekistonda dengiz yo'q, xalqaro miqyosda qat'iy qo'riqlanadigan global gigant.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered (Yo'qolib ketish arafasida). XX asrdagi sanoat kit ovi sababli soni keskin kamayib ketgan.",
        "similar_species": "Finval, Bukri kit (Humpback whale), Qashalot (Sperm whale)",
        "differences": """1. QASHALOTDAN FARQI: Qashalot yirik tishli yirtqich kit bo'lib, chuqur suvda kalmarlarni ovlaydi; Ko'k kitda esa tish o'rniga elastik kit mo'ylovi bor va faqat krill filtrlaydi.
2. VAZNI: Ko'k kit Yer yuzidagi eng og'ir jonzot bo'lib (180 tonnagacha), boshqa hech qaysi sutemizuvchi uning vazniga teng kela olmaydi.
3. FAVVORA: Suv yuzasiga chiqqanda o'pkasidan otilib chiquvchi suv favvorasi 10-12 metr balandlikkacha ko'tariladi.""",
        "sound_file": "/static/audio/dolphin_click.mp3",
        "sound_description": "Ko'k kitning okean tubida minglab kilometr masofaga yetuvchi eng qudratli past chastotali infratovush qo'shiqlari.",
        "sound_type": "dolphin",
        "image_url": "https://images.unsplash.com/photo-1568430462989-44163eb1752f?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Ko'k kitning asosiy qon tomirlari shunchalik kengki, ularning ichidan odam suzib o'tishi mumkin.",
            "Ko'k kit bolasi tug'ilganda uzunligi 7-8 metr, og'irligi 3 tonna bo'ladi va har kuni 90 kg ga semiradi.",
            "Uning yuragi daqiqasiga atigi 4-8 marta uradi, lekin chiqargan tovushi 188 desibelga yetib, reaktiv samolyot shovqinidan ham kuchliroqdir."
        ]
    },
    {
        "name_uz": "Oq ayiq (Qutb ayig'i)",
        "name_latin": "Ursus maritimus",
        "name_en": "Polar Bear",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Halqali tyulenlar, dengiz quyonlari, morjlar)",
        "habitat": "Arktika muzliklari, suzuvchi muz maydonlari va Shimoliy qutb orollari",
        "lifespan": "25 - 30 yil",
        "speed": "40 km/soat (quruqlikda), 10 km/soat (muzdek suvda uzoq suzish)",
        "weight": "400 - 800 kg (erkagi), 200 - 350 kg (urg'ochisi)",
        "description": "Oq ayiq — Shimoliy qutbning mutlaq hukmdori va quruqlikdagi eng yirik yirtqich ayiq turi. U qattiq Arktika sovuqlarida yashash uchun ajoyib biologik tuzilishga ega: uning terisi qop-qora bo'lib, quyosh issiqligini to'liq o'ziga yutadi; yungi esa aslida oq emas, balki nurni qaytaruvchi shaffof ichi bo'sh naychalardan iborat. Muzli suvlarda to'xtovsiz 100 kilometrlab masofaga suza oladi.",
        "uz_red_book_status": "Kiritilmagan (Arktika turi)",
        "uz_red_book_desc": "O'zbekiston tabiatida uchramaydi, global iqlim o'zgarishi indikatori.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Muzliklarning erishi va yashash hududining yo'qolishi sababli xavf ostida.",
        "similar_species": "Qo'ng'ir ayiq (Ursus arctos), Gritsli ayiq, Qora ayiq (Baribal)",
        "differences": """1. QO'NG'IR AYIQDAN FARQI: Oq ayiq deyarli 100% go'sht va yog' bilan oziqlanuvchi yirtqich; qo'ng'ir ayiq esa aralash oziqlanuvchi bo'lib rezavorlar va o'tlarni ko'p yeydi.
2. TANA TUZILISHI: Oq ayiqning bo'yni uzunroq, bosimi cho'ziqroq va panjalarining osti muzda sirpanmaslik uchun jun bilan qoplangan.
3. SUZISH MAHORATI: Oq ayiq dengiz sutemizuvchisi hisoblanadi va suv ostida 2 daqiqadan ko'proq nafas olmasdan sho'ng'iy oladi.""",
        "sound_file": "/static/audio/bear_growl.mp3",
        "sound_description": "Oq ayiqning qor bo'ronlari uzra eshitiladigan chuqur vahimali g'o'ldirashi va pishqirishi.",
        "sound_type": "bear",
        "image_url": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Oq ayiqning terisi qop-qora, tili esa to'q ko'k rangda bo'ladi; yungi esa optik tolaga o'xshab quyosh nurini to'g'ridan-to'g'ri qora teriga uzatadi.",
            "Ular to'xtamasdan ketma-ket 9-10 kun davomida muzli okean suvlarida yuzlab kilometr suzib yurishga qodir.",
            "Oq ayiqning hid bilish qobiliyati 1 metr qalinlikdagi muz tagida yashiringan tyulenni 30 km uzoqlikdan aniqlay oladi."
        ]
    },
    {
        "name_uz": "Katta panda",
        "name_latin": "Ailuropoda melanoleuca",
        "name_en": "Giant Panda",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (Ratsionining 99% qismi faqat bambuk novdalari va barglari)",
        "habitat": "Xitoyning Sichuan tog'li tumanlaridagi qalin bambukzorlar",
        "lifespan": "20 yil (tabiatda), 30 yilgacha (qo'riqxonalarda)",
        "speed": "20 km/soat",
        "weight": "80 - 125 kg",
        "description": "Katta panda — o'zining qora-oq rangli yoqimli ko'rinishi va xotirjam fe'l-atvori bilan butun jahon mehrini qozongan noyob ayiq turi. Yirtqichlar turkumiga mansub bo'lsa-da, evolyutsiya davomida faqat bambuk bilan oziqlanishga o'tgan. Bambukning ozuqaviy kuchi past bo'lgani sababli, panda kunining 12-16 soatini to'xtovsiz ovqatlanish bilan o'tkazadi va kuniga 15-30 kg bambuk yeydi.",
        "uz_red_book_status": "Kiritilmagan (Xitoy endemigi)",
        "uz_red_book_desc": "Butunjahon yovvoyi tabiat fondi (WWF) ramzi hisoblanadi.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif maqomda, qat'iy muhofaza choralari tufayli yo'qolib ketish xavfi 'EN' dan 'VU' ga tushirilgan).",
        "similar_species": "Qizil panda (Ailurus fulgens), Qo'ng'ir ayiq, Koala",
        "differences": """1. QIZIL PANDADAN FARQI: Qizil panda mushukdek kichik (4-6 kg), yenotsimonlar oilasiga yaqin va dumi uzun paxmoq; Katta panda esa haqiqiy yirik bahaybat ayiqdir.
2. OLTINCHI BARMOQ: Katta pandaning oldingi panjalarida 6 ta barmoq bor — 6-barmoq bu bilak suyagining maxsus o'simtasi bo'lib, bambuk shoxlarini mahkam ushlab turishga xizmat qiladi.
3. QISHKI UYQU: Boshqa ayiqlardan farqli ravishda panda qishki uyquga ketmaydi, chunki uning ozuqasi yil bo'yi o'zgarmaydi.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Pandalar ayiq kabi o'kirmaydi, balki qo'zichoqdek mayin ma'raydi va chuldiragan tovushlar chiqaradi.",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1527118732049-c88155f2107c?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Panda bolasi tug'ilganda atigi 100 gramm bo'lib, onasidan 900 barobar kichikroq bo'ladi — bu barcha sutemizuvchilar ichidagi eng katta vazn farqlaridan biridir.",
            "Panda kuniga 40 martagacha najas chiqaradi, chunki bambuk tolasi uning ichagidan o'ta tez harakatlanadi.",
            "Xitoyda pandani noqonuniy ovlagan yoki o'ldirgan kimsaga qonun bo'yicha umrbod qamoq jazosi beriladi."
        ]
    },
    {
        "name_uz": "Old Osiyo qoploni (Leopard)",
        "name_latin": "Panthera pardus ciscaucasica",
        "name_en": "Persian Leopard / Caucasian Leopard",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Tog' echkilari, jayronlar, yovvoyi to'ng'izlar, quyonlar)",
        "habitat": "Janubiy O'zbekistonning baland qoyali tog' tizmalari (Ko'hitang, Bobotog', Surxondaryo)",
        "lifespan": "12 - 17 yil",
        "speed": "60 km/soat",
        "weight": "50 - 80 kg",
        "description": "Old Osiyo qoploni — dunyodagi eng yirik va go'zal leopard kenja turlaridan biri. U mushuksimonlar ichida eng chaqqon alpinist bo'lib, o'z og'irligidan 2 barobar og'irroq o'ljasini (tog' echkisini) daraxt tepasiga yoki tik qoyalarga olib chiqib yashira oladi. Tanasidagi halqasimon 'rozetka' dog'lari toshloq va butazor tog'larda uni ko'z ilg'amas qiladi.",
        "uz_red_book_status": "1 (Yo'qolib ketish arafasidagi o'ta kamyob tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. Surxondaryo davlat qo'riqxonasi va Ko'hitang tog'larida bir necha donasi qayd etilgan.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered (Xavf ostida). Markaziy Osiyo bo'ylab umumiy soni 800-1000 donadan oshmaydi.",
        "similar_species": "Gepard (Acinonyx jubatus), Qor qoploni (Panthera uncia), Yaguar",
        "differences": """1. GEPARDDAN FARQI: Leopard tanasida rozetka (o'rtasi bo'sh doiracha) dog'lar bor va yuzida ko'z yoshi chizig'i yo'q; gepardda esa oddiy to'liq qora nuqtalar va qora ko'z yoshi chizig'i bo'ladi.
2. TIRNOQLAR: Leopardning tirnoqlari to'liq ichkariga tortiladi va daraxtga erkin tirmashadi; gepardniki esa tortilmaydi.
3. QOR QOPLONIDAN FARQI: Qor qoplonining dumi ancha qalin, yungi och kulrang va faqat qorli tog' cho'qqilarida yashaydi; leopard esa sarg'ish rangda bo'ladi.""",
        "sound_file": "/static/audio/lion_roar.mp3",
        "sound_description": "Qoplonning yo'talga o'xshash qisqa va qat'iy irillashi (sawing rasp call).",
        "sound_type": "lion",
        "image_url": "https://images.unsplash.com/photo-1575550959106-5a7defe28b56?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1456926631375-92c8ce872def?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Leopardlar o'z o'ljasini yerda gienalar yoki sherlar tortib olmasligi uchun daraxt shoxlariga olib chiqib osib qo'yishadi.",
            "Ular suv ichmasdan o'lja qoni va go'shtidagi namlik hisobiga oylarcha yashashi mumkin.",
            "Bir sakrashda 6 metr uzunlikka va 3 metr balandlikka sakray oladi."
        ]
    },
    {
        "name_uz": "Pushti saqoqqush (Pelikan)",
        "name_latin": "Pelecanus onocrotalus",
        "name_en": "Great White Pelican",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Baliqxo'r (Zog'ora, karp, oq amur, leshch - kuniga 1.5-2 kg)",
        "habitat": "Amudaryo va Sirdaryo deltalari, Aydarko'l, Sudoche va Arnasoy ko'llar tizimi",
        "lifespan": "20 - 30 yil",
        "speed": "50 km/soat (havoda silliq parvoz)",
        "weight": "9 - 15 kg, qanotlari yoyilganda 2.8 - 3.2 metr",
        "description": "Pushti saqoqqush — O'zbekiston suv havzalaridagi eng ulkan va hayratlanarli qushlardan biri. Uning pastki jag'iga birikkan bahaybat elastik charm xaltasi 12-14 litrgacha suv va baliqni sig'dira oladi. Saqoqqushlar jamoa bo'lib ov qiladi: bir necha qush suv yuzida qanotlarini qattiq qoqib, baliqlarni sayozlikka haydaydi va birgalikda cho'michdek og'zi bilan suzib oladi.",
        "uz_red_book_status": "2 (Kamayib borayotgan, zaif tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Suv havzalarining qurishi va qamishzorlarning yoqilishi tufayli uya qurish joylari kamaygan.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Dunyo miqyosida barqaror, ammo O'zbekiston oraliq ko'chish hududida muhofazaga muhtoj).",
        "similar_species": "Jingalak saqoqqush (Pelecanus crispus), Oq laylak, Qoravoy",
        "differences": """1. JINGALAK SAQOQUSHDAN FARQI: Pushti saqoqqushning patlari pushti tusli oq va boshidagi kokili qisqa; jingalak saqoqqushning pati kulrang-oq, boshida esa jingalak patlar to'dasi bor.
2. OVLASH USULI: Saqoqqush suv ostiga chuqur sho'ng'imaydi, balki suv yuzasidan boshini tiqib baliq tutadi.
3. TUMSHUQ XALTASI: Teri xaltasi faqat baliq tutish uchun to'r vazifasini o'taydi, u yerda baliq saqlanmaydi — suvni chiqarib tashlab darhol yutib yuboradi.""",
        "sound_file": "/static/audio/swallow_song.mp3",
        "sound_description": "Saqoqqushlar uya qurgan koloniyalarida past xirillagan g'o'ldirash tovushlarini chiqaradi.",
        "sound_type": "swallow",
        "image_url": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1550853024-fae8cd4be477?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Saqoqqushning tumshuq xaltasiga uning oshqozonidan 3 barobar ko'proq (12 litrgacha) suv sig'adi.",
            "Ular baland havoda termal havo oqimlaridan foydalanib, 3 000 metr balandlikkacha ko'tarilib parvoz qila oladi.",
            "Urug'lanish davrida ularning peshonasida maxsus shish paydo bo'ladi va patlari yanada yorqin pushti rangga kiradi."
        ]
    },
    {
        "name_uz": "Pushti flamingo (Qizilg'oz)",
        "name_latin": "Phoenicopterus roseus",
        "name_en": "Greater Flamingo",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Sho'rxok suv o'tlari, mikroskopik qisqichbaqasimonlar (Artemia salina), hasharot lichinkalari",
        "habitat": "Sho'r ko'llar, dengiz qo'ltiqlari (Dengizko'l, Sudoche, Orolbo'yi suvliklari)",
        "lifespan": "30 - 40 yil",
        "speed": "50 - 60 km/soat",
        "weight": "2 - 4 kg, bo'yi 1.2 - 1.45 metr",
        "description": "Pushti flamingo (Qizilg'oz) — O'zbekiston tabiatining eng nafis va maftunkor qushlaridan biri. Uzun nozik oyoqlari va o'rtasidan tirsakdek bukilgan maxsus tumshug'i bor. Ular boshini teskari (pastga qaratib) suvga tiqib, o'ziga xos taroqsimon filtrlari yordamida loydan qisqichbaqachalarni suzib yeydi. Uning mashhur pushti rangi aynan u yeydigan qizil qisqichbaqalar tarkibidagi karotinoid pigmenti sabablidir.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Buxoro viloyatidagi 'Dengizko'l' Ramsar xalqaro ahamiyatga ega suv-botqoqlik hududida ko'payadi va qishlaydi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Dunyo miqyosida barqaror, ammo mahalliy sho'rxok ko'llarda qat'iy muhofaza qilinadi).",
        "similar_species": "Turna (Grus grus), Qizil flamingo, Oq laylak",
        "differences": """1. TURNA VA LAYLAKDAN FARQI: Turnaning tumshug'i to'g'ri nayzasimon; flamingoning tumshug'i esa o'rtasidan tirsakdek pastga keskin bukilgan.
2. FILTRLASH MOSLAMASI: Flamingolar ozuqani boshini 180 daraja teskari burib suv tubidan filtrlaydi.
3. RANGI: Yosh jo'jalari kulrang-oq bo'lib tug'iladi, faqat 2-3 yoshdan keyin karotinoidga boy ovqat yeb pushti rang oladi.""",
        "sound_file": "/static/audio/swallow_song.mp3",
        "sound_description": "Flamingolar parvoz paytida g'ozga o'xshash jarangdor g'aqillash tovushlarini chiqaradi.",
        "sound_type": "swallow",
        "image_url": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1497206365907-f5e630693df0?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Flamingolar ko'pincha bitta oyoqda turishadi — bu ularning tana issiqligini tejashiga yordam beradi.",
            "Ota-ona flamingolar o'z jo'jalarini qizil rangli 'qush suti' (bo'qoq suyuqligi) bilan boqishadi.",
            "Ular o'ta sho'r va ishqorli suv havzalarida yashay oladi, bu suvlarda boshqa hayvonlar hatto zaharli kuyish oladi."
        ]
    },
    {
        "name_uz": "Yo'rg'a tuvaloq (Yo'rg'atoq)",
        "name_latin": "Chlamydotis macqueenii",
        "name_en": "Macqueen's Bustard / Asian Houbara",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Hasharotlar (Chigirtkalar, qo'ng'izlar), cho'l o'simliklarining shira barglari va urug'lari",
        "habitat": "Qizilqum cho'li, Ustyurt platosi, sho'rxok va qumloq dashtlar",
        "lifespan": "12 - 15 yil",
        "speed": "40 km/soat (yerda tez yugurish), 60 km/soat (parvoz)",
        "weight": "1.2 - 2.5 kg",
        "description": "Yo'rg'a tuvaloq — cho'l hayotiga mukammal moslashgan, nihoyatda ehtiyotkor qush. Xavf sezganda osmonga uchishdan ko'ra, cho'l butalari orasiga pusib yerga yopishib oladi yoki chaqqon yo'rg'alab qochadi. Erkak yo'rg'a tuvaloqning bahorgi to'y raqsi tabiat mo''jizasidir: u boshidagi va bo'ynidagi oppoq hashamatli patlarini shishirib, o'z atrofida aylanib raqsga tushadi.",
        "uz_red_book_status": "1 (Yo'qolib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. Navoiy va Buxoro maxsus pitomniklarida ko'paytirilib yovvoyi tabiatga qo'yib yuborilmoqda.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Noqonuniy ov va cho'llarning o'zlashtirilishi tufayli qattiq muhofazada.",
        "similar_species": "Katta tuvaloq (Otis tarda), Bezgak tuvaloq (Tetrax tetrax)",
        "differences": """1. KATTA TUVALOQDAN FARQI: Katta tuvaloq bahaybat (16 kg gacha yetuvchi dunyodagi eng og'ir uchar qush); yo'rg'a tuvaloq esa ixcham (2 kg gacha) va bo'ynida qora-oq yoqa patlari bor.
2. NIQOBLANISH: Qum rangli patlari tufayli yarim metr naridagi qumda o'tirgan qushni ham payqash imkonsiz.
3. QOCHISH USLUBI: To'g'ri chiziq bo'ylab yugurmaydi, balki to'satdan yo'nalishini burib qum barxanlari ortiga berkinadi.""",
        "sound_file": "/static/audio/swallow_song.mp3",
        "sound_description": "Erkak tuvaloqning to'y raqsi paytida chiqaradigan bo'g'iq gumburlash va qanot shovqini.",
        "sound_type": "swallow",
        "image_url": "https://images.unsplash.com/photo-1579202673506-ca3ce28943ef?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1549608276-5786777e6587?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Yo'rg'a tuvaloq deyarli suv ichmaydi — barcha kerakli suyuqlikni oziqlanadigan hasharotlar va cho'l o'simliklaridan oladi.",
            "Yirtqich qirg'iy hujum qilganda, tuvaloq uning ko'ziga maxsus yopishqoq suyuqlik otib uni vaqtincha ko'r qilib qochishi mumkin.",
            "Uning tuxumlari qum ustida hech qanday insiz qo'yiladi va toshchalarga juda o'xshaydi."
        ]
    },
    {
        "name_uz": "Oq boshli quzg'un (Sip)",
        "name_latin": "Gyps fulvus",
        "name_en": "Griffon Vulture",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "O'laksaxo'r (Yirik tuyoqlilar jasadlari - tabiat sanitari)",
        "habitat": "Chotqol, Zarafshon, Turkiston, Ko'hitang va Nurota tog' tizmalari",
        "lifespan": "30 - 40 yil",
        "speed": "65 km/soat (havoda qanot qoqmasdan soatlab silliq parvoz)",
        "weight": "6.5 - 11 kg, qanotlari kengligi 2.4 - 2.8 metr",
        "description": "Oq boshli quzg'un — tog'larning gigant qushi va tabiatning ajralmas sanitari. Uning qanotlari kengligi deyarli 2.8 metrga yetadi. Bosh va bo'ynida patlarning deyarli yo'qligi unga o'laksa bilan oziqlanganda tozalikni saqlashga xizmat qiladi. Ularning oshqozon shirasi shunchalik kuchli kislotaga egaki, kuydirgi (sibir yarasi), vabo va botulizm kabi eng halokatli bakteriyalarni ham zararsizlantirib yuboradi.",
        "uz_red_book_status": "2 (Zaif, kamyob tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Tog' qo'riqxonalari (Chotqol, G'issar, Zomin) qoyalarida uya quradi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Dunyo bo'ylab barqaror, ammo pestitsidlar va zaharlanishlar sababli kuzatuvda).",
        "similar_species": "Qora tasqara (Aegypius monachus), Boltayutar (Gypaetus barbatus / Qoplonqush)",
        "differences": """1. QORA TASQARADAN FARQI: Qora tasqara to'q qora-qo'ng'ir rangda va butunlay tekislik va o'rmon daraxtlariga in quradi; Quzg'un esa sarg'ish-och qumrang bo'lib, faqat tik qoyalarda uya soladi.
2. BOLTAYUTARDAN FARQI: Boltayutar asosan suyaklar bilan oziqlanadi va havoda suyakni toshga tashlab chaqadi; Oq boshli quzg'un esa go'sht to'qimalarini yeydi.
3. OSHQOZON KISLOTASI: Uning oshqozon kislotasi pH darajasi 1 ga yaqin bo'lib, o'lat va kuydirgi bakteriyalarini butunlay yo'q qiladi.""",
        "sound_file": "/static/audio/swallow_song.mp3",
        "sound_description": "O'laksa atrofida talashganda chiqariladigan xirillagan hisslash va qiyqirishlar.",
        "sound_type": "swallow",
        "image_url": "https://images.unsplash.com/photo-1549608276-5786777e6587?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1579202673506-ca3ce28943ef?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Quzg'unlar o'laksalarni yeb, o'lat va boshqa yuqumli epidemiyalar tarqalishining oldini oluvchi yagona tabiiy tozalovchilardir.",
            "Ular havoda 3 500 metr balandlikda qanot qoqmasdan soatlab ko'tariluvchi issiq havo oqimlarida ucha oladilar.",
            "Quzg'un o'z o'ljasini yoki o'laksani 5-6 kilometr uzoqlikdan turib ko'ra oladigan o'tkir ko'rish qobiliyatiga ega."
        ]
    },
    {
        "name_uz": "Bo'z echkiemar (Varan)",
        "name_latin": "Varanus griseus",
        "name_en": "Desert Monitor",
        "category": "Sudralib yuruvchilar",
        "class_name": "Reptilia",
        "diet": "Yirtqich (Kemiruvchilar, ilonlar, kaltakesaklar, toshbaqa tuxumlari, qushlar)",
        "habitat": "Qizilqum cho'li, Ustyurt, Surxondaryo va Farg'ona vodiysi cho'l zonalari",
        "lifespan": "10 - 15 yil",
        "speed": "20 km/soat (tez yugurish, daraxtga chiqish)",
        "weight": "2.5 - 3.5 kg, uzunligi 1.5 metrgacha",
        "description": "Bo'z echkiemar — O'zbekiston faunasidagi eng bahaybat kaltakesak (xalq orasida 'cho'l timsohi' deb ham ataladi). Uzunligi dumi bilan birga 1.5 metrga yetadi. Zaharli ilonlar (jumladan kobra va charxilon) chaqishiga nisbatan tabiiy immunitetga ega. Xavf tug'ilganda u tanasini shishiradi, dumi bilan qamchidek qattiq uradi va dahshatli pishqiradi.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES I ilovasiga kiritilgan. O'tmishda terisi uchun ko'p ovlangan, hozirda qat'iy muhofaza qilinadi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Dunyo miqyosida, ammo O'rta Osiyoda populyatsiyasi sezilarli qisqargan).",
        "similar_species": "Komodo ajdari (Varanus komodoensis), Cho'l kaltakesagi, Agama",
        "differences": """1. ODDIY KALTAKESAKLARDAN FARQI: Echkiemar dumi dushmanini urib yiqitadigan qurol vazifasini o'taydi va dumi uzilib tushmaydi (avtotomiya yo'q); oddiy kaltakesak dumi uziladi.
2. TILI: Uning tili ilonlarniki kabi uzun, binafsharang va uchi ikki ayrilgan bo'lib, hid molekulalarini ushlaydi.
3. ILONLARNI OVLASH: Har qanday zaharli cho'l ilonini osongina ushlab, boshidan yutib yuboradi, zahari unga ta'sir qilmaydi.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Echkiemarning vajohatli xirillashi, puflashi va qattiq pishqirishi.",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Bo'z echkiemar yer ostida 2-2.5 metr chuqurlikda in qaziydi va qishki sovuqda 6 oy davomida uyquda yotadi.",
            "Xalq orasida uni 'echki emadi' degan asossiz afsona yuradi, aslida u echki emmaydi, faqat cho'l zararkunandalarini ovlaydi.",
            "U dumi bilan urgan zarba kuchi kichik kemiruvchining suyaklarini sindirishga yetadi."
        ]
    },
    {
        "name_uz": "O'rta Osiyo toshbaqasi (Dasht toshbaqasi)",
        "name_latin": "Testudo horsfieldii / Agrionemys horsfieldii",
        "name_en": "Central Asian Tortoise / Horsfield's Tortoise",
        "category": "Sudralib yuruvchilar",
        "class_name": "Reptilia",
        "diet": "O'txo'r (Efemer o'tlar, shuvoq, gullar, poliz ekinlari barglari)",
        "habitat": "O'zbekistonning barcha cho'l, adir va tog' etagi hududlari",
        "lifespan": "30 - 50 yil",
        "speed": "0.3 - 0.5 km/soat",
        "weight": "0.8 - 2 kg, kosasi uzunligi 15 - 25 sm",
        "description": "O'rta Osiyo toshbaqasi — qattiq suyak kosasi (karapaks va plastron) bilan himoyalangan qadimiy sudralib yuruvchi. Uning oldingi oyoqlarida 4 tadan mustahkam tirnoqli barmoq bor (shuning uchun to'rt barmoqli toshbaqa ham deyiladi), bu tirnoqlar bilan qattiq cho'l tuprog'ida chuqur inlar qaziydi. U yilning faqat 3-4 oyida (bahorda) faol hayot kechiradi, jazirama yozda va qahraton qishda esa yer ostida chuqur uyquga ketadi.",
        "uz_red_book_status": "Kiritilmagan (Keng tarqalgan, ammo eksporti qat'iy cheklangan)",
        "uz_red_book_desc": "CITES II ro'yxatiga kiritilgan. Noqonuniy ushlab xorijga sotish taqiqlangan.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif holatda). Cho'llarning o'zlashtirilishi va noqonuniy savdo xavfi tufayli xalqaro ro'yxatda zaif maqomda.",
        "similar_species": "O'rtayer dengizi toshbaqasi (Testudo graeca), Botqoq toshbaqasi",
        "differences": """1. BOTQOQ TOSHBАQASIDAN FARQI: Botqoq toshbaqasi suvda yashaydi, barmoqlari orasida suzgich pardalar bor va yirtqich; O'rta Osiyo toshbaqasi quruqlikda yashaydi va mutlaq o'txo'r.
2. OYOQ BARMOQLARI: O'rta Osiyo toshbaqasida 4 ta barmoq bo'ladi, O'rtayer dengizi toshbaqasida esa 5 ta.
3. UYQU DAVRI: Yilning 8-9 oyini yer osti uyqusida (ham qishki, ham yozgi estivatsiya) o'tkazuvchi kamyob biologik moslashuvga ega.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Toshbaqa xavf sezib boshini kosasiga tortganda chiqaradigan xosildor xirillash tovushi.",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1508817628294-5a453fa0b8fb?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "1968 yilda sovet kosmik kemasi 'Zond-5' bortida O'rta Osiyo toshbaqalari Oy atrofini aylanib uchib, tirik qaytgan dastlabki jonzotlar bo'lgan.",
            "Toshbaqa kosasi qobig'idagi halqalar soniga qarab daraxt kabi uning yoshini aniqlash mumkin.",
            "Ular oylarcha mutlaqo suvsiz yashay oladi, namlikni faqat bahorgi shirali o'tlardan oladi."
        ]
    },
    {
        "name_uz": "O'rta Osiyo kobrasi",
        "name_latin": "Naja oxiana",
        "name_en": "Central Asian Cobra / Oxus Cobra",
        "category": "Sudralib yuruvchilar",
        "class_name": "Reptilia",
        "diet": "Yirtqich (Kemiruvchilar, qurbaqalar, boshqa ilonlar va qush tuxumlari)",
        "habitat": "Surxondaryo, Qashqadaryo, Samarqand va Navoiy adirlari, toshloq qirlar",
        "lifespan": "15 - 20 yil",
        "speed": "8 - 12 km/soat",
        "weight": "1 - 2 kg, uzunligi 1.5 - 1.8 metr",
        "description": "O'rta Osiyo kobrasi — O'zbekistonning eng xavfli va ulug'vor zaharli iloni. Hind kobrasidan farqli o'laroq, uning orqasida 'ko'zoynak' surati bo'lmaydi. Xavf tug'ilganda u tanasining oldingi 1/3 qismini yer uzra tik ko'taradi, qovurg'alarini kengaytirib kapyushon hosil qiladi va qattiq vishillaydi. Uning zahari o'ta kuchli neyrotoksik ta'sirga ega bo'lib, nafas olish markazini falajlaydi. Tibbiyotda uning zaharidan qimmatbaho dorilar olinadi.",
        "uz_red_book_status": "1 (Yo'qolib borayotgan, kamyob tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va CITES II ilovasiga kiritilgan. Zahar olish maqsadida ko'p tutib yo'q qilingan, tabiatda qat'iy qo'riqlanadi.",
        "iucn_status": "NT",
        "iucn_desc": "Near Threatened (Zaif holatga yaqin).",
        "similar_species": "Hind kobrasi (Naja naja), Qora ilon (Gyurza / Macrovipera lebetina), Charxilon (Echis carinatus)",
        "differences": """1. GYURZADAN FARQI: Gyurza qalin gavdali, boshi uchburchak va kapyushoni yo'q, zahari gemotoksik (qonni iviydi); Kobra esa nozik, kapyushon yozadi va zahari neyrotoksik (asabni falajlaydi).
2. HIND KOBRASIDAN FARQI: O'rta Osiyo kobrasining kapyushonida ko'zoynak halqasi yo'q, rangi och sarg'ish-qo'ng'irdan qoragacha bo'ladi.
3. HUJUM USLUBI: Kobra darhol chaqmaydi — avval tik turib ogohlantiradi, ko'pincha boshini urib quruq zarba beradi, faqat majbur bo'lganda zahar kiritadi.""",
        "sound_file": "/static/audio/rabbit_sound.mp3",
        "sound_description": "Kobraning vajohat bilan kapyushon yoyib tiklangandagi bo'g'iq vishillashi (hissing).",
        "sound_type": "rabbit",
        "image_url": "https://images.unsplash.com/photo-1531386151447-fd76ad50012f?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Kobra hech qachon o'ljasini chaynay olmaydi, o'zining boshidan 2-3 barobar katta kemiruvchilarni ham butunligicha yutadi.",
            "Kobra zahari neyrotoksin bo'lib, tibbiyotda og'riqsizlantiruvchi va yurak xurujlariga qarshi dorilar tayyorlashda ishlatiladi.",
            "Kobraning pastki jag' suyaklari bir-biriga elastik boylamlar bilan birikkan bo'lib, o'ljani yutayotganda keng ochiladi."
        ]
    },
    {
        "name_uz": "Orol bakrasi (Ship balig'i)",
        "name_latin": "Acipenser nudiventris",
        "name_en": "Bastard Sturgeon / Ship Sturgeon",
        "category": "Baliqlar",
        "class_name": "Actinopterygii",
        "diet": "Bentosxo'r (Suv tubidagi mollyuskalar, qisqichbaqasimonlar, mayda baliqlar)",
        "habitat": "Orol dengizi havzasi, Amudaryo va Sirdaryoning quyi oqimlari",
        "lifespan": "30 - 35 yil",
        "speed": "15 km/soat",
        "weight": "20 - 40 kg (ba'zan 50 kg gacha), uzunligi 2 metr",
        "description": "Orol bakrasi — qadimiy dinozavrlar davridan beri deyarli o'zgarmay kelayotgan osyotrsimon relikt baliq. Uning suyakli skeleti o'rniga elastik tog'ay (xorda) mavjud bo'lib, terisi ustida 5 qator qattiq suyakli 'bug'unchalar' (blyashkalar) bor. Orol dengizining qurishi va daryolarda to'g'onlar qurilishi oqibatida tabiiy ko'payish yo'llari to'silib, deyarli qirilib ketish arafasiga kelgan.",
        "uz_red_book_status": "1 (Yo'qolib borayotgan, o'ta kritik holatdagi tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga va IUCN Qizil ro'yxatiga CR maqomida kiritilgan. Maxsus pitomniklarda sun'iy ko'paytirilmoqda.",
        "iucn_status": "CR",
        "iucn_desc": "Critically Endangered (Kritik xavf ostida). Yovvoyi tabiatda deyarli yo'q bo'lib bormoqda.",
        "similar_species": "Beluga (Huso huso), Rus osyotri (Acipenser gueldenstaedtii), Soxta kurakburun (Scaphirhynchus)",
        "differences": """1. SOXTA KURAKBURUNDAN FARQI: Soxta kurakburun kichik (50-70 sm) va dumi uzun qamchisimon; Orol bakrasi esa bahaybat (2 metr) va dumi akulanikidek asimmetrik.
2. PASTKI LABI: Orol bakrasining pastki labi butun (uzluksiz) bo'ladi, boshqa osyotrlarda esa pastki lab o'rtasidan ajralgan.
3. SUYAK TUZILISHI: Baliqda haqiqiy suyaklar yo'q, butun umurtqa o'rnida tog'ay xorda joylashgan, go'shti va qora uvildiriqi qadimdan juda yuqori baholangan.""",
        "sound_file": "/static/audio/dolphin_click.mp3",
        "sound_description": "Daryo tubida suzganda suv pufakchalari va mayin suv to'lqinlari shovqini.",
        "sound_type": "dolphin",
        "image_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Orol bakrasi Orol dengizining sho'r suvida semirib, tuxum qo'yish (urug'lanish) uchun Amudaryo bo'ylab yuzlab kilometr yuqoriga suzib chiqqan.",
            "Uning qora ikrasi (uvildiriqi) tabiatda eng qimmatbaho biologik mahsulotlardan biri hisoblangan.",
            "Bakra baliqlari 200 million yildan ortiq vaqt davomida o'z tashqi tuzilishini o'zgartirmagan tirik qazilmadir."
        ]
    }
]

def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Hayvonlar ma'lumotlari yangilanmoqda...")
    inserted_count = 0
    updated_count = 0
    for item in ANIMALS_DATA:
        cursor.execute("SELECT id FROM animals WHERE name_uz = ?", (item["name_uz"],))
        existing = cursor.fetchone()
        if existing:
            update_animal(existing[0], item)
            updated_count += 1
        else:
            insert_animal(item)
            inserted_count += 1
            
    print(f"Jami {len(ANIMALS_DATA)} ta hayvon: {inserted_count} ta yangi qo'shildi, {updated_count} ta yangilandi.")
    
    # Create default demo admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'admin@hayvonlar.uz'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO users (google_id, email, name, picture, role)
        VALUES ('google-admin-101', 'admin@hayvonlar.uz', 'Bosh Administrator', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80', 'admin')
        """)
        conn.commit()
        print("Standart administrator hisobi yaratildi: admin@hayvonlar.uz")
        
    conn.close()

if __name__ == "__main__":
    seed()
