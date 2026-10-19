import os
import json
import sqlite3
import re
from typing import Dict, Any, List, Optional
from database import get_connection, get_all_animals, normalize_uz_text
from translations import localize_animal, get_translation

SYSTEM_PROMPTS = {
    "uz": """Siz hayvonot olami, zoologiya, O'zbekiston va Xalqaro Qizil kitob bo'yicha ixtisoslashgan mukammal AI yordamchisiz.
Ismingiz: Animora AI.
Vazifangiz: Foydalanuvchilarga hayvonlar, ularning o'xshash turlaridan qanday farqlanishi, yashash tarzi, ovozlari, O'zbekiston Qizil kitobi va IUCN maqomi haqida o'zbek tilida aniq, ravon va qiziqarli javob berish.
Har doim do'stona, ilmiy va tushunarli uslubda javob bering.""",

    "kaa": """Siz haywanat dúnyası, zoologiya, Ózbekstan hám Xalıqaralıq Qızıl kitap boyınsha qánigelesken mukammal AI járdemshisiz.
Atıńız: Animora AI.
Wazıypańız: Paydalanıwshılarǵa haywanlar, olardıń uqsas túrlerden parıqlanıwı, jasaw tárizi, dawısları, Qızıl kitap statusı haqqında qaraqalpaq tilinde anıq, ilimiy hám qızıqlı juwap beriw.
Har dayım doslarsha hám túsindirip juwap beriń.""",

    "ru": """Вы — высококвалифицированный научный ассистент по зоологии, животному миру Узбекистана и Международной Красной книге.
Ваше имя: Animora AI.
Ваша задача: подробно, увлекательно и научно грамотно отвечать пользователям на русском языке об отличиях животных, их повадках, голосах и охранном статусе.
Всегда отвечайте вежливо, понятно и структурированно.""",

    "en": """You are an advanced AI zoological intelligence assistant specializing in wildlife, species distinctions, and the Red Data Book.
Your name is Animora AI.
Your mission is to provide accurate, engaging, and scientifically structured responses in English regarding animal behaviors, comparative biology, sounds, and conservation status.
Always maintain a friendly, knowledgeable, and accessible tone.""",

    "fr": """Vous êtes un assistant IA de pointe spécialisé en zoologie, faune sauvage et Livre Rouge des espèces menacées.
Votre nom est Animora IA.
Votre mission est de répondre en français avec précision, clarté et rigueur scientifique sur les distinctions entre espèces, leurs habitats, leurs vocalisations et leur protection.
Répondez toujours de manière chaleureuse, pédagogique et structurée."""
}

def get_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'gemini_api_key'")
        row = cursor.fetchone()
        conn.close()
        if row and row["value"]:
            return row["value"]
    except:
        pass
    return ""

def call_gemini_api(api_key: str, message: str, lang: str = "uz") -> str:
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    sys_prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["uz"])
    contents = []
    contents.append({
        "role": "user",
        "parts": [{"text": sys_prompt + "\n\nSavol / Question: " + message}]
    })
    
    headers = {"Content-Type": "application/json"}
    payload = {"contents": contents}
    
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    if response.status_code == 200:
        data = response.json()
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
    raise Exception(f"Gemini API xatoligi: {response.text}")

def _extract_animal_tokens(animal: Dict[str, Any]) -> List[str]:
    """Extract normalized keywords for matching an animal across languages."""
    tokens = set()
    for key in ["name_uz", "name_latin", "name_en"]:
        val = normalize_uz_text(animal.get(key, ""))
        for w in re.findall(r'[a-z0-9]+', val):
            if len(w) > 2 and w not in ["yovvoyi", "qum", "chol", "orta", "osiyo", "tur", "daryo", "the", "and", "wild"]:
                tokens.add(w)
    return list(tokens)

