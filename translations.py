"""
ANIMORA - 5 Tilda Xalqaro Lokalizatsiya Moduli (i18n)
Tillar:
1. O'zbek (uz) - 🇺🇿
2. Qoraqalpoq (kaa) - 🟩🟨🟦
3. Rus (ru) - 🇷🇺
4. Ingliz (en) - 🇬🇧
5. Fransuz (fr) - 🇫🇷
"""

try:
    from animal_content_en import ANIMALS_EN
except ImportError:
    ANIMALS_EN = {}

try:
    from animal_content_ru import ANIMALS_RU
except ImportError:
    ANIMALS_RU = {}

try:
    from animal_content_kaa import ANIMALS_KAA
except ImportError:
    ANIMALS_KAA = {}

try:
    from animal_content_fr import ANIMALS_FR
except ImportError:
    ANIMALS_FR = {}

ANIMAL_CONTENT_I18N = {
    "en": ANIMALS_EN,
    "ru": ANIMALS_RU,
    "kaa": ANIMALS_KAA,
    "fr": ANIMALS_FR
}

SUPPORTED_LANGUAGES = {
    "uz": {
        "code": "uz",
        "name": "O'zbek",
        "native": "O'zbekcha",
        "flag": "🇺🇿",
        "speech_lang": "uz-UZ"
    },
    "kaa": {
        "code": "kaa",
        "name": "Qoraqalpoq",
        "native": "Qaraqalpaqsha",
        "flag": "🟩🟨🟦",
        "speech_lang": "kk-KZ"
    },
    "ru": {
        "code": "ru",
        "name": "Rus",
        "native": "Русский",
        "flag": "🇷🇺",
        "speech_lang": "ru-RU"
    },
    "en": {
        "code": "en",
        "name": "Ingliz",
        "native": "English",
        "flag": "🇬🇧",
        "speech_lang": "en-US"
    },
    "fr": {
        "code": "fr",
        "name": "Fransuz",
        "native": "Français",
        "flag": "🇫🇷",
        "speech_lang": "fr-FR"
    }
}

DEFAULT_LANGUAGE = "uz"

