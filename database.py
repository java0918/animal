import sqlite3
import json
import os
import shutil
import re
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "fauna.db")

def normalize_uz_text(text: Optional[str]) -> str:
    """Normalize Uzbek text: remove all variations of apostrophes/backticks and lowercase."""
    if not text:
        return ""
    cleaned = re.sub(r"['`’ʻʼ‘´]", "", str(text).lower())
    return cleaned.strip()

def is_serverless_env():
    return bool(
        os.environ.get("VERCEL") or 
        os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or 
        os.environ.get("NOW_REGION") or
        not os.access(os.path.dirname(os.path.abspath(__file__)), os.W_OK)
    )

def get_connection():
    if is_serverless_env():
        tmp_db = "/tmp/fauna.db"
        if not os.path.exists(tmp_db):
            os.makedirs(os.path.dirname(tmp_db), exist_ok=True)
            if os.path.exists(DB_PATH):
                try:
                    shutil.copyfile(DB_PATH, tmp_db)
                except Exception as e:
                    print(f"DB copy error: {e}")
        target_db = tmp_db
    else:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        target_db = DB_PATH

    conn = sqlite3.connect(target_db, timeout=30.0)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    conn.create_function("NORMALIZE_UZ", 1, normalize_uz_text)
    conn.row_factory = sqlite3.Row
    return conn



def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Animals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_uz TEXT NOT NULL,
        name_latin TEXT NOT NULL,
        name_en TEXT NOT NULL,
        category TEXT NOT NULL,
        class_name TEXT NOT NULL,
        diet TEXT NOT NULL,
        habitat TEXT NOT NULL,
        lifespan TEXT,
        speed TEXT,
        weight TEXT,
        description TEXT NOT NULL,
        uz_red_book_status TEXT NOT NULL,
        uz_red_book_desc TEXT,
        iucn_status TEXT NOT NULL,
        iucn_desc TEXT,
        similar_species TEXT NOT NULL,
        differences TEXT NOT NULL,
        sound_file TEXT,
        sound_description TEXT,
        sound_type TEXT DEFAULT 'roar',
        image_url TEXT NOT NULL,
        gallery_images TEXT,
        fun_facts TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Users table (for Google Sign-In & Admins)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        picture TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # Quizzes table (1000 questions bank)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        question_kaa TEXT,
        question_ru TEXT,
        question_en TEXT,
        sound_type TEXT DEFAULT 'roar',
        audio_url TEXT,
        options TEXT NOT NULL,
        options_kaa TEXT,
        options_ru TEXT,
        options_en TEXT,
        correct INTEGER NOT NULL,
        explanation TEXT NOT NULL,
        explanation_kaa TEXT,
        explanation_ru TEXT,
        explanation_en TEXT,
        category TEXT,
        animal_id INTEGER
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_quizzes_id ON quizzes(id)")
    
    conn.commit()
    
    cursor.execute("SELECT count(*) FROM animals")
    row = cursor.fetchone()
    count = row[0] if row else 0
    conn.close()
    
    if count == 0:
        try:
            from seed_data import seed
            seed()
        except Exception as e:
            print(f"Auto-seed warning: {e}")