def _find_matching_animals(norm_msg: str, animals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    matched = []
    for a in animals:
        tokens = _extract_animal_tokens(a)
        if any(re.search(r'\b' + re.escape(t) + r'\b', norm_msg) for t in tokens):
            matched.append(a)
        elif any(t in norm_msg for t in tokens if len(t) >= 4):
            if a not in matched:
                matched.append(a)
    return matched

def fallback_smart_ai(message: str, lang: str = "uz") -> str:
    """
    Intelligent Biological Knowledge Engine supporting 5 languages: uz, kaa, ru, en, fr.
    """
    norm_msg = normalize_uz_text(message)
    raw_animals = get_all_animals()
    matched_animals = _find_matching_animals(norm_msg, raw_animals)
    
    # Check for comparison
    comp_keywords = [
        "farq", "farqi", "farqlanadi", "taqqosla", "solishtir", "ajrat", "solishtirilsa",
        "parq", "parqi", "salistir", "salistiriw",
        "разница", "отличие", "отличается", "сравни", "сравнение",
        "difference", "differ", "distinguish", "compare", "versus",
        "différence", "differe", "comparer", "comparaison"
    ]
    is_compare = any(k in norm_msg for k in comp_keywords)
    
    if is_compare:
        if len(matched_animals) >= 2:
            a1 = localize_animal(matched_animals[0], lang)
            a2 = localize_animal(matched_animals[1], lang)
            if lang == "en":
                return f"""⚖️ **Biological comparison between {a1['name_uz']} and {a2['name_uz']}:**

📌 **1. {a1['name_uz']} ({a1['name_latin']}):**
• **Habitat:** {a1['habitat']}
• **Diet:** {a1['diet']}
• **Speed & Weight:** {a1['speed']} | {a1['weight']}
• **Status:** Uzbekistan Red Book: `{a1['uz_red_book_status']}`, IUCN: `{a1['iucn_status']}`

📌 **2. {a2['name_uz']} ({a2['name_latin']}):**
• **Habitat:** {a2['habitat']}
• **Diet:** {a2['diet']}
• **Speed & Weight:** {a2['speed']} | {a2['weight']}
• **Status:** Uzbekistan Red Book: `{a2['uz_red_book_status']}`, IUCN: `{a2['iucn_status']}`

🔍 **Distinguishing features:**
{a1['differences']}"""
            elif lang == "ru":
                return f"""⚖️ **Биологическое сравнение: {a1['name_uz']} и {a2['name_uz']}:**

📌 **1. {a1['name_uz']} ({a1['name_latin']}):**
• **Среда обитания:** {a1['habitat']}
• **Питание:** {a1['diet']}
• **Скорость и вес:** {a1['speed']} | {a1['weight']}
• **Статус:** Красная книга Узбекистана: `{a1['uz_red_book_status']}`, МСОП: `{a1['iucn_status']}`

📌 **2. {a2['name_uz']} ({a2['name_latin']}):**
• **Среда обитания:** {a2['habitat']}
• **Питание:** {a2['diet']}
• **Скорость и вес:** {a2['speed']} | {a2['weight']}
• **Статус:** Красная книга Узбекистана: `{a2['uz_red_book_status']}`, МСОП: `{a2['iucn_status']}`

🔍 **Отличительные особенности:**
{a1['differences']}"""
            elif lang == "fr":
                return f"""⚖️ **Comparaison biologique entre {a1['name_uz']} et {a2['name_uz']} :**

📌 **1. {a1['name_uz']} ({a1['name_latin']}) :**
• **Habitat :** {a1['habitat']}
• **Régime :** {a1['diet']}
• **Vitesse et poids :** {a1['speed']} | {a1['weight']}
• **Statut :** Livre Rouge d'Ouzbékistan : `{a1['uz_red_book_status']}`, UICN : `{a1['iucn_status']}`

📌 **2. {a2['name_uz']} ({a2['name_latin']}) :**
• **Habitat :** {a2['habitat']}
• **Régime :** {a2['diet']}
• **Vitesse et poids :** {a2['speed']} | {a2['weight']}
• **Statut :** Livre Rouge d'Ouzbékistan : `{a2['uz_red_book_status']}`, UICN : `{a2['iucn_status']}`

🔍 **Traits distinctifs :**
{a1['differences']}"""
            elif lang == "kaa":
                return f"""⚖️ **{a1['name_uz']} hám {a2['name_uz']} arasındaǵı biologiyalıq salıstırıw:**

📌 **1. {a1['name_uz']} ({a1['name_latin']}):**
• **Jasaw ornı:** {a1['habitat']}
• **Awqatlanıwı:** {a1['diet']}
• **Tezligi hám salmaǵı:** {a1['speed']} | {a1['weight']}
• **Qorǵaw statusı:** Qızıl kitap: `{a1['uz_red_book_status']}`, IUCN: `{a1['iucn_status']}`

📌 **2. {a2['name_uz']} ({a2['name_latin']}):**
• **Jasaw ornı:** {a2['habitat']}
• **Awqatlanıwı:** {a2['diet']}
• **Tezligi hám salmaǵı:** {a2['speed']} | {a2['weight']}
• **Qorǵaw statusı:** Qızıl kitap: `{a2['uz_red_book_status']}`, IUCN: `{a2['iucn_status']}`

🔍 **Uqsas túrlerden ajıratıwshı tiykarǵı parıqlar:**
{a1['differences']}"""
            else:
                return f"""⚖️ **{a1['name_uz']} va {a2['name_uz']} o'rtasidagi biologik taqqoslash:**

📌 **1. {a1['name_uz']}:**
• **Yashash joyi:** {a1['habitat']}
• **Oziqlanishi:** {a1['diet']}
• **Tezligi va vazni:** {a1['speed']} | {a1['weight']}
• **Muhofaza maqomi:** O'zbekiston Qizil kitobi: `{a1['uz_red_book_status']}`, IUCN: `{a1['iucn_status']}`

📌 **2. {a2['name_uz']}:**
• **Yashash joyi:** {a2['habitat']}
• **Oziqlanishi:** {a2['diet']}
• **Tezligi va vazni:** {a2['speed']} | {a2['weight']}
• **Muhofaza maqomi:** O'zbekiston Qizil kitobi: `{a2['uz_red_book_status']}`, IUCN: `{a2['iucn_status']}`

🔍 **O'xshash turlardan ajratuvchi asosiy farqlar:**
{a1['differences']}"""

        elif len(matched_animals) == 1:
            a = localize_animal(matched_animals[0], lang)
            return f"""🦁 **{a['name_uz']} ({a['name_latin']}):**

{a['differences']}

📌 **Habitat / Yashash joyi:** {a['habitat']}
🥩 **Diet / Oziqlanishi:** {a['diet']}
⚡ **Speed / Tezligi:** {a['speed']} | ⚖️ **Weight / Vazni:** {a['weight']}"""

        # General cheetah vs leopard
        if any(w in norm_msg for w in ["gepard", "qoplon", "leopard", "cheetah"]):
            if lang in ["en", "fr"]:
                return """🐆 **Key Differences: Cheetah vs Leopard:**
1. **Coat & Spots:** Cheetah has solid, round, discrete black spots. A leopard has rose-like 'rosettes' with open centers.
2. **Facial Markings:** Cheetah has iconic black 'tear tracks' running from inside corners of eyes down to the mouth. Leopards lack tear stripes.
3. **Claws:** Cheetah claws are semi-retractable like dogs (providing traction at high speed). Leopard claws retract completely.
4. **Hunting Behavior:** Cheetah hunts by blazing acceleration (up to 120 km/h) in open plains; leopard ambushes prey and hoists heavy kills up trees."""
            elif lang == "ru":
                return """🐆 **Основные отличия: Гепард и Леопард:**
1. **Пятна:** У гепарда — сплошные четкие черные точки. У леопарда — кольцеобразные пятна-розетки с пустотой внутри.
2. **Слезные дорожки:** У гепарда от внутренних уголков глаз к пасти идут черные «слезные полосы» (защита от солнца). У леопарда их нет.
3. **Когти:** У гепарда когти невтяжные (как у собак), дают сцепление при беге. У леопарда когти втягиваются полностью.
4. **Повадки:** Гепард охотится на открытых равнинах на скорости до 120 км/ч. Леопард нападает из засады и затаскивает добычу на деревья."""
            elif lang == "kaa":
                return """🐆 **Gepard hám Qaplan (Leopard) arasındaǵı tiykarǵı parıqlar:**
1. **Daǵları:** Gepard denesindegi daǵlar tutas qara noqatlar. Leopardta bolsa gúldey 'rozetka' daǵlar boladı.
2. **Kóz jas sızıǵı:** Gepardtıń kózinen awzına shekem qara sızıq ótken. Leopardta bunday sızıq joq.
3. **Tırnaqları:** Gepard tırnaqları tolıq kirmeydi; leopard tırnaqların tolıq jasırıp qoya aladı.
4. **Awlaw tárizi:** Leopard oljasın aǵashqa alıp shıǵadı; gepard tek tegislikte 120 km/saat tezlik penen quwıp awlaydı."""
            else:
                return """🐆 **Gepard va Qoplon (Leopard) o'rtasidagi asosiy farqlar:**
1. **Dog'lari:** Gepard tanasidagi dog'lar yakka-yakka yaxlit qora nuqtalardir. Leopardda esa gulsimon, markazi ochiq 'rozetka' dog'lar bo'ladi.
2. **Yuzdagi chiziq:** Gepardning ko'zlaridan labiga qadar qora 'ko'z yoshi chizig'i' o'tgan (quyosh nuridan himoya). Leopardda bunday chiziq yo'q.
3. **Tirnoqlari:** Gepardning tirnoqlari itlarnikidek ichkariga to'liq kirmaydi va yerga tiraladi; leopard tirnoqlarini to'liq yashira oladi.
4. **Xulq-atvori:** Leopard o'ljasini baland daraxtlarga olib chiqadi; gepard esa faqat tekislikda katta tezlikda (120 km/soat) quvlab ovlaydi."""

    # Red book query
    if any(k in norm_msg for k in ["qizil kitob", "red book", "iucn", "yoqolib", "красная книга", "livre rouge", "qizil kitap"]):
        red_animals = [a for a in raw_animals if a["uz_red_book_status"] != "Kiritilmagan" or a["iucn_status"] in ["CR", "EN", "VU"]]
        title = {
            "en": "📕 **Key Species Listed in the Red Book of Uzbekistan & IUCN:**\n",
            "ru": "📕 **Важнейшие виды, занесенные в Красную книгу Узбекистана и МСОП:**\n",
            "fr": "📕 **Espèces clés inscrites au Livre Rouge d'Ouzbékistan & UICN :**\n",
            "kaa": "📕 **Ózbekstan hám Xalıqaralıq Qızıl kitapqa kiritilgen turlar:**\n",
            "uz": "📕 **O'zbekiston va Xalqaro Qizil kitobga kiritilgan muhim turlar:**\n"
        }.get(lang, "📕 **O'zbekiston va Xalqaro Qizil kitobga kiritilgan muhim turlar:**\n")
        
        response_lines = [title]
        for ra in red_animals[:6]:
            loc = localize_animal(ra, lang)
            response_lines.append(f"• **{loc['name_uz']}** ({loc['name_latin']}):\n  - Red Book / Status: `{loc['uz_red_book_status']}` | IUCN: `{loc['iucn_status']}`\n  - {loc['uz_red_book_desc']}")
        return "\n".join(response_lines)

    # Specific animal match
    if matched_animals:
        a = localize_animal(matched_animals[0], lang)
        facts = "\n".join([f"  - {f}" for f in a.get("fun_facts", [])])
        return f"""🐾 **{a['name_uz']} ({a['name_latin']}):**

📖 **{get_translation(lang, 'stat_total')}:** {a['description']}
🌿 **{get_translation(lang, 'habitat')}:** {a['habitat']}
🥩 **{get_translation(lang, 'diet')}:** {a['diet']}
⚡ **{get_translation(lang, 'speed')}:** {a['speed']} | ⚖️ **{get_translation(lang, 'weight')}:** {a['weight']} | ⏳ **{get_translation(lang, 'lifespan')}:** {a['lifespan']}

📕 **{get_translation(lang, 'redbook_title')}:**
• Status: `{a['uz_red_book_status']}` ({a['uz_red_book_desc']})
• IUCN: `{a['iucn_status']}` ({a['iucn_desc']})

🔍 **{get_translation(lang, 'diff_title')}:**
{a['differences']}

✨ **{get_translation(lang, 'facts_title')}:**
{facts}"""

    # General Greeting
    greetings = {
        "kaa": """🌿 **Sálem! Men Animora AI — haywanat dúnyası boyınsha aqıllı járdemshimen.**
Sizge tómendegi temalarda járdem bere alaman:
1. **Haywanlardı salıstırıw:** Mısalı: *'Gepard penen qaplan parqı qanday?'*
2. **Qızıl kitap:** *'Qızıl kitapqa qaysı haywanlar kiritilgen?'*
3. **Dawıslar hám qızıqlı faktlar:** Jasaw ornı, tezligi hám tábiyatı.""",
        "ru": """🌿 **Здравствуйте! Я Animora AI — ваш интеллектуальный помощник по животному миру.**
Я готов ответить на ваши вопросы по следующим темам:
1. **Сравнение животных:** Например: *«В чем разница между гепардом и леопардом?»* или *«Сравни льва и волка»*.
2. **Красная книга:** *«Какие редкие животные охраняются в Узбекистане?»*
3. **Голоса и повадки:** Как звучит беркут, как охотится снежный барс и многое другое!""",
        "en": """🌿 **Hello! I am Animora AI — your wildlife & zoological intelligence assistant.**
I can assist you with:
1. **Species Comparisons:** e.g., *'What is the difference between a cheetah and a leopard?'* or *'Compare lion and wolf.'*
2. **Red Data Book:** *'Which endangered animals are protected in Uzbekistan?'*
3. **Animal Sounds & Biology:** Habitats, speed, diets, vocalizations, and remarkable facts!""",
        "fr": """🌿 **Bonjour ! Je suis Animora IA — votre assistant intelligent sur la faune et la zoologie.**
Je peux vous aider sur :
1. **Comparaison des espèces :** Par exemple : *« Quelle est la différence entre un guépard et un léopard ? »*
2. **Livre Rouge :** *« Quelles sont les espèces menacées en Ouzbékistan ? »*
3. **Cris et biologie :** Habitats, vitesses de course, régimes alimentaires et faits insolites !""",
        "uz": """🌿 **Salom! Men Animora AI — hayvonot olami bo'yicha aqlli yordamchingizman.**
Men sizga quyidagi mavzularda yordam bera olaman:
1. **Hayvonlarni solishtirish:** Masalan, *'Gepard bilan qoplon qanday farqlanadi?'* yoki *'Sher bilan bo'ri farqi nima?'*
2. **Qizil kitob:** *'O'zbekiston Qizil kitobiga qaysi hayvonlar kiritilgan?'* yoki *'Qor qoploni maqomi qanday?'*
3. **Ovozlar:** *'Sherning o'kirishi qanchalik uzoqqa eshitiladi?'* yoki *'Burgut qanday qichqiradi?'*
4. **Biologik faktlar:** Yashash muhiti, oziqlanishi, tezligi va kamyob odatlari."""
    }
    return greetings.get(lang, greetings["uz"])

def ask_ai(message: str, lang: str = "uz") -> str:
    key = get_gemini_api_key()
    if key:
        try:
            return call_gemini_api(key, message, lang=lang)
        except Exception as e:
            return fallback_smart_ai(message, lang=lang)
    return fallback_smart_ai(message, lang=lang)