TRANSLATIONS = {
    "uz": {
        # Nav
        "brand_subtitle": "Hayvonot Olami Portali",
        "nav_animals": "Hayvonlar",
        "nav_compare": "Turlarni Taqqoslash",
        "nav_redbook": "Qizil Kitob",
        "nav_quiz": "Viktorina (O'yin)",
        "nav_ai": "Animora AI Yordamchi",
        "nav_admin": "Admin Panel",
        "nav_login": "Kirish",
        "nav_logout": "Chiqish 🚪",
        "theme_day": "Kun",
        "theme_night": "Tun",
        "lang_name": "O'zbekcha",

        # Splash
        "splash_title": "ANIMORA AI MATRITSA YUKLANMOQDA...",
        "splash_sub": "Jonli tabiat va ekotizim ma'lumotlari yangilanmoqda",

        # Home
        "hero_tag": "🦁 ZAMONAVIY BIOLOGIK EKOTIZIM",
        "hero_title": "O'zbekiston va Jahon Hayvonot Olami",
        "hero_desc": "Noyob hayvonlar, ularning o'xshash turlaridan qanday farqlanishi, haqiqiy akustik tovushlari va Qizil kitob maqomi bilan tanishing.",
        "stat_total": "Bazada jami hayvonlar",
        "stat_redbook": "Qizil kitobga kiritilganlar",
        "stat_sounds": "Akustik hayvon ovozlari",
        "stat_ai": "Aqlli biologik yordamchi",

        # Categories
        "cat_all": "🐾 Barchasi",
        "cat_mammals": "🐆 Sutemizuvchilar",
        "cat_birds": "🦅 Qushlar",
        "cat_reptiles": "🦎 Sudralib yuruvchilar",
        "cat_fish": "🐟 Baliqlar",
        "cat_redbook": "📕 Qizil Kitob turlari",
        "search_placeholder": "Hayvon nomi, lotincha yoki tavsif...",

        # Card actions
        "listen_sound": "Ovozni tinglash",
        "how_it_differs": "Farqi qanday? 🔬",
        "view_details": "Batafsil ma'lumot 🐾",
        "similar_species_label": "O'xshash turlari:",
        "safe_status": "Xavfsiz holatda",
        "no_results": "Afsuski, so'rovingiz bo'yicha hech qanday hayvon topilmadi.",

        # Detail Page
        "back_link": "← Barcha hayvonlarga qaytish",
        "acoustic_title": "Akustik Ovoz",
        "acoustic_sub": "ning tovush signali",
        "listen": "Tinglash",
        "habitat": "🌿 Yashash joyi",
        "diet": "🥩 Oziqlanishi",
        "speed": "⚡ Tezligi",
        "weight": "⚖️ O'rtacha vazni",
        "lifespan": "⏳ Umri",
        "compare_btn": "⚖️ Boshqa hayvon bilan solishtirish (Laboratoriya)",
        "diff_title": "O'xshash Turlaridan Qanday Farqlanadi?",
        "diff_sub": "Taqqoslanuvchi turlar:",
        "redbook_title": "Qizil Kitob Maqomi va Muhofazasi",
        "redbook_uz": "O'zbekiston Qizil Kitobi",
        "redbook_iucn": "Xalqaro IUCN Qizil Ro'yxati",
        "facts_title": "✨ Kam Ma'lum Bo'lgan Qiziqarli Faktlar",

        # Compare
        "compare_hero_badge": "🔬 Interaktiv Zoologik Laboratoriya",
        "compare_hero_title": "O'xshash Turlarni Farqlash",
        "compare_hero_desc": "Gepard va qoplon, sher va yo'lbars, quyon va tovushqon kabi o'xshash turlar qanday farqlanadi? Ikkita hayvonni tanlang va solishtiring!",
        "compare_animal1": "1-Hayvon:",
        "compare_animal2": "2-Hayvon:",
        "compare_btn_action": "Taqqoslash ⚖️",
        "compare_diff_features": "FARQLOVCHI BELGILARI:",

        # Redbook
        "redbook_hero_badge": "📕 O'zbekiston & Xalqaro Muhofaza",
        "redbook_hero_title": "Qizil Kitob va Yo'qolib Ketish Xavfidagi Turlar",
        "redbook_hero_desc": "Tabiatni asrash — insoniyat burchidir. Bu yerda O'zbekiston Qizil kitobi hamda IUCN xalqaro qizil ro'yxatiga kiritilgan noyob turlar haqida ilmiy ma'lumotlar jamlangan.",
        "filter_all": "Barcha Xavf Ostidagi Turlar",
        "filter_cr": "CR — Butunlay yo'q bo'lish arafasida",
        "filter_en": "EN — Xavf ostidagi turlar",
        "filter_vu": "VU — Zaif holatdagi turlar",

        # Quiz
        "quiz_hero_badge": "🧠 Interaktiv Biologik Viktorina",
        "quiz_hero_title": "Hayvonlar Farqini Topa Olasizmi?",
        "quiz_hero_desc": "Akustik tovushlar, biologik belgilar va farqlarni sinab ko'ring. Savolni o'qib berish tugmasini bosishingiz mumkin!",
        "quiz_question_num": "Savol:",
        "quiz_score": "To'plangan ball:",
        "quiz_listen": "Savolni o'qib berish",
        "quiz_reading": "Savol o'qilmoqda... (To'xtatish)",
        "quiz_expl": "💡 ZOOLOGIK TUSHUNTIRISH:",
        "quiz_next": "Keyingi savol →",
        "quiz_congrats": "Tabriklaymiz, Viktorina Yakunlandi!",
        "quiz_finished_desc": "Siz barcha savollarga javob berdingiz.",
        "quiz_your_score": "Natijangiz:",
        "quiz_restart": "Qaytadan Boshlash 🔄",
        "quiz_back_home": "Bosh Sahifaga Qaytish 🐾",

        # AI Chat
        "ai_hero_badge": "✨ 3.8 Aqlli Zoologik Neyron Tarmog'i",
        "ai_hero_title": "Animora AI Zoologik Maslahatchi",
        "ai_hero_desc": "Hayvonlar bir-biridan qanday farqlanishi, O'zbekiston Qizil kitobi, yashash tarzi va ovozlari bo'yicha istalgan savolingizni bering!",
        "ai_welcome": "Salom! Men Animora AI biologik yordamchingizman. Hayvonlar, ularning o'xshash turlaridan qanday farqlanishi yoki Qizil kitob bo'yicha savolingizni bering.",
        "ai_chip1": "Gepard va qoplon farqi",
        "ai_chip2": "Sayg'oq haqida ma'lumot",
        "ai_chip3": "Qizil kitobga nimalar kirgan?",
        "ai_placeholder": "Savolingizni yozing (masalan, Gepard va qoplon farqi nima?)...",
        "ai_send": "Yuborish",

        # Login
        "login_title": "Tizimga Kirish",
        "login_desc": "Animora — yopiq ilmiy-ommabop biologik portal. Saytdan foydalanish uchun Google hisobingiz orqali kiring.",
        "login_btn_google": "Google Hisob bilan Kirish",
        "login_btn_admin": "🛡️ Administrator Kirishi (Parol bilan)",
        "admin_modal_title": "Administrator Kirishi",
        "admin_user": "Login",
        "admin_pass": "Parol",
        "admin_submit": "Kirish 🚀",

        # Footer & Modal
        "footer_title": "Animora — O'zbekiston va Jahon Hayvonot Olami Portali",
        "footer_sub": "O'zbekiston Qizil kitobi & IUCN Xalqaro Qizil ro'yxati asosida tuzilgan ilmiy-ommabop biologik tizim.",
        "footer_rights": "© 2026 Barcha huquqlar himoyalangan. Himoyalangan xavfsiz tizim.",
        "modal_diff_title": "Hayvon farqi",
        "modal_got_it": "Tushunarli",
        "status_audio_playing": "Akustik tovush to'lqini ijro etilmoqda...",
        "feature_latin_name": "Lotincha nomi",
        "feature_category": "Kategoriyasi",
        "filter_label": "Filtr",
        "hero_swallow_desc": "Epchil parvoz dinamikasiga ega havoyi hasharotxo'r.",
        "hero_rabbit_desc": "360 darajali panoramik ko'rish qobiliyatiga ega hushyor o'txo'r.",
        "hero_lion_desc": "Ochiq tekisliklar va savannalarning oliy ijtimoiy yirtqichi."
    },

    "kaa": {
        # Nav
        "brand_subtitle": "Haywanat Dúnyası Portalı",
        "nav_animals": "Haywanlar",
        "nav_compare": "Túrlerdi Salıstırıw",
        "nav_redbook": "Qızıl Kitap",
        "nav_quiz": "Viktorina (Oyın)",
        "nav_ai": "Animora AI Járdemshi",
        "nav_admin": "Admin Panel",
        "nav_login": "Kiriw",
        "nav_logout": "Shıǵıw 🚪",
        "theme_day": "Kún",
        "theme_night": "Tún",
        "lang_name": "Qaraqalpaqsha",

        # Splash
        "splash_title": "ANIMORA AI MATRITSA JÚKLENBEKTE...",
        "splash_sub": "Tiri tábiyat hám ekosistema maǵlıwmatları jańalanbaqta",

        # Home
        "hero_tag": "🦁 ZAMANAGÓY BIOLOGIYALÍQ EKOSISTEMA",
        "hero_title": "Ózbekstan hám Dúnya Haywanat Dúnyası",
        "hero_desc": "Nayev haywanlar, olardıń uqsas túrlerinen qalay parıqlanıwı, haqıyqıy akustikalıq dawısları hám Qızıl kitap statusı menen tanıasıń.",
        "stat_total": "Bazadag'ı barlıq haywanlar",
        "stat_redbook": "Qızıl kitapqa kirgizilgenler",
        "stat_sounds": "Akustikalıq haywan dawısları",
        "stat_ai": "Aqıllı biologiyalıq járdemshi",

        # Categories
        "cat_all": "🐾 Barlıǵı",
        "cat_mammals": "🐆 Sút emiziwshiler",
        "cat_birds": "🦅 Quslar",
        "cat_reptiles": "🦎 Bawırlap joriwshılar",
        "cat_fish": "🐟 Balıqlar",
        "cat_redbook": "📕 Qızıl Kitap túrleri",
        "search_placeholder": "Haywan atı, latınsha yamasa xarakteristika...",

        # Card actions
        "listen_sound": "Dawıstı tıńlaw",
        "how_it_differs": "Parqı qanday? 🔬",
        "view_details": "Tolıq maǵlıwmat 🐾",
        "similar_species_label": "Uqsas túrleri:",
        "safe_status": "Qáwipsiz jaǵdayda",
        "no_results": "Ókinishke oray, sorawıńız boyınsha hesh qanday haywan tabılmadı.",

        # Detail Page
        "back_link": "← Barlıq haywanlarǵa qaytıw",
        "acoustic_title": "Akustikalıq Dawıs",
        "acoustic_sub": "dawıs belgisi",
        "listen": "Tıńlaw",
        "habitat": "🌿 Jasaw ornı",
        "diet": "🥩 Awqatlanıwı",
        "speed": "⚡ Tezligi",
        "weight": "⚖️ Ortasha salmaǵı",
        "lifespan": "⏳ Ómiri",
        "compare_btn": "⚖️ Basqa haywan menen salıstırıw (Laboratoriya)",
        "diff_title": "Uqsas Túrlerinen Qalay Parıqlanadı?",
        "diff_sub": "Salıstırılatuǵın túrler:",
        "redbook_title": "Qızıl Kitap Statusı hám Qorǵalıwı",
        "redbook_uz": "Ózbekstan Qızıl Kitabı",
        "redbook_iucn": "Xalıqaralıq IUCN Qızıl Dizimi",
        "facts_title": "✨ Az Belgili Qızıqlı Faktlar",

        # Compare
        "compare_hero_badge": "🔬 Interaktiv Zoologiyalıq Laboratoriya",
        "compare_hero_title": "Uqsas Túrlerdi Parıqlaw",
        "compare_hero_desc": "Gepard penen qaplan, arystan menen jolbars, qoyan menen qum qoyanı qalay parıqlanadı? Eki haywandı saylap salıstırıń!",
        "compare_animal1": "1-Haywan:",
        "compare_animal2": "2-Haywan:",
        "compare_btn_action": "Salıstırıw ⚖️",
        "compare_diff_features": "PARÍQLAWSHÍ BELGILERI:",

        # Redbook
        "redbook_hero_badge": "📕 Ózbekstan & Xalıqaralıq Qorǵaw",
        "redbook_hero_title": "Qızıl Kitap hám Joǵalıw Qáwipindegi Túrler",
        "redbook_hero_desc": "Tábiyattı saqlaw — insaniyattıń minneti. Bul jerde Ózbekstan Qızıl kitabı hám IUCN qızıl dizimine kirgizilgen nayev túrler maǵlıwmatları jıynalǵan.",
        "filter_all": "Barlıq Qáwip Astındaǵı Túrler",
        "filter_cr": "CR — Joǵalıp ketiw qarsańında",
        "filter_en": "EN — Qáwip astındaǵı túrler",
        "filter_vu": "VU — Hálsiz jaǵdaydaǵı túrler",

        # Quiz
        "quiz_hero_badge": "🧠 Interaktiv Biologiyalıq Viktorina",
        "quiz_hero_title": "Haywanlar Parqın Taba Alasızba?",
        "quiz_hero_desc": "Akustikalıq dawıslar hám biologiyalıq belgilerdi sınań. Sorawdı oqıw túymesin basıwıńız múmkin!",
        "quiz_question_num": "Soraw:",
        "quiz_score": "Jıynaǵan ball:",
        "quiz_listen": "Sorawdı oqıp beriw",
        "quiz_reading": "Soraw oqılmaqta... (Toqtatıw)",
        "quiz_expl": "💡 ZOOLOGIYALÍQ TÚSINDIRIW:",
        "quiz_next": "Keyingi soraw →",
        "quiz_congrats": "Qutlıqlaymız, Viktorina Juwmaqlandı!",
        "quiz_finished_desc": "Siz barlıq sorawlarǵa juwap berdińiz.",
        "quiz_your_score": "Natiyjeńiz:",
        "quiz_restart": "Qaytadan Baslaw 🔄",
        "quiz_back_home": "Bas Betke Qaytıw 🐾",

        # AI Chat
        "ai_hero_badge": "✨ 3.8 Aqıllı Zoologiyalıq Neyron Tarmaǵı",
        "ai_hero_title": "Animora AI Zoologiyalıq Másláhátshi",
        "ai_hero_desc": "Haywanlar qalay parıqlanıwı, Qızıl kitap, jasaw tárizi haqqında soraw berip kórıń!",
        "ai_welcome": "Sálem! Men Animora AI biologiyalıq járdemshisimen. Haywanlar, olardıń parıqları yamasa Qızıl kitap boyınsha sorawıńızdı beriń.",
        "ai_chip1": "Gepard penen qaplan parqı",
        "ai_chip2": "Sayǵaq haqqında maǵlıwmat",
        "ai_chip3": "Qızıl kitapqa nelar kirgen?",
        "ai_placeholder": "Sorawıńızdı jazıń...",
        "ai_send": "Jiberiw",

        # Login
        "login_title": "Sistemaǵa Kiriw",
        "login_desc": "Animora — jabıq biologiyalıq portal. Paydalanıw ushın Google akkauntıńız arqalı kiriń.",
        "login_btn_google": "Google Akkaunt penen Kiriw",
        "login_btn_admin": "🛡️ Administrator Kiriwi (Parol menen)",
        "admin_modal_title": "Administrator Kiriwi",
        "admin_user": "Login",
        "admin_pass": "Parol",
        "admin_submit": "Kiriw 🚀",

        # Footer & Modal
        "footer_title": "Animora — Ózbekstan hám Dúnya Haywanat Dúnyası Portalı",
        "footer_sub": "Ózbekstan Qızıl kitabı & IUCN Xalıqaralıq Qızıl dizimi tiykarında dúzilgen biologiyalıq sistema.",
        "footer_rights": "© 2026 Barlıq huqıqlar qorǵalǵan.",
        "modal_diff_title": "Haywan parqı",
        "modal_got_it": "Túsindim",
        "status_audio_playing": "Akustikalıq dawıs tolqını esitilmekte...",
        "feature_latin_name": "Latınsha atı",
        "feature_category": "Kategoriyası",
        "filter_label": "Filtr",
        "hero_swallow_desc": "Shaqqan ushıw qábilyetine iye shıbın-shirkeyxor qus.",
        "hero_rabbit_desc": "360 graduslı panoroma kóriwge iye sezgir ósimlikxor.",
        "hero_lion_desc": "Ashıq maydanlar hám savannalardıń eń kúshli toparlı yırtqıshı."
    },

    "ru": {
        # Nav
        "brand_subtitle": "Портал животного мира",
        "nav_animals": "Животные",
        "nav_compare": "Сравнение видов",
        "nav_redbook": "Красная книга",
        "nav_quiz": "Викторина (Игра)",
        "nav_ai": "Animora AI Помощник",
        "nav_admin": "Админ-панель",
        "nav_login": "Войти",
        "nav_logout": "Выход 🚪",
        "theme_day": "День",
        "theme_night": "Ночь",
        "lang_name": "Русский",

        # Splash
        "splash_title": "ЗАГРУЗКА МАТРИЦЫ ANIMORA AI...",
        "splash_sub": "Синхронизация данных о живой природе и экосистемах",

        # Home
        "hero_tag": "🦁 СОВРЕМЕННАЯ БИОЛОГИЧЕСКАЯ ЭКОСИСТЕМА",
        "hero_title": "Животный мир Узбекистана и всей планеты",
        "hero_desc": "Познакомьтесь с редкими животными, их биологическими отличиями от схожих видов, настоящими звуками и статусом Красной книги.",
        "stat_total": "Всего животных в базе",
        "stat_redbook": "В Красной книге",
        "stat_sounds": "Акустические голоса",
        "stat_ai": "Умный био-помощник",

        # Categories
        "cat_all": "🐾 Все виды",
        "cat_mammals": "🐆 Млекопитающие",
        "cat_birds": "🦅 Птицы",
        "cat_reptiles": "🦎 Пресмыкающиеся",
        "cat_fish": "🐟 Рыбы",
        "cat_redbook": "📕 Виды Красной книги",
        "search_placeholder": "Название животного, латынь или описание...",

        # Card actions
        "listen_sound": "Слушать голос",
        "how_it_differs": "В чем разница? 🔬",
        "view_details": "Подробнее 🐾",
        "similar_species_label": "Схожие виды:",
        "safe_status": "Вне опасности",
        "no_results": "К сожалению, по вашему запросу ничего не найдено.",

        # Detail Page
        "back_link": "← Назад ко всем животным",
        "acoustic_title": "Акустический Голос",
        "acoustic_sub": "звуковой сигнал",
        "listen": "Слушать",
        "habitat": "🌿 Среда обитания",
        "diet": "🥩 Рацион питания",
        "speed": "⚡ Скорость бега",
        "weight": "⚖️ Средний вес",
        "lifespan": "⏳ Продолжительность жизни",
        "compare_btn": "⚖️ Сравнить с другим животным (Лаборатория)",
        "diff_title": "Чем отличается от схожих видов?",
        "diff_sub": "Сравниваемые виды:",
        "redbook_title": "Статус Красной книги и охрана",
        "redbook_uz": "Красная книга Узбекистана",
        "redbook_iucn": "Международный список IUCN",
        "facts_title": "✨ Малоизвестные интересные факты",

        # Compare
        "compare_hero_badge": "🔬 Интерактивная зоологическая лаборатория",
        "compare_hero_title": "Различение схожих видов",
        "compare_hero_desc": "Как отличить гепарда от леопарда, льва от тигра, зайца от кролика? Выберите двух животных и наглядно сравните!",
        "compare_animal1": "1-е Животное:",
        "compare_animal2": "2-е Животное:",
        "compare_btn_action": "Сравнить ⚖️",
        "compare_diff_features": "ОТЛИЧИТЕЛЬНЫЕ ПРИЗНАКИ:",

        # Redbook
        "redbook_hero_badge": "📕 Охрана природы Узбекистана и мира",
        "redbook_hero_title": "Красная книга и исчезающие виды",
        "redbook_hero_desc": "Беречь природу — общий долг. Здесь собраны научные сведения об охраняемых видах из Красной книги Узбекистана и Красного списка МСОП.",
        "filter_all": "Все виды под угрозой",
        "filter_cr": "CR — На грани полного исчезновения",
        "filter_en": "EN — Исчезающие виды",
        "filter_vu": "VU — Уязвимые виды",

        # Quiz
        "quiz_hero_badge": "🧠 Интерактивная био-викторина",
        "quiz_hero_title": "Сможете отличить животных?",
        "quiz_hero_desc": "Проверьте свои знания по биоакустике и анатомическим признакам. Нажмите кнопку, чтобы озвучить вопрос голосом!",
        "quiz_question_num": "Вопрос:",
        "quiz_score": "Набранные баллы:",
        "quiz_listen": "Озвучить вопрос",
        "quiz_reading": "Вопрос озвучивается... (Остановить)",
        "quiz_expl": "💡 ЗООЛОГИЧЕСКОЕ ПОЯСНЕНИЕ:",
        "quiz_next": "Следующий вопрос →",
        "quiz_congrats": "Поздравляем, викторина завершена!",
        "quiz_finished_desc": "Вы ответили на все вопросы.",
        "quiz_your_score": "Ваш результат:",
        "quiz_restart": "Начать заново 🔄",
        "quiz_back_home": "Вернуться на главную 🐾",

        # AI Chat
        "ai_hero_badge": "✨ 3.8 Умная нейросеть по зоологии",
        "ai_hero_title": "Animora AI Зоологический консультант",
        "ai_hero_desc": "Задайте любой вопрос об отличиях животных, Красной книге, среде обитания и повадках!",
        "ai_welcome": "Здравствуйте! Я Animora AI — ваш биологический помощник. Задайте любой вопрос об отличиях животных или Красной книге.",
        "ai_chip1": "Разница между гепардом и леопардом",
        "ai_chip2": "Информация о сайгаке",
        "ai_chip3": "Кто занесен в Красную книгу?",
        "ai_placeholder": "Введите ваш вопрос (например, в чем разница между гепардом и леопардом?)...",
        "ai_send": "Отправить",

        # Login
        "login_title": "Вход в систему",
        "login_desc": "Animora — закрытый научно-популярный портал о животном мире. Для доступа войдите через Google-аккаунт.",
        "login_btn_google": "Войти через аккаунт Google",
        "login_btn_admin": "🛡️ Вход для администратора (по паролю)",
        "admin_modal_title": "Вход администратора",
        "admin_user": "Логин",
        "admin_pass": "Пароль",
        "admin_submit": "Войти 🚀",

        # Footer & Modal
        "footer_title": "Animora — Портал животного мира Узбекистана и планеты",
        "footer_sub": "Научно-популярная система на основе Красной книги Узбекистана и Красного списка МСОП.",
        "footer_rights": "© 2026 Все права защищены. Защищенная безопасная система.",
        "modal_diff_title": "Отличия животного",
        "modal_got_it": "Понятно",
        "status_audio_playing": "Воспроизведение акустической звуковой волны...",
        "feature_latin_name": "Научное название",
        "feature_category": "Категория",
        "filter_label": "Фильтр",
        "hero_swallow_desc": "Виртуозный воздушный охотник за летающими насекомыми.",
        "hero_rabbit_desc": "Чуткое травоядное с панорамным круговым зрением 360°.",
        "hero_lion_desc": "Верховный социальный хищник открытых равнин и саванн."
    },

    "en": {
        # Nav
        "brand_subtitle": "Fauna & Wildlife Portal",
        "nav_animals": "Animals",
        "nav_compare": "Species Comparison",
        "nav_redbook": "Red Book",
        "nav_quiz": "Quiz Game",
        "nav_ai": "Animora AI Assistant",
        "nav_admin": "Admin Panel",
        "nav_login": "Log In",
        "nav_logout": "Log Out 🚪",
        "theme_day": "Day",
        "theme_night": "Night",
        "lang_name": "English",

        # Splash
        "splash_title": "LOADING ANIMORA AI MATRIX...",
        "splash_sub": "Live wildlife and ecosystem intelligence synchronizing",

        # Home
        "hero_tag": "🦁 ADVANCED BIOLOGICAL ECOSYSTEM",
        "hero_title": "Wildlife of Uzbekistan and the World",
        "hero_desc": "Discover rare wildlife, biological distinctions between similar species, authentic acoustic calls, and global conservation status.",
        "stat_total": "Total animals in database",
        "stat_redbook": "Red Book species",
        "stat_sounds": "Acoustic animal voices",
        "stat_ai": "Smart biological assistant",

        # Categories
        "cat_all": "🐾 All Animals",
        "cat_mammals": "🐆 Mammals",
        "cat_birds": "🦅 Birds",
        "cat_reptiles": "🦎 Reptiles",
        "cat_fish": "🐟 Fishes",
        "cat_redbook": "📕 Red Book Species",
        "search_placeholder": "Animal name, latin name or description...",

        # Card actions
        "listen_sound": "Listen to sound",
        "how_it_differs": "How it differs? 🔬",
        "view_details": "Full details 🐾",
        "similar_species_label": "Similar species:",
        "safe_status": "Least Concern (Safe)",
        "no_results": "No animals found matching your query.",

        # Detail Page
        "back_link": "← Back to all animals",
        "acoustic_title": "Acoustic Vocalization",
        "acoustic_sub": "audio signal",
        "listen": "Play sound",
        "habitat": "🌿 Habitat",
        "diet": "🥩 Diet",
        "speed": "⚡ Running speed",
        "weight": "⚖️ Average weight",
        "lifespan": "⏳ Lifespan",
        "compare_btn": "⚖️ Compare with another animal (Lab)",
        "diff_title": "How Does It Differ from Similar Species?",
        "diff_sub": "Compared species:",
        "redbook_title": "Red Book Status & Protection",
        "redbook_uz": "Red Data Book of Uzbekistan",
        "redbook_iucn": "International IUCN Red List",
        "facts_title": "✨ Lesser-Known Fascinating Facts",

        # Compare
        "compare_hero_badge": "🔬 Interactive Zoological Laboratory",
        "compare_hero_title": "Distinguishing Similar Species",
        "compare_hero_desc": "How do you tell a cheetah from a leopard, a lion from a tiger, a hare from a rabbit? Pick two animals and compare side-by-side!",
        "compare_animal1": "1st Animal:",
        "compare_animal2": "2nd Animal:",
        "compare_btn_action": "Compare ⚖️",
        "compare_diff_features": "DISTINGUISHING FEATURES:",

        # Redbook
        "redbook_hero_badge": "📕 Uzbekistan & Global Conservation",
        "redbook_hero_title": "Red Data Book & Endangered Species",
        "redbook_hero_desc": "Preserving nature is our shared responsibility. Comprehensive scientific data on protected species from Uzbekistan and the IUCN Red List.",
        "filter_all": "All Threatened Species",
        "filter_cr": "CR — Critically Endangered",
        "filter_en": "EN — Endangered",
        "filter_vu": "VU — Vulnerable",

        # Quiz
        "quiz_hero_badge": "🧠 Interactive Wildlife Quiz",
        "quiz_hero_title": "Can You Distinguish Wildlife?",
        "quiz_hero_desc": "Test your knowledge of acoustic calls, anatomy, and distinct species traits. Click the voice button to hear questions read aloud!",
        "quiz_question_num": "Question:",
        "quiz_score": "Score:",
        "quiz_listen": "Read Question Aloud",
        "quiz_reading": "Reading question... (Stop)",
        "quiz_expl": "💡 ZOOLOGICAL EXPLANATION:",
        "quiz_next": "Next question →",
        "quiz_congrats": "Congratulations, Quiz Completed!",
        "quiz_finished_desc": "You have answered all the questions.",
        "quiz_your_score": "Your Score:",
        "quiz_restart": "Restart Quiz 🔄",
        "quiz_back_home": "Back to Home 🐾",

        # AI Chat
        "ai_hero_badge": "✨ 3.8 Smart Zoological Neural Engine",
        "ai_hero_title": "Animora AI Wildlife Consultant",
        "ai_hero_desc": "Ask any question regarding animal distinctions, the Red Book, natural habitats, acoustic sounds, and animal behavior!",
        "ai_welcome": "Hello! I am Animora AI, your wildlife assistant. Ask me anything about animal distinctions, species traits, or the Red Book.",
        "ai_chip1": "Difference between cheetah and leopard",
        "ai_chip2": "Information about Saiga antelope",
        "ai_chip3": "Which species are in the Red Book?",
        "ai_placeholder": "Type your question (e.g. difference between cheetah and leopard?)...",
        "ai_send": "Send",

        # Login
        "login_title": "Sign In to Portal",
        "login_desc": "Animora is an exclusive zoological wildlife portal. Please sign in with your Google account to explore.",
        "login_btn_google": "Sign in with Google",
        "login_btn_admin": "🛡️ Administrator Login (Password)",
        "admin_modal_title": "Administrator Login",
        "admin_user": "Username",
        "admin_pass": "Password",
        "admin_submit": "Log In 🚀",

        # Footer & Modal
        "footer_title": "Animora — Wildlife & Zoological Portal of Uzbekistan and the World",
        "footer_sub": "Scientific-educational intelligence system based on the Red Data Book of Uzbekistan and IUCN Red List.",
        "footer_rights": "© 2026 All rights reserved. Secure protected system.",
        "modal_diff_title": "Species distinction",
        "modal_got_it": "Understood",
        "status_audio_playing": "Playing acoustic sound waveform...",
        "feature_latin_name": "Scientific Name",
        "feature_category": "Category",
        "filter_label": "Filter",
        "hero_swallow_desc": "Acrobatic aerial insectivore with agile flight dynamics.",
        "hero_rabbit_desc": "High-alert terrestrial herbivore with 360-degree panoramic vision.",
        "hero_lion_desc": "Apex social carnivore of open plains and scrublands."
    },

    "fr": {
        # Nav
        "brand_subtitle": "Portail de la Faune & Vie Sauvage",
        "nav_animals": "Animaux",
        "nav_compare": "Comparaison des espèces",
        "nav_redbook": "Livre Rouge",
        "nav_quiz": "Quiz Éducatif",
        "nav_ai": "Assistant IA Animora",
        "nav_admin": "Panneau d'administration",
        "nav_login": "Connexion",
        "nav_logout": "Déconnexion 🚪",
        "theme_day": "Jour",
        "theme_night": "Nuit",
        "lang_name": "Français",

        # Splash
        "splash_title": "CHARGEMENT DE LA MATRICE ANIMORA IA...",
        "splash_sub": "Synchronisation des données sur la faune et les écosystèmes",

        # Home
        "hero_tag": "🦁 ÉCOSYSTÈME BIOLOGIQUE AVANCÉ",
        "hero_title": "Faune d'Ouzbékistan et du Monde",
        "hero_desc": "Découvrez des animaux rares, leurs distinctions par rapport aux espèces similaires, leurs vocalises réelles et leur statut de conservation mondial.",
        "stat_total": "Total des animaux dans la base",
        "stat_redbook": "Espèces du Livre Rouge",
        "stat_sounds": "Sons acoustiques d'animaux",
        "stat_ai": "Assistant biologique intelligent",

        # Categories
        "cat_all": "🐾 Tous les animaux",
        "cat_mammals": "🐆 Mammifères",
        "cat_birds": "🦅 Oiseaux",
        "cat_reptiles": "🦎 Reptiles",
        "cat_fish": "🐟 Poissons",
        "cat_redbook": "📕 Espèces du Livre Rouge",
        "search_placeholder": "Nom de l'animal, nom latin ou description...",

        # Card actions
        "listen_sound": "Écouter le son",
        "how_it_differs": "Quelle différence ? 🔬",
        "view_details": "Détails complets 🐾",
        "similar_species_label": "Espèces similaires :",
        "safe_status": "Préoccupation mineure (Sûr)",
        "no_results": "Aucun animal trouvé pour votre recherche.",

        # Detail Page
        "back_link": "← Retour à tous les animaux",
        "acoustic_title": "Vocalisation Acoustique",
        "acoustic_sub": "signal sonore",
        "listen": "Écouter",
        "habitat": "🌿 Habitat naturel",
        "diet": "🥩 Régime alimentaire",
        "speed": "⚡ Vitesse de course",
        "weight": "⚖️ Poids moyen",
        "lifespan": "⏳ Espérance de vie",
        "compare_btn": "⚖️ Comparer avec un autre animal (Labo)",
        "diff_title": "Comment diffère-t-il des espèces similaires ?",
        "diff_sub": "Espèces comparées :",
        "redbook_title": "Statut du Livre Rouge & Préservation",
        "redbook_uz": "Livre Rouge d'Ouzbékistan",
        "redbook_iucn": "Liste Rouge Internationale de l'UICN",
        "facts_title": "✨ Faits fascinants et peu connus",

        # Compare
        "compare_hero_badge": "🔬 Laboratoire Zoologique Interactif",
        "compare_hero_title": "Distinguer les Espèces Similaires",
        "compare_hero_desc": "Comment distinguer un guépard d'un léopard, un lion d'un tigre, un lièvre d'un lapin ? Choisissez deux animaux et comparez !",
        "compare_animal1": "1er Animal :",
        "compare_animal2": "2e Animal :",
        "compare_btn_action": "Comparer ⚖️",
        "compare_diff_features": "CARACTÉRISTIQUES DISTINCTIVES :",

        # Redbook
        "redbook_hero_badge": "📕 Protection en Ouzbékistan & Monde",
        "redbook_hero_title": "Livre Rouge & Espèces Menacées",
        "redbook_hero_desc": "Protéger la nature est notre devoir commun. Données scientifiques sur les espèces protégées du Livre Rouge d'Ouzbékistan et de l'UICN.",
        "filter_all": "Toutes les espèces menacées",
        "filter_cr": "CR — En danger critique d'extinction",
        "filter_en": "EN — En danger",
        "filter_vu": "VU — Vulnérable",

        # Quiz
        "quiz_hero_badge": "🧠 Quiz Biologique Interactif",
        "quiz_hero_title": "Pouvez-vous distinguer les animaux ?",
        "quiz_hero_desc": "Testez vos connaissances en sons réels, anatomie et critères distinctifs. Activez la lecture vocale de la question !",
        "quiz_question_num": "Question :",
        "quiz_score": "Score :",
        "quiz_listen": "Lire la question à voix haute",
        "quiz_reading": "Lecture en cours... (Arrêter)",
        "quiz_expl": "💡 EXPLICATION ZOOLOGIQUE :",
        "quiz_next": "Question suivante →",
        "quiz_congrats": "Félicitations, Quiz Terminé !",
        "quiz_finished_desc": "Vous avez répondu à toutes les questions.",
        "quiz_your_score": "Votre Résultat :",
        "quiz_restart": "Recommencer 🔄",
        "quiz_back_home": "Retour à l'accueil 🐾",

        # AI Chat
        "ai_hero_badge": "✨ Moteur Neuronal Zoologique 3.8",
        "ai_hero_title": "Animora IA Consultant Zoologique",
        "ai_hero_desc": "Posez toutes vos questions sur les différences entre espèces, le Livre Rouge, les habitats naturels et les cris d'animaux !",
        "ai_welcome": "Bonjour ! Je suis Animora IA, votre assistant zoologique. Posez-moi vos questions sur les animaux, leurs distinctions ou le Livre Rouge.",
        "ai_chip1": "Différence entre guépard et léopard",
        "ai_chip2": "Informations sur l'antilope saïga",
        "ai_chip3": "Quelles espèces sont dans le Livre Rouge ?",
        "ai_placeholder": "Posez votre question (ex. quelle différence entre guépard et léopard ?)...",
        "ai_send": "Envoyer",

        # Login
        "login_title": "Connexion au Portail",
        "login_desc": "Animora est un portail zoologique exclusif. Veuillez vous connecter avec votre compte Google.",
        "login_btn_google": "Se connecter avec Google",
        "login_btn_admin": "🛡️ Connexion Administrateur (Mot de passe)",
        "admin_modal_title": "Connexion Administrateur",
        "admin_user": "Identifiant",
        "admin_pass": "Mot de passe",
        "admin_submit": "Connexion 🚀",

        # Footer & Modal
        "footer_title": "Animora — Portail de la Faune Sauvage d'Ouzbékistan et du Monde",
        "footer_sub": "Système d'intelligence scientifique basé sur le Livre Rouge d'Ouzbékistan et la Liste Rouge de l'UICN.",
        "footer_rights": "© 2026 Tous droits réservés. Système sécurisé.",
        "modal_diff_title": "Distinction de l'espèce",
        "modal_got_it": "Compris",
        "status_audio_playing": "Lecture de l'onde acoustique en cours...",
        "feature_latin_name": "Nom scientifique",
        "feature_category": "Catégorie",
        "filter_label": "Filtre",
        "hero_swallow_desc": "Insectivore aérien acrobatique au vol extrêmement agile.",
        "hero_rabbit_desc": "Herbivore terrestre très vigilant doté d'une vision panoramique à 360°.",
        "hero_lion_desc": "Superprédateur social régnant sur les savanes et plaines ouvertes."
    }
}

