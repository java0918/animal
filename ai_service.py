import os
import json
import sqlite3
import re
from typing import Dict, Any, List
from database import get_connection, get_all_animals

SYSTEM_PROMPT = """Siz hayvonot olami, zoologiya, O'zbekiston va Xalqaro Qizil kitob bo'yicha ixtisoslashgan mukammal AI yordamchisiz.
Ismingiz: Animore AI.
Vazifangiz: Foydalanuvchilarga hayvonlar, ularning o'xshash turlaridan qanday farqlanishi, yashash tarzi, ovozlari, O'zbekiston Qizil kitobi va IUCN maqomi haqida o'zbek tilida aniq, ravon va qiziqarli javob berish.
Har doim do'stona, ilmiy va tushunarli uslubda javob bering."""

def get_gemini_api_key() -> str:
    # Check env or database settings
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
    # system instruction or prompt context
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

def fallback_smart_ai(message: str) -> str:
    """
    Intelligent Biological Knowledge Engine in Uzbek.
    Matches animal queries, comparisons, red book questions, sounds, and general biology.
    """
    msg_lower = message.lower()
    animals = get_all_animals()
    
    # 1. Check for animal difference / comparison query
    if any(k in msg_lower for k in ["farq", "farqi", "farqlanadi", "taqqosla", "solishtir", "ajrat"]):
        for a in animals:
            name_low = a["name_uz"].lower()
            sim_low = a["similar_species"].lower()
            if any(part in msg_lower for part in name_low.split()[:2]) or any(part in msg_lower for part in sim_low.split()):
                return f"""🦁 **{a['name_uz']} va unga o'xshash turlar o'rtasidagi asosiy farqlar:**\n\n{a['differences']}\n\n📌 **Yashash muhiti:** {a['habitat']}\n⚡ **Harakat tezligi:** {a['speed']}"""
                
        if "gepard" in msg_lower or "qoplon" in msg_lower or "leopard" in msg_lower:
            return """🐆 **Gepard va Qoplon (Leopard) o'rtasidagi asosiy farqlar:**
1. **Dog'lari:** Gepard tanasidagi dog'lar yakka-yakka yaxlit qora nuqtalardir. Leopardda esa gulsimon, markazi ochiq 'rozetka' dog'lar bo'ladi.
2. **Yuzdagi chiziq:** Gepardning ko'zlaridan labiga qadar qora 'ko'z yoshi chizig'i' o'tgan (quyosh nuridan himoya). Leopardda bunday chiziq yo'q.
3. **Tirnoqlari:** Gepardning tirnoqlari itlarnikidek ichkariga to'liq kirmaydi va yerga tiraladi; leopard tirnoqlarini to'liq yashira oladi.
4. **Xulq-atvori:** Leopard o'ljasini baland daraxtlarga olib chiqadi; gepard esa faqat tekislikda katta tezlikda (120 km/soat) quvlab ovlaydi."""

    # 2. Check for Red Book query
    if any(k in msg_lower for k in ["qizil kitob", "red book", "iucn", "yo'qolib", "yoqolib", "muhofaza", "noyob"]):
        red_animals = [a for a in animals if a["uz_red_book_status"] != "Kiritilmagan" or a["iucn_status"] in ["CR", "EN", "VU"]]
        response_lines = ["📕 **O'zbekiston va Xalqaro Qizil kitobga kiritilgan muhim turlar:**\n"]
        for ra in red_animals[:6]:
            response_lines.append(f"• **{ra['name_uz']}** ({ra['name_latin']}):\n  - O'zbekiston Qizil kitobi: `{ra['uz_red_book_status']}`\n  - Xalqaro IUCN maqomi: `{ra['iucn_status']}`\n  - Izoh: {ra['uz_red_book_desc']}")
        response_lines.append("\n💡 *Saytimizning 'Qizil Kitob' maxsus bo'limida barcha xavf ostidagi hayvonlar va ularni muhofaza qilish choralari to'liq ko'rsatilgan.*")
        return "\n".join(response_lines)

    # 3. Check for animal sounds query
    if any(k in msg_lower for k in ["ovoz", "tovush", "sayrash", "o'kir", "okir", "uvilla"]):
        for a in animals:
            if any(w in msg_lower for w in a["name_uz"].lower().split()[:2]):
                return f"""🔊 **{a['name_uz']}ning ovozi haqida:**\n\n{a['sound_description']}\n\nSiz ushbu hayvon kartasidagi **'Ovozni tinglash'** tugmasini bosib, uning haqiqiy tovushini audio to'lqinlar bilan eshitishingiz mumkin!"""
        return """🎵 **Hayvonlarning ovozlari haqida:**
Har bir hayvon o'ziga xos akustik signallar orqali muloqot qiladi:
• **Sher:** Haybatli o'kirishi 8 km masofagacha eshitiladi.
• **Qaldirg'och:** Quvnoq jilvalanuvchi chuldirash va hushtak ohanglari.
• **Bo'ri:** Uzoq masofali mungli uvillash (stayni to'plash uchun).
• **Burgut:** Tog'larda aks beruvchi o'tkir qichqiriq.
• **Delfin:** Ultratovushli exolokatsiya chertishlari va hushtaklar.

Istalgan hayvon kartasida ovoz belgisini bosing!"""

    # 4. Check for specific animal info
    for a in animals:
        name_parts = a["name_uz"].lower().split()
        if any(part in msg_lower for part in name_parts if len(part) > 2) or a["name_latin"].lower() in msg_lower or a["name_en"].lower() in msg_lower:
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
    return f"""🌿 **Salom! Men Animore AI — hayvonot olami bo'yicha aqlli yordamchingizman.**

Men sizga quyidagi mavzularda yordam bera olaman:
1. **Hayvonlarni solishtirish:** Masalan, *'Gepard bilan qoplon qanday farqlanadi?'* yoki *'Sher bilan yo'lbars farqi nima?'*
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
            # Fallback to local intelligent engine
            return fallback_smart_ai(message)
    return fallback_smart_ai(message)
