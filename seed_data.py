import os
import sqlite3
from database import init_db, get_connection, insert_animal

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
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Qaldirg'och suvni ham to'xtamasdan, havoda daryo yoki ko'l yuzasidan uchib o'tayotganda ichadi.",
            "Bir qaldirg'och oilasi yoz davomida 1 milliontagacha zararli hasharot va chivinlarni yo'q qiladi.",
            "Har yili bahorda minglab kilometr masofani bosib o'tib, aynan o'tgan yilgi eski iniga qaytib keladi."
        ]
    },
    {
        "name_uz": "Qor qoploni (Ilbirs)",
        "name_latin": "Panthera uncia",
        "name_en": "Snow Leopard",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Sibir tog' echkisi, arxar, sug'urlar, qushlar)",
        "habitat": "Baland qorli tog'lar (Tyanshan, Pomir-Oloy, 3000-5000 metr balandlikda)",
        "lifespan": "15 - 18 yil",
        "speed": "65 km/soat (tik qoyalarda chaqqon sakrash)",
        "weight": "30 - 55 kg",
        "description": "Ilbirs — O'zbekiston va Markaziy Osiyo tog'larining eng sirli va go'zal ramzi. Oqish-kulrang qalin mo'ynasi, qora halqasimon dog'lari va ulkan kalta-qalin dumi bor. U sovuq iqlimga, kislorod tanqis balandliklarga va tik qoyalarda yashashga ajoyib moslashgan.",
        "uz_red_book_status": "1 (Yo'qolib ketish arafasida turgan)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. G'arbiy Tyanshan va Pomir-Oloy tog' tizmalarida (Chotqol, Hisor qo'riqxonalari) juda kam sonli (taxminan 80-100 bosh) saqlanib qolgan.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif maqomda). Butun dunyo bo'yicha qat'iy muhofaza qilinadi.",
        "similar_species": "Oddiy qoplon (Panthera pardus), Gepard, Silovsin (Lynx)",
        "differences": """1. ODDIY QOPLON (LEOPARD)DAN FARQI: Ilbirsning mo'ynasi qalin, momiq va oq-kumushrang; oddiy qoplon esa qisqa yaltiroq sarg'ish-olovrang mo'ynaga ega.
2. DUMI: Ilbirsning dumi tanasi uzunligiga teng (1 metrgacha) va juda qalin bo'lib, sakrashda rul vazifasini o'taydi hamda sovuqda yuzini o'rab isinadi.
3. OVOZI: Ilbirs sher yoki yo'lbars kabi qattiq o'kira olmaydi (tomoq tuzilishi boshqacha), faqat past ovozda xirillaydi va xushchaqchaq murlar chiqaradi.""",
        "sound_file": "/static/audio/snow_leopard.mp3",
        "sound_description": "Ilbirsning o'ziga xos tovushlari: purr, xirillash va past tonli xurillashlar. O'kirmaydi.",
        "sound_type": "leopard",
        "image_url": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1577975882846-431adc8c2009?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Ilbirs bir sakrashda 15 metrgacha masofani zabt eta oladi — bu mushuksimonlar ichida mutlaq rekord!",
            "Keng va yungli panjalari qorda chang'i kabi sirg'almasdan va botmasdan yurishiga yordam beradi.",
            "O'zbekistonda ilbirs Hisor va Ugom-Chotqol milliy bog'larida fotoqopqonlar orqali kuzatiladi."
        ]
    },
    {
        "name_uz": "Gepard",
        "name_latin": "Acinonyx jubatus",
        "name_en": "Cheetah",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (G'azallar, jayronlar, yosh antilopalar, tovushqonlar)",
        "habitat": "Ochiq savannalar, cho'llar va quruq dashtlar",
        "lifespan": "10 - 12 yil",
        "speed": "112 - 120 km/soat (sayyoradagi eng tez yuguruvchi sutemizuvchi)",
        "weight": "35 - 65 kg",
        "description": "Gepard — quruqlikdagi eng tezkor hayvon. U atigi 3 soniyada 0 dan 100 km/soat tezlikka chiqa oladi. Yupqa elastik tanasi, keng o'pka va yuragi, o'ziga xos yuz chiziqlari bilan boshqa barcha mushuklardan farqlanadi.",
        "uz_red_book_status": "0 (Yo'qolib ketgan tur)",
        "uz_red_book_desc": "O'zbekistonda Ustyurt va Qizilqum cho'llarida Osiyo gepardi yashagan. So'nggi marta 1970-yillarda Ustyurtda qayd etilgan, hozirda O'zbekiston tabiatida yo'qolgan deb hisoblanadi.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Osiyo gepardi kenja turi esa CR - o'ta xavf ostida).",
        "similar_species": "Qoplon (Leopard), Yaguar, Serval",
        "differences": """1. KO'Z YOSHI CHIZIG'I: Gepardning ko'zlarining ichki burchagidan og'ziga qadar qora chiziq o'tgan bo'lib, u quyosh nurini qaytaradi. Leopard va yaguarda bunday chiziq yo'q!
2. DOG'LAR SHAKLI: Gepardning dog'lari oddiy, yaxlit qora nuqtalar shaklida; leopardda esa o'rtasi ochiq halqasimon 'rozetka' dog'lar mavjud.
3. TIRNOQLARI: Gepardning tirnoqlari itlarnikidek ichkariga to'liq tortilmaydi — bu unga katta tezlikda yerga yopishib yugurish imkonini beradi. Boshqa mushuklarda tirnoq to'liq berkinadi.""",
        "sound_file": "/static/audio/cheetah_chirp.mp3",
        "sound_description": "Gepard qushlarnikiga o'xshash chiyillash (chirp), purrlash va xirillash ovozlarini chiqaradi. U mutlaqo o'kirmaydi.",
        "sound_type": "cheetah",
        "image_url": "https://images.unsplash.com/photo-1547970810-dc1eac8161a7?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Gepard maksimal tezlikda chopganda, har bir qadamda 7 metrgacha masofani bosib o'tadi va vaqtning 50% qismida tanasi havoda bo'ladi.",
            "Uzoq quvlashdan so'ng gepardning tana harorati 41°C ga yetishi mumkin, shuning uchun ovdan so'ng 30 daqiqa dam olishi shart.",
            "Dumi yugurish vaqtida keskin burilishlar uchun xuddi kema ruli kabi xizmat qiladi."
        ]
    },
    {
        "name_uz": "Jayron (Qoraquyruq ohu)",
        "name_latin": "Gazella subgutturosa",
        "name_en": "Goitered Gazelle",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (Cho'l o'tlari, shuvoq, sho'ra, saksovul novdalari)",
        "habitat": "Qizilqum, Ustyurt cho'llari, gipsli va qumloq dashtlar",
        "lifespan": "8 - 12 yil",
        "speed": "65 km/soat",
        "weight": "20 - 33 kg",
        "description": "Jayron — Markaziy Osiyo cho'llarining eng xushbichim va nafis antilopasi. O'zbekistonda xalq dostonlarida go'zallik ramzi sanaladi. Erkaklarining qora liratsimon shoxlari, urg'ochilarida esa shox bo'lmaydi. Dumi qop-qora bo'lgani sababli xalq orasida 'qoraquyruq' deb ataladi.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Buxorodagi 'Jayron' ekologik markazida maxsus ko'paytiriladi va muhofaza qilinadi.",
        "iucn_status": "VU",
        "iucn_desc": "Vulnerable (Zaif maqomda). Cho'llarning o'zlashtirilishi tufayli kamaygan.",
        "similar_species": "Sayg'oq (Saiga tatarica), Ohu (Capreolus)",
        "differences": """1. SAYG'OQDAN FARQI: Sayg'oqning o'ziga xos egilgan yumaloq 'xartumsimon' burni bor; jayronning yuzi esa tekis, nihoyatda chiroyli va nozik.
2. SHOXLARI: Erkak jayronlarning shoxlari qora va liraga o'xshash qayrilgan; sayg'oqning shoxlari esa sarg'ish-shaffof va to'g'riroq.
3. DUMI: Jayron qochayotganda qora dumini yuqoriga ko'taradi — bu o'z to'dasiga xavf belgisidir.""",
        "sound_file": "/static/audio/gazelle_snort.mp3",
        "sound_description": "Jayronlar xavf paytida burnidan pishqirgan (snort) ovoz chiqaradi va yerga tuyoq uradi.",
        "sound_type": "gazelle",
        "image_url": "https://images.unsplash.com/photo-1574063413132-355dbfd83e25?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Jayronlar suv ichmasdan haftalab yashay oladi, namlikni cho'l o'simliklarining ertalabki shabnamidan oladi.",
            "Buxoro yaqinidagi 'Jayron' pitomnigi dunyodagi eng noyob cho'l hayvonlari pitomniklaridan biridir.",
            "Yangi tug'ilgan jayronchalar bir necha soat ichida onasining ketidan yugura oladi."
        ]
    },
    {
        "name_uz": "Oddiy Bo'ri",
        "name_latin": "Canis lupus",
        "name_en": "Grey Wolf",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Yirtqich (Tuyoqlilar, tovushqonlar, kemiruvchilar)",
        "habitat": "Tog'lar, cho'llar, dashtlar, to'qayzorlar",
        "lifespan": "10 - 15 yil",
        "speed": "55 - 65 km/soat (uzoq masofalarga charchamasdan yuguradi)",
        "weight": "35 - 70 kg",
        "description": "Bo'ri — itlar oilasining eng yirik yovvoyi a'zosi. Yuksak intellekt, qat'iy to'da (stay) iyerarxiyasi va ajoyib chidamlilikka ega. Ekotizimda 'tabiat sanitari' vazifasini bajarib, kasal va zaif hayvonlarni yo'qotadi.",
        "uz_red_book_status": "Kiritilmagan",
        "uz_red_book_desc": "O'zbekistonning barcha viloyatlarida, tog' va cho'llarida uchraydi, soni qonuniy tartibda nazorat qilinadi.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Xavf ostida emas).",
        "similar_species": "Shoqol (Canis aureus), Tulki (Vulpes vulpes), It (Canis familiaris)",
        "differences": """1. SHOQOLDAN FARQI: Bo'ri shoqoldan 2-3 barobar yirik; shoqol 8-15 kg bo'lsa, bo'ri 40-70 kg bo'ladi. Bo'rining dumi pastga osilgan, shoqolning dumi kalta va ingichka.
2. TULKIDAN FARQI: Tulki ancha kichik, qizg'ish mo'ynali, momiq dumi uzun va oq uchli; bo'ri esa yirik kulrang yirtqich.
3. ITDAN FARQI: Bo'ri hech qachon dumini tepaga qayirib ko'tarmaydi (doim orqasida osilib turadi), izlari bir to'g'ri chiziq bo'ylab tushadi va ko'zlari doim sariq-olovrang bo'ladi.""",
        "sound_file": "/static/audio/wolf_howl.mp3",
        "sound_description": "Bo'rining uzun va mungli uvillashi (howl) to'da a'zolarini yig'ish, hududni belgilash va ovga chorlash uchun xizmat qiladi.",
        "sound_type": "wolf",
        "image_url": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1598439210625-5067c578f3f6?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Bo'rilar to'dasi 200 km² gacha bo'lgan hududni nazorat qilishi mumkin.",
            "Bo'rining hid bilish qobiliyati insondan 100 barobar kuchliroq bo'lib, o'ljasini 2.5 km uzoqlikdan seza oladi.",
            "Bo'rilar umrining oxirigacha bitta juft bilan birga yashaydi (monogam)."
        ]
    },
    {
        "name_uz": "Tyanshan Qo'ng'ir Ayig'i (Oq tirnoqli ayiq)",
        "name_latin": "Ursus arctos isabellinus",
        "name_en": "Himalayan / Tien Shan Brown Bear",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "Hammao'r (Mevalar, yong'oqlar, ildizlar, hasharotlar, go'sht, baliq)",
        "habitat": "Tyanshan va Pomir-Oloy tog' tizmalari, archazorlar, baland alp o'tloqlari",
        "lifespan": "20 - 30 yil",
        "speed": "45 - 50 km/soat",
        "weight": "150 - 280 kg",
        "description": "Tog'larimizning eng yirik yirtqich vakili. Och sarg'ish-qo'ng'ir mo'ynasi va uzun oqish tirnoqlari bilan mashhur bo'lgani sababli 'oq tirnoqli ayiq' deb ham yuritiladi. Qishda qor ostidagi chuqur g'orlarda uyquga ketadi.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Chotqol, Zomin, Hisor tog' qo'riqxonalarida qat'iy muhofaza qilinadi.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered (Xavf ostida). Markaziy Osiyo hududida soni kam qolgan.",
        "similar_species": "Oddiy Yevroosiyo qo'ng'ir ayig'i (Ursus arctos arctos), Qora ayiq",
        "differences": """1. ODDIY QO'NG'IR AYIQDAN FARQI: Tyanshan ayig'ining old panjalaridagi tirnoqlari yorqin oq-sarg'ish rangda va juda uzun (10 sm gacha); oddiy qo'ng'ir ayiqda tirnoqlar qora bo'ladi.
2. MO'YNA RANGI: Rangi ancha och, sarg'ish-somonsimon bo'ladi.
3. KICHIKROQ O'LCHAM: Sibir va Kamchatka ayiqlariga (500 kg+) nisbatan ancha yengil va chaqqon.""",
        "sound_file": "/static/audio/bear_growl.mp3",
        "sound_description": "Ayiqning chuqur pishqirishi, vovullashi va past tonli tahdidli xirillashi (growl).",
        "sound_type": "bear",
        "image_url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Tyanshan ayig'i qishki uyquga yotishdan oldin tana vaznining 30-40 foizigacha yog' to'playdi.",
            "Qo'pol ko'rinsa-da, tik qoyalarda aqlbovar qilmas epchillik bilan ko'tariladi va daraxtlarga ham chiqa oladi.",
            "Yong'oqzor va mevali bog'lar ekotizimida urug'larni tarqatishda beqiyos o'rin tutadi."
        ]
    },
    {
        "name_uz": "Buxoro Bug'usi (Xongul)",
        "name_latin": "Cervus hanglu bactrianus",
        "name_en": "Bukhara Deer / Bactrian Deer",
        "category": "Sutemizuvchilar",
        "class_name": "Mammalia",
        "diet": "O'txo'r (To'qay qamishlari, jiyda barglari, yulg'un, o'tlar)",
        "habitat": "Amudaryo va Sirdaryo bo'yidagi to'qayzorlar",
        "lifespan": "12 - 16 yil",
        "speed": "50 km/soat",
        "weight": "160 - 240 kg",
        "description": "Xongul — Buxoro kiyigi nomi bilan mashhur bo'lgan O'zbekistonning milliy iftixori. Cho'l daryolari to'qaylariga mukammal moslashgan ushbu olijanob bug'u XX asrda deyarli qirilib ketish yoqasiga kelib qolgan edi, sa'y-harakatlar tufayli qayta tiklandi.",
        "uz_red_book_status": "1 (Yo'qolib ketish xavfi ostidagi tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobi va Qizil kitobning xalqaro ro'yxatida. Baday-To'qay, Quyi Amudaryo va Zarafshon davlat qo'riqxonalarida saqlanmoqda.",
        "iucn_status": "EN",
        "iucn_desc": "Endangered. Butun dunyoda faqat Markaziy Osiyo to'qaylarida yashaydi.",
        "similar_species": "Olijanob Yevropa bug'usi (Cervus elaphus), Kiyik (Capreolus)",
        "differences": """1. YEVROPA BUG'USIDAN FARQI: Xongulning tanasi och kulrang-qumloq tusda, to'qay o'simliklari orasida ko'rinmaydigan kamuflyajga ega. Shoxlarining tuzilishi soddaroq va 5 ta asosiy o'simtadan oshmaydi.
2. YASHASH MUHITI: Oddiy bug'ular sovuq ignabargli o'rmonlarda yashasa, xongul jazirama cho'llar orasidagi nam to'qayzorlarda yashaydi.
3. SUZISH QOBILIYATI: Daryolardan, hatto shiddatli Amudaryodan bemalol suzib o'tish qobiliyatiga ega.""",
        "sound_file": "/static/audio/deer_call.mp3",
        "sound_description": "Kuzgi juftlashish davrida erkak xongullarning kuchli karnaysimon bo'kirishi (bellowing/bugling).",
        "sound_type": "deer",
        "image_url": "https://images.unsplash.com/photo-1484406566174-9da000fda645?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "O'zbekiston tabiatni muhofaza qilish dasturlari orqali xongul soni 300 tadan 2500 boshdan ortiqqa ko'paytirildi — bu tabiatni saqlashning eng katta yutuqlaridan biridir.",
            "Erkak kiyiklar har yili bahorda ulkan shoxlarini tashlab yuboradi va yoz oxirigacha yangi shoxlar o'sib chiqadi.",
            "Xongulning qadimgi suratlari Afrosiyob devoriy rasmlarida ham uchraydi."
        ]
    },
    {
        "name_uz": "Burgut (Oltin burgut)",
        "name_latin": "Aquila chrysaetos",
        "name_en": "Golden Eagle",
        "category": "Qushlar",
        "class_name": "Aves",
        "diet": "Yirtqich (Quyonlar, sug'urlar, mayda tuyoqlilar, tulkilar)",
        "habitat": "Tog' cho'qqilari, tik qoyalar, keng ochiq platolar",
        "lifespan": "25 - 35 yil",
        "speed": "240 - 320 km/soat (o'ljaga shong'ishda)",
        "weight": "3.5 - 6.5 kg, qanot qulochi 2.2 metrgacha",
        "description": "Burgut — osmonning eng qudratli va mag'rur hukmdori. Boshining orqasidagi oltin tusli patlar unga alohida shukuh bag'ishlaydi. Kuchli panjalari va o'tkir tirnoqlari bo'rining bo'ynini ham majaqlashga yetadi. Markaziy Osiyo xalqlarida qadimdan ov qushi sifatida e'zozlanadi.",
        "uz_red_book_status": "2 (Zaif, kamayib borayotgan tur)",
        "uz_red_book_desc": "O'zbekiston Qizil kitobiga kiritilgan. Tog'li hududlarda uya quradi, soni inson ta'siri sababli kamaygan.",
        "iucn_status": "LC",
        "iucn_desc": "Least Concern (Global miqyosda barqaror).",
        "similar_species": "Lochin (Falco peregrinus), Qiyg'ir (Accipiter), Boltayutar (Gypaetus)",
        "differences": """1. LOCHINDAN FARQI: Burgut lochindan deyarli 4 barobar katta. Lochin havoda uchayotgan qushlarni urib tushiradi, burgut esa yerda yurgan yirik sutemizuvchilarni (quyon, hatto kiyik bolasi, bo'ri) ovlaydi.
2. PANJA VA TUMSHUG'I: Burgutning panjalari odam bilagidek baquvvat va tirnoqlari 6 sm gacha yetadi; lochinning panjalari ingichkaroq.
3. PARVOZ USLUBI: Burgut soatlab qanot qoqmasdan havo oqimlarida muallaq suzadi; lochin esa qanotlarini tez qoqib uchadi.""",
        "sound_file": "/static/audio/eagle_screech.mp3",
        "sound_description": "Burgutning o'tkir, vahimali qichqirig'i (screech) tog' daralarida aks-sado beradi.",
        "sound_type": "eagle",
        "image_url": "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?auto=format&fit=crop&w=1200&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1549608276-5786777e6587?auto=format&fit=crop&w=1000&q=80"
        ],
        "fun_facts": [
            "Burgut 2 kilometr balandlikdan turib o'tlar orasida qimirlagan sichqonni yoki quyonni aniq ko'ra oladi.",
            "O'ljaga sho'ng'iganida tezligi zamonaviy poyga avtomobillaridan ham oshib, 320 km/soatga yetadi.",
            "Ular qurgan uyalar ba'zan 2 metr diametrga va bir necha yuz kilogramm og'irlikka yetishi mumkin."
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
        "differences": """1. BALIQLAR VA AKULALARDAN FARQI: Akula baliq bo'lib jabra (quloq bargi) bilan nafas oladi va sovuqqonli; delfin esa issiqqonli sutemizuvchi bo'lib, o'pka bilan nafas oladi va bolalaydi.
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
    }
]

def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM animals")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Baza bo'sh. Standart hayvonlar ma'lumotlari kiritilmoqda...")
        for item in ANIMALS_DATA:
            insert_animal(item)
        print(f"{len(ANIMALS_DATA)} ta hayvon muvaffaqiyatli kiritildi!")
    else:
        print(f"Bazada allaqachon {count} ta hayvon mavjud.")
    
    # Create default demo admin user
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