# Localized animal names
ANIMAL_NAMES_I18N = {
    1: {
        "uz": "Sher (Arslon)",
        "kaa": "Arystan (Sher)",
        "ru": "Лев",
        "en": "Lion",
        "fr": "Lion"
    },
    2: {
        "uz": "Quyon (Yovvoyi quyon / Qum tovushqoni)",
        "kaa": "Qoyan (Qum qoyanı)",
        "ru": "Заяц (Песчаный заяц)",
        "en": "Hare / Wild Rabbit",
        "fr": "Lièvre / Lapin sauvage"
    },
    3: {
        "uz": "Qaldirg'och (Qishloq qaldirg'ochi)",
        "kaa": "Qarlıǵash",
        "ru": "Ласточка (Деревенская ласточка)",
        "en": "Barn Swallow",
        "fr": "Hirondelle rustique"
    },
    4: {
        "uz": "Qor qoploni (Ilbirs)",
        "kaa": "Qar qaplanı (Ilbirs)",
        "ru": "Снежный барс (Ирбис)",
        "en": "Snow Leopard",
        "fr": "Léopard des neiges (Panthère des neiges)"
    },
    5: {
        "uz": "Gepard",
        "kaa": "Gepard",
        "ru": "Гепард",
        "en": "Cheetah",
        "fr": "Guépard"
    },
    6: {
        "uz": "Jayron (Qoraquyruq ohu)",
        "kaa": "Jeyran (Qaraquyrıq)",
        "ru": "Джейран (Чернохвостая газель)",
        "en": "Goitered Gazelle",
        "fr": "Gazelle à goître"
    },
    7: {
        "uz": "Oddiy Bo'ri",
        "kaa": "Ápiwayı Bóri",
        "ru": "Серый волк",
        "en": "Grey Wolf",
        "fr": "Loup gris"
    },
    8: {
        "uz": "Tyanshan Qo'ng'ir Ayig'i",
        "kaa": "Tyanshan Qońır Ayıwı",
        "ru": "Тянь-шаньский бурый медведь",
        "en": "Tien Shan Brown Bear",
        "fr": "Ours brun du Tian Shan"
    },
    9: {
        "uz": "Buxoro Bug'usi (Xongul)",
        "kaa": "Buxara Bug'ısı (Xońgıl)",
        "ru": "Бухарский олень (Хангул)",
        "en": "Bactrian Deer (Bukhara Deer)",
        "fr": "Cerf de Bactriane (Hangul)"
    },
    10: {
        "uz": "Burgut (Oltin burgut)",
        "kaa": "Búrkıt (Altın búrkıt)",
        "ru": "Беркут",
        "en": "Golden Eagle",
        "fr": "Aigle royal"
    },
    11: {
        "uz": "Delfin (Afalina)",
        "kaa": "Delfin (Afalina)",
        "ru": "Дельфин (Афалина)",
        "en": "Bottlenose Dolphin",
        "fr": "Grand dauphin"
    },
    14: {
        "uz": "Sayg'oq (Sayga kiyigi)",
        "kaa": "Aqqulaq (Sayǵaq)",
        "ru": "Сайгак (Сайга)",
        "en": "Saiga Antelope",
        "fr": "Antilope Saïga"
    },
    15: {
        "uz": "Amur yo'lbarsi (Sibir yo'lbarsi)",
        "kaa": "Amur jolbarısı",
        "ru": "Амурский тигр",
        "en": "Amur Tiger (Siberian Tiger)",
        "fr": "Tigre de Sibérie"
    },
    16: {
        "uz": "Afrika fili",
        "kaa": "Afrika pili",
        "ru": "Африканский слон",
        "en": "African Elephant",
        "fr": "Éléphant d'Afrique"
    },
    17: {
        "uz": "Jirafa",
        "kaa": "Jirafa",
        "ru": "Жираф",
        "en": "Giraffe",
        "fr": "Girafe"
    },
    18: {
        "uz": "Ko'k kit (Moviy kit)",
        "kaa": "Kók kit",
        "ru": "Синий кит",
        "en": "Blue Whale",
        "fr": "Baleine bleue"
    },
    19: {
        "uz": "Oq ayiq (Qutb ayig'i)",
        "kaa": "Aq ayıw",
        "ru": "Белый медведь",
        "en": "Polar Bear",
        "fr": "Ours polaire"
    },
    20: {
        "uz": "Katta panda",
        "kaa": "Úlken panda",
        "ru": "Большая панда",
        "en": "Giant Panda",
        "fr": "Panda géant"
    },
    21: {
        "uz": "Old Osiyo qoploni (Leopard)",
        "kaa": "Aldıńǵı Aziya qaplanı",
        "ru": "Переднеазиатский леопард",
        "en": "Persian Leopard",
        "fr": "Léopard de Perse"
    },
    22: {
        "uz": "Pushti saqoqqush (Pelikan)",
        "kaa": "Qızǵısh birqazan",
        "ru": "Розовый пеликан",
        "en": "Great White Pelican",
        "fr": "Pélican blanc"
    },
    23: {
        "uz": "Pushti flamingo (Qizilg'oz)",
        "kaa": "Qızǵısh flamingo",
        "ru": "Обыкновенный фламинго",
        "en": "Greater Flamingo",
        "fr": "Flamant rose"
    },
    24: {
        "uz": "Yo'rg'a tuvaloq (Yo'rg'atoq)",
        "kaa": "Jorǵa duadaq",
        "ru": "Дрофа-красотка (Джек)",
        "en": "Macqueen's Bustard",
        "fr": "Outarde de Macqueen"
    },
    25: {
        "uz": "Oq boshli quzg'un (Sip)",
        "kaa": "Aq baslı qaraqus",
        "ru": "Белоголовый сип",
        "en": "Griffon Vulture",
        "fr": "Vautour fauve"
    },
    26: {
        "uz": "Bo'z echkiemar (Varan)",
        "kaa": "Boz eshkiemar (Varan)",
        "ru": "Серый варан",
        "en": "Desert Monitor",
        "fr": "Varan du désert"
    },
    27: {
        "uz": "O'rta Osiyo toshbaqasi (Dasht toshbaqasi)",
        "kaa": "Orta Aziya tasbaqası",
        "ru": "Среднеазиатская черепаха",
        "en": "Central Asian Tortoise",
        "fr": "Tortue de Horsfield"
    },
    28: {
        "uz": "O'rta Osiyo kobrasi",
        "kaa": "Orta Aziya kobrası",
        "ru": "Среднеазиатская кобра",
        "en": "Central Asian Cobra",
        "fr": "Cobra d'Asie centrale"
    },
    29: {
        "uz": "Orol bakrasi (Ship balig'i)",
        "kaa": "Aral bekiresi (Ship balıǵı)",
        "ru": "Аральский шип",
        "en": "Ship Sturgeon",
        "fr": "Esturgeon bâtard"
    }
}