def get_animals_count(category: Optional[str] = None, red_book_only: bool = False, search: Optional[str] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM animals WHERE 1=1"
    params = []
    if category and category != 'all':
        query += " AND category = ?"
        params.append(category)
    if red_book_only:
        query += " AND (uz_red_book_status != 'Kiritilmagan' OR iucn_status IN ('CR', 'EN', 'VU'))"
    if search:
        cleaned_search = normalize_uz_text(search)
        query += " AND (NORMALIZE_UZ(name_uz) LIKE ? OR NORMALIZE_UZ(name_latin) LIKE ? OR NORMALIZE_UZ(name_en) LIKE ? OR NORMALIZE_UZ(description) LIKE ?)"
        s = f"%{cleaned_search}%"
        params.extend([s, s, s, s])
    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_animals(category: Optional[str] = None, red_book_only: bool = False, search: Optional[str] = None, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM animals WHERE 1=1"
    params = []
    
    if category and category != 'all':
        query += " AND category = ?"
        params.append(category)
        
    if red_book_only:
        query += " AND (uz_red_book_status != 'Kiritilmagan' OR iucn_status IN ('CR', 'EN', 'VU'))"
        
    if search:
        cleaned_search = normalize_uz_text(search)
        query += " AND (NORMALIZE_UZ(name_uz) LIKE ? OR NORMALIZE_UZ(name_latin) LIKE ? OR NORMALIZE_UZ(name_en) LIKE ? OR NORMALIZE_UZ(description) LIKE ?)"
        s = f"%{cleaned_search}%"
        params.extend([s, s, s, s])
        
    query += " ORDER BY id ASC"
    if limit is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    results = []
    for r in rows:
        item = dict(r)
        if item.get("gallery_images"):
            try:
                item["gallery_images"] = json.loads(item["gallery_images"])
            except:
                item["gallery_images"] = []
        else:
            item["gallery_images"] = []
        if item.get("fun_facts"):
            try:
                item["fun_facts"] = json.loads(item["fun_facts"])
            except:
                item["fun_facts"] = []
        else:
            item["fun_facts"] = []
        results.append(item)
        
    conn.close()
    return results

def get_animal_by_id(animal_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animals WHERE id = ?", (animal_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    if item.get("gallery_images"):
        try:
            item["gallery_images"] = json.loads(item["gallery_images"])
        except:
            item["gallery_images"] = []
    else:
        item["gallery_images"] = []
    if item.get("fun_facts"):
        try:
            item["fun_facts"] = json.loads(item["fun_facts"])
        except:
            item["fun_facts"] = []
    else:
        item["fun_facts"] = []
    return item

def insert_animal(data: Dict[str, Any]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    gallery = json.dumps(data.get("gallery_images", []))
    facts = json.dumps(data.get("fun_facts", []))
    
    cursor.execute("""
    INSERT INTO animals (
        name_uz, name_latin, name_en, category, class_name, diet, habitat,
        lifespan, speed, weight, description, uz_red_book_status, uz_red_book_desc,
        iucn_status, iucn_desc, similar_species, differences, sound_file,
        sound_description, sound_type, image_url, gallery_images, fun_facts
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name_uz"),
        data.get("name_latin"),
        data.get("name_en", ""),
        data.get("category", "Sutemizuvchilar"),
        data.get("class_name", "Mammalia"),
        data.get("diet", "Yirtqich"),
        data.get("habitat", "O'rmon"),
        data.get("lifespan", ""),
        data.get("speed", ""),
        data.get("weight", ""),
        data.get("description", ""),
        data.get("uz_red_book_status", "Kiritilmagan"),
        data.get("uz_red_book_desc", ""),
        data.get("iucn_status", "LC"),
        data.get("iucn_desc", ""),
        data.get("similar_species", ""),
        data.get("differences", ""),
        data.get("sound_file", ""),
        data.get("sound_description", ""),
        data.get("sound_type", "roar"),
        data.get("image_url", ""),
        gallery,
        facts
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_animal(animal_id: int, data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    
    gallery = json.dumps(data.get("gallery_images", [])) if isinstance(data.get("gallery_images"), list) else data.get("gallery_images", "[]")
    facts = json.dumps(data.get("fun_facts", [])) if isinstance(data.get("fun_facts"), list) else data.get("fun_facts", "[]")
    
    cursor.execute("""
    UPDATE animals SET
        name_uz = ?, name_latin = ?, name_en = ?, category = ?, class_name = ?, diet = ?, habitat = ?,
        lifespan = ?, speed = ?, weight = ?, description = ?, uz_red_book_status = ?, uz_red_book_desc = ?,
        iucn_status = ?, iucn_desc = ?, similar_species = ?, differences = ?, sound_file = ?,
        sound_description = ?, sound_type = ?, image_url = ?, gallery_images = ?, fun_facts = ?
    WHERE id = ?
    """, (
        data.get("name_uz"),
        data.get("name_latin"),
        data.get("name_en", ""),
        data.get("category", "Sutemizuvchilar"),
        data.get("class_name", "Mammalia"),
        data.get("diet", "Yirtqich"),
        data.get("habitat", "O'rmon"),
        data.get("lifespan", ""),
        data.get("speed", ""),
        data.get("weight", ""),
        data.get("description", ""),
        data.get("uz_red_book_status", "Kiritilmagan"),
        data.get("uz_red_book_desc", ""),
        data.get("iucn_status", "LC"),
        data.get("iucn_desc", ""),
        data.get("similar_species", ""),
        data.get("differences", ""),
        data.get("sound_file", ""),
        data.get("sound_description", ""),
        data.get("sound_type", "roar"),
        data.get("image_url", ""),
        gallery,
        facts,
        animal_id
    ))
    conn.commit()
    conn.close()

def delete_animal(animal_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
    conn.commit()
    conn.close()

def get_or_create_user(google_id: str, email: str, name: str, picture: str, role: str = 'user') -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? OR google_id = ?", (email, google_id))
    row = cursor.fetchone()
    if row:
        user = dict(row)
        cursor.execute("UPDATE users SET name = ?, picture = ?, role = ? WHERE id = ?", (name, picture, role, user["id"]))
        conn.commit()
        conn.close()
        user["name"] = name
        user["picture"] = picture
        user["role"] = role
        return user
    else:
        cursor.execute("""
        INSERT INTO users (google_id, email, name, picture, role)
        VALUES (?, ?, ?, ?, ?)
        """, (google_id, email, name, picture, role))
        user_id = cursor.lastrowid
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        new_user = dict(cursor.fetchone())
        conn.close()
        return new_user


def get_all_users() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name, picture, role, created_at FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    users = [dict(r) for r in rows]
    conn.close()
    return users

def get_stats() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM animals")
    total_animals = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM animals WHERE uz_red_book_status != 'Kiritilmagan' OR iucn_status IN ('CR', 'EN', 'VU')")
    red_book_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT category) FROM animals")
    categories_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_animals": total_animals,
        "red_book_count": red_book_count,
        "categories_count": categories_count,
        "users_count": users_count
    }


def get_quizzes_total_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM quizzes")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_random_quizzes(count: int = 20, exclude_ids: Optional[List[int]] = None, lang: str = "uz") -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    exclude_clean = []
    if exclude_ids:
        for x in exclude_ids:
            try:
                exclude_clean.append(int(x))
            except (ValueError, TypeError):
                pass
                
    results = []
    # 1. Try to fetch from questions NOT seen by user
    if exclude_clean:
        placeholders = ",".join(["?"] * len(exclude_clean))
        cursor.execute(f"SELECT * FROM quizzes WHERE id NOT IN ({placeholders}) ORDER BY RANDOM() LIMIT ?", (*exclude_clean, count))
        results = [dict(r) for r in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM quizzes ORDER BY RANDOM() LIMIT ?", (count,))
        results = [dict(r) for r in cursor.fetchall()]
        
    # 2. If unseen questions are fewer than count (e.g. user answered 990 questions), supplement from remaining
    if len(results) < count:
        needed = count - len(results)
        chosen_ids = [r["id"] for r in results]
        if chosen_ids:
            sub_placeholders = ",".join(["?"] * len(chosen_ids))
            cursor.execute(f"SELECT * FROM quizzes WHERE id NOT IN ({sub_placeholders}) ORDER BY RANDOM() LIMIT ?", (*chosen_ids, needed))
        else:
            cursor.execute("SELECT * FROM quizzes ORDER BY RANDOM() LIMIT ?", (needed,))
        for r in cursor.fetchall():
            results.append(dict(r))
            
    conn.close()
    
    # 3. Format according to requested language
    formatted = []
    for q in results:
        q_text = q.get(f"question_{lang}") or q["question"]
        expl_text = q.get(f"explanation_{lang}") or q["explanation"]
        
        opts_raw = q.get(f"options_{lang}") or q["options"]
        opts = []
        if isinstance(opts_raw, str):
            try:
                opts = json.loads(opts_raw)
            except Exception:
                opts = []
        elif isinstance(opts_raw, list):
            opts = opts_raw
            
        if not opts:
            try:
                opts = json.loads(q["options"])
            except Exception:
                opts = ["Variant A", "Variant B", "Variant C", "Variant D"]
                
        formatted.append({
            "id": q["id"],
            "question": q_text,
            "options": opts,
            "correct": q["correct"],
            "explanation": expl_text,
            "soundType": q.get("sound_type", "roar"),
            "audioUrl": q.get("audio_url", ""),
            "category": q.get("category", "")
        })
        
    return formatted
