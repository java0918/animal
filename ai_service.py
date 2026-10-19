import os
import json
import sqlite3
import re
from typing import Dict, Any, List, Optional
from database import get_connection, get_all_animals, normalize_uz_text

SYSTEM_PROMPT = """Siz hayvonot olami, zoologiya, O'zbekiston va Xalqaro Qizil kitob bo'yicha ixtisoslashgan mukammal AI yordamchisiz.
Ismingiz: Animora AI.
Vazifangiz: Foydalanuvchilarga hayvonlar, ularning o'xshash turlaridan qanday farqlanishi, yashash tarzi, ovozlari, O'zbekiston Qizil kitobi va IUCN maqomi haqida o'zbek tilida aniq, ravon va qiziqarli javob berish.
Har doim do'stona, ilmiy va tushunarli uslubda javob bering."""

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

def call_gemini_api(api_key: str, message: str, history: List[Dict[str, str]] = None) -> str:
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    contents = []
    contents.append({
        "role": "user",
        "parts": [{"text": SYSTEM_PROMPT + "\n\nSavol: " + message}]
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
    """Extract normalized keywords for matching an animal."""
    tokens = set()
    norm_uz = normalize_uz_text(animal.get("name_uz", ""))
    words = re.findall(r'[a-z0-9]+', norm_uz)
    for w in words:
        if len(w) > 2 and w not in ["yovvoyi", "qum", "chol", "orta", "osiyo", "tur", "daryo"]:
            tokens.add(w)
            
    norm_latin = normalize_uz_text(animal.get("name_latin", ""))
    for w in re.findall(r'[a-z0-9]+', norm_latin):
        if len(w) > 3:
            tokens.add(w)

    norm_en = normalize_uz_text(animal.get("name_en", ""))
    for w in re.findall(r'[a-z0-9]+', norm_en):
        if len(w) > 3:
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

def fallback_smart_ai(message: str) -> str:
    """
    Intelligent Biological Knowledge Engine in Uzbek.
    Matches animal queries, comparisons, red book questions, sounds, and general biology.
    """
    norm_msg = normalize_uz_text(message)
    animals = get_all_animals()
    matched_animals = _find_matching_animals(norm_msg, animals)
    
    # 1. Check for animal difference / comparison query
    is_compare = any(k in norm_msg for k in ["farq", "farqi", "farqlanadi", "taqqosla", "solishtir", "ajrat", "solishtirilsa"])
    
    if is_compare:
        if len(matched_animals) >= 2:
            a1, a2 = matched_animals[0], matched_animals[1]
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
{a1['differences']}

💡 *Batafsil solishtirish uchun saytimizning 'Turlarni Taqqoslash' bo'limiga kiring.*"""

        elif len(matched_animals) == 1:
            a = matched_animals[0]
            return f"""🦁 **{a['name_uz']} va unga o'xshash turlar o'rtasidagi asosiy farqlar:**

{a['differences']}

📌 **Yashash muhiti:** {a['habitat']}
🥩 **Oziqlanishi:** {a['diet']}
⚡ **Harakat tezligi:** {a['speed']} | ⚖️ **Vazni:** {a['weight']}"""

        if any(w in norm_msg for w in ["gepard", "qoplon", "leopard"]):
            return """🐆 **Gepard va Qoplon (Leopard) o'rtasidagi asosiy farqlar:**
1. **Dog'lari:** Gepard tanasidagi dog'lar yakka-yakka yaxlit qora nuqtalardir. Leopardda esa gulsimon, markazi ochiq 'rozetka' dog'lar bo'ladi.
2. **Yuzdagi chiziq:** Gepardning ko'zlaridan labiga qadar qora 'ko'z yoshi chizig'i' o'tgan (quyosh nuridan himoya). Leopardda bunday chiziq yo'q.
3. **Tirnoqlari:** Gepardning tirnoqlari itlarnikidek ichkariga to'liq kirmaydi va yerga tiraladi; leopard tirnoqlarini to'liq yashira oladi.
4. **Xulq-atvori:** Leopard o'ljasini baland daraxtlarga olib chiqadi; gepard esa faqat tekislikda katta tezlikda (120 km/soat) quvlab ovlaydi."""

    # 2. Check for Red Book query
    if any(k in norm_msg for k in ["qizil kitob", "red book", "iucn", "yoqolib", "muhofaza", "noyob", "xavf"]):
        red_animals = [a for a in animals if a["uz_red_book_status"] != "Kiritilmagan" or a["iucn_status"] in ["CR", "EN", "VU"]]
        response_lines = ["📕 **O'zbekiston va Xalqaro Qizil kitobga kiritilgan muhim turlar:**\n"]
        for ra in red_animals[:6]:
            response_lines.append(f"• **{ra['name_uz']}** ({ra['name_latin']}):\n  - O'zbekiston Qizil kitobi: `{ra['uz_red_book_status']}`\n  - Xalqaro IUCN maqomi: `{ra['iucn_status']}`\n  - Izoh: {ra['uz_red_book_desc']}")
        response_lines.append("\n💡 *Saytimizning 'Qizil Kitob' maxsus bo'limida barcha xavf ostidagi hayvonlar va ularni muhofaza qilish choralari to'liq ko'rsatilgan.*")
        return "\n".join(response_lines)

    # 3. Check for animal sounds query
    if any(k in norm_msg for k in ["ovoz", "tovush", "sayrash", "okir", "uvilla", "chuldirash", "qichqir"]):
        if matched_animals:
            a = matched_animals[0]
            return f"""🔊 **{a['name_uz']}ning ovozi haqida:**

{a['sound_description']}

Siz ushbu hayvon kartasidagi **'Ovozni tinglash'** tugmasini bosib, uning haqiqiy tovushini audio to'lqinlar bilan eshitishingiz mumkin!"""
        return """🎵 **Hayvonlarning ovozlari haqida:**
Har bir hayvon o'ziga xos akustik signallar orqali muloqot qiladi:
• **Sher:** Haybatli o'kirishi 8 km masofagacha eshitiladi.
• **Qaldirg'och:** Quvnoq jilvalanuvchi chuldirash va hushtak ohanglari.
• **Bo'ri:** Uzoq masofali mungli uvillash (stayni to'plash uchun).
• **Burgut:** Tog'larda aks beruvchi o'tkir qichqiriq.
• **Delfin:** Ultratovushli exolokatsiya chertishlari va hushtaklar.

Istalgan hayvon kartasida ovoz belgisini bosing!"""

    # 4. Check for specific animal info
    if matched_animals:
        a = matched_animals[0]
        facts = "\n".join([f"  - {f}" for f in a.get("fun_facts", [])])
        return f"""🐾 **{a['name_uz']} ({a['name_latin']}) haqida to'liq ma'lumot:**

📖 **Tavsifi:** {a['description']}
🌿 **Yashash joyi:** {a['habitat']}
🥩 **Oziqlanishi:** {a['diet']}
⚡ **Tezligi:** {a['speed']} | ⚖️ **Vazni:** {a['weight']} | ⏳ **Umri:** {a['lifespan']}

📕 **Qizil kitob maqomi:**
• O'zbekiston Qizil kitobi: `{a['uz_red_book_status']}` ({a['uz_red_book_desc']})
• IUCN xalqaro: `{a['iucn_status']}` ({a['iucn_desc']})

🔍 **O'xshash turlaridan farqi:**
{a['differences']}

✨ **Qiziqarli faktlar:**
{facts}"""

    # 5. General intelligent assistant response
    return f"""🌿 **Salom! Men Animora AI — hayvonot olami bo'yicha aqlli yordamchingizman.**

Men sizga quyidagi mavzularda yordam bera olaman:
1. **Hayvonlarni solishtirish:** Masalan, *'Gepard bilan qoplon qanday farqlanadi?'* yoki *'Sher bilan bo'ri farqi nima?'*
2. **Qizil kitob:** *'O'zbekiston Qizil kitobiga qaysi hayvonlar kiritilgan?'* yoki *'Qor qoploni maqomi qanday?'*
3. **Ovozlar:** *'Sherning o'kirishi qanchalik uzoqqa eshitiladi?'* yoki *'Qaldirg'och qanday sayraydi?'*
4. **Biologik faktlar:** Yashash muhiti, oziqlanishi, tezligi va kamyob odatlari.

Istalgan savolingizni yozing, mamnuniyat bilan javob beraman!"""

def ask_ai(message: str) -> str:
    key = get_gemini_api_key()
    if key:
        try:
            return call_gemini_api(key, message)
        except Exception as e:
            return fallback_smart_ai(message)
    return fallback_smart_ai(message)