# Categories i18n
CATEGORY_I18N = {
    "Sutemizuvchilar": {
        "uz": "Sutemizuvchilar",
        "kaa": "Sút emiziwshiler",
        "ru": "Млекопитающие",
        "en": "Mammals",
        "fr": "Mammifères"
    },
    "Qushlar": {
        "uz": "Qushlar",
        "kaa": "Quslar",
        "ru": "Птицы",
        "en": "Birds",
        "fr": "Oiseaux"
    },
    "Sudralib yuruvchilar": {
        "uz": "Sudralib yuruvchilar",
        "kaa": "Bawırlap joriwshılar",
        "ru": "Пресмыкающиеся",
        "en": "Reptiles",
        "fr": "Reptiles"
    },
    "Baliqlar": {
        "uz": "Baliqlar",
        "kaa": "Balıqlar",
        "ru": "Рыбы",
        "en": "Fish",
        "fr": "Poissons"
    }
}

def get_translation(lang: str, key: str, default: str = None) -> str:
    """Retrieve translated string for a given key."""
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANGUAGE
    trans = TRANSLATIONS[lang]
    if key in trans:
        return trans[key]
    # Fallback to uz
    if key in TRANSLATIONS[DEFAULT_LANGUAGE]:
        return TRANSLATIONS[DEFAULT_LANGUAGE][key]
    return default or key

