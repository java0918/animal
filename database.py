import sqlite3
import json
import os
import shutil
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "fauna.db")

def get_connection():
    target_db = DB_PATH
    if os.environ.get("VERCEL"):
        tmp_db = "/tmp/fauna.db"
        if not os.path.exists(tmp_db):
            if os.path.exists(DB_PATH):
                shutil.copyfile(DB_PATH, tmp_db)
            else:
                os.makedirs(os.path.dirname(tmp_db), exist_ok=True)
        target_db = tmp_db
    else:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(target_db, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
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
    
    conn.commit()
    
    cursor.execute("SELECT count(*) FROM animals")
    row = cursor.fetchone()
    count = row[0] if row else 0
    conn.close()
    
    if count == 0:
        try:
            from seed_data import seed_database
            seed_database()
        except Exception as e:
            print(f"Auto-seed warning: {e}")


def get_all_animals(category: Optional[str] = None, red_book_only: bool = False, search: Optional[str] = None) -> List[Dict[str, Any]]:
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
        query += " AND (name_uz LIKE ? OR name_latin LIKE ? OR name_en LIKE ? OR description LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s, s])
        
    query += " ORDER BY id ASC"
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