def localize_animal(animal: dict, lang: str = "uz") -> dict:
    """Return fully localized animal dictionary with all scientific, biological, and conservation fields."""
    if not animal or lang == "uz":
        return animal
    item = dict(animal)
    animal_id = item.get("id")

    # If full localized dataset exists for this language and animal ID
    if lang in ANIMAL_CONTENT_I18N and animal_id in ANIMAL_CONTENT_I18N[lang]:
        content = ANIMAL_CONTENT_I18N[lang][animal_id]
        for field, value in content.items():
            if value is not None:
                item[field] = value
    else:
        if animal_id in ANIMAL_NAMES_I18N and lang in ANIMAL_NAMES_I18N[animal_id]:
            item["name_uz"] = ANIMAL_NAMES_I18N[animal_id][lang]
        elif lang == "en" and item.get("name_en"):
            item["name_uz"] = item["name_en"]
            
        cat = item.get("category")
        if cat in CATEGORY_I18N and lang in CATEGORY_I18N[cat]:
            item["category"] = CATEGORY_I18N[cat][lang]
            
    return item

def localize_animals_list(animals: list, lang: str = "uz") -> list:
    """Return list of localized animals."""
    if not animals or lang == "uz":
        return animals
    return [localize_animal(a, lang) for a in animals]
