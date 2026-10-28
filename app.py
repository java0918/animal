import os
import json
import uuid
import shutil
import urllib.parse
from typing import Optional, List
import hashlib
from fastapi import FastAPI, Request, Response, Form, UploadFile, File, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
import aiofiles

from database import (
    init_db, get_all_animals, get_animals_count, get_animal_by_id, insert_animal,
    update_animal, delete_animal, get_or_create_user, get_all_users,
    get_stats, get_connection, get_random_quizzes, get_quizzes_total_count,
    register_user_credentials, authenticate_user_credentials, check_username_exists
)
from ai_service import ask_ai
from audio_resolver import resolve_animal_audio
from translations import (
    SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, get_translation,
    localize_animal, localize_animals_list
)

app = FastAPI(title="Zooventure — Hayvonot Olami Portali")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

is_serverless = bool(
    os.environ.get("VERCEL") or 
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or 
    os.environ.get("NOW_REGION") or 
    not os.access(BASE_DIR, os.W_OK)
)

if is_serverless:
    UPLOAD_ROOT = "/tmp/uploads"
else:
    UPLOAD_ROOT = os.path.join(STATIC_DIR, "uploads")

UPLOAD_IMG_DIR = os.path.join(UPLOAD_ROOT, "images")
UPLOAD_AUD_DIR = os.path.join(UPLOAD_ROOT, "audio")

try:
    os.makedirs(UPLOAD_ROOT, exist_ok=True)
    os.makedirs(UPLOAD_IMG_DIR, exist_ok=True)
    os.makedirs(UPLOAD_AUD_DIR, exist_ok=True)
except OSError:
    pass

if is_serverless:
    if not os.path.exists(UPLOAD_ROOT):
        try:
            os.makedirs(UPLOAD_ROOT, exist_ok=True)
        except OSError:
            pass
    if os.path.exists(UPLOAD_ROOT):
        app.mount("/static/uploads", StaticFiles(directory=UPLOAD_ROOT), name="static_uploads")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Helper for current user from cookie
def get_current_user(request: Request) -> Optional[dict]:
    session_cookie = request.cookies.get("zooventure_session") or request.cookies.get("animind_session") or request.cookies.get("animora_session") or request.cookies.get("animore_session") or request.cookies.get("fauna_session")
    if not session_cookie:
        return None
    try:
        raw_val = urllib.parse.unquote(session_cookie)
        user_data = json.loads(raw_val)
        return user_data
    except Exception:
        return None

# Helper for current language
def get_current_lang(request: Request) -> str:
    lang_param = request.query_params.get("lang")
    if lang_param and lang_param in SUPPORTED_LANGUAGES:
        return lang_param
    lang_cookie = request.cookies.get("zooventure_lang") or request.cookies.get("animind_lang") or request.cookies.get("animora_lang")
    if lang_cookie and lang_cookie in SUPPORTED_LANGUAGES:
        return lang_cookie
    return DEFAULT_LANGUAGE

def get_base_context(request: Request, current_lang: str) -> dict:
    user = get_current_user(request)
    lang_info = SUPPORTED_LANGUAGES.get(current_lang, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE])
    return {
        "request": request,
        "user": user,
        "current_lang": current_lang,
        "current_lang_label": lang_info["native"],
        "current_lang_flag": lang_info["flag"],
        "supported_languages": SUPPORTED_LANGUAGES,
        "t": lambda key, default=None: get_translation(current_lang, key, default)
    }

# Middleware for Closed Website Protection
class ClosedPortalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Public paths: static assets, login page, auth API endpoints, language switch
        public_prefixes = ["/static", "/login", "/api/auth", "/set-lang", "/api/tts"]
        if any(path.startswith(prefix) for prefix in public_prefixes):
            return await call_next(request)
            
        user = get_current_user(request)
        if not user:
            if path.startswith("/api/"):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Sayt yopiq. Avval Google hisob bilan kiring."}
                )
            return RedirectResponse(url="/login?redirect=" + path)
            
        return await call_next(request)

app.add_middleware(ClosedPortalMiddleware)

@app.on_event("startup")
async def startup_event():
    init_db()

# ================= LANGUAGE SWITCH ROUTE =================

@app.get("/set-lang/{lang_code}")
async def set_language(lang_code: str, request: Request):
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    referer = request.headers.get("referer") or "/"
    try:
        parsed = urllib.parse.urlparse(referer)
        qs = urllib.parse.parse_qs(parsed.query)
        qs.pop("lang", None)
        new_query = urllib.parse.urlencode(qs, doseq=True)
        clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        clean_url = "/"
    if not clean_url:
        clean_url = "/"
    res = RedirectResponse(url=clean_url, status_code=303)
    res.set_cookie(key="zooventure_lang", value=lang_code, max_age=86400 * 365, samesite="lax", path="/")
    res.set_cookie(key="animind_lang", value=lang_code, max_age=86400 * 365, samesite="lax", path="/")
    res.set_cookie(key="animora_lang", value=lang_code, max_age=86400 * 365, samesite="lax", path="/")
    return res

# ================= AUTH & LOGIN ROUTES =================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    current_lang = get_current_lang(request)
    user = get_current_user(request)
    if user and user.get("role") == "admin" and not request.query_params.get("switch"):
        return RedirectResponse(url="/admin")
        
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'google_client_id'")
    row = c.fetchone()
    google_client_id = row["value"] if row and row["value"] else ""
    conn.close()
    
    ctx = get_base_context(request, current_lang)
    ctx["google_client_id"] = google_client_id
    ctx["redirect_target"] = request.query_params.get("redirect", "")
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=ctx
    )

@app.post("/api/auth/google")
async def google_auth(request: Request, response: Response):
    try:
        data = await request.json()
        credential = data.get("credential")
        email = data.get("email")
        name = data.get("name")
        picture = data.get("picture")
        sub = data.get("sub", str(uuid.uuid4()))
        
        if credential and not email:
            import base64
            parts = credential.split(".")
            if len(parts) >= 2:
                payload_part = parts[1]
                payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
                decoded = base64.b64decode(payload_part).decode("utf-8")
                user_info = json.loads(decoded)
                email = user_info.get("email")
                name = user_info.get("name", "Foydalanuvchi")
                picture = user_info.get("picture", "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80")
                sub = user_info.get("sub", sub)

        if not email:
            email = f"user_{sub[:8]}@zooventure.uz"
        if not name:
            name = "Tabiat Shaydosi"
        if not picture:
            picture = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80"
            
        role = "user"
        if email.lower() in ["admin@zooventure.uz", "admin@animind.uz", "admin@animora.uz", "admin@fauna.uz", "java0918@gmail.com", "admin@gmail.com"]:
            role = "admin"
            
        user = get_or_create_user(google_id=sub, email=email, name=name, picture=picture, role=role)
        
        res = JSONResponse({"success": True, "user": user})
        cookie_val = urllib.parse.quote(json.dumps(user))
        for k in ["zooventure_session", "animind_session", "animora_session", "fauna_session"]:
            res.set_cookie(key=k, value=cookie_val, httponly=True, max_age=86400 * 30, samesite="lax", path="/")
        return res
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)

@app.post("/api/auth/admin-login")
@app.post("/api/auth/login")
async def admin_login(request: Request, response: Response):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    custom_redirect = data.get("redirect", "").strip()
    
    if not username or not password:
        return JSONResponse({"success": False, "message": "Iltimos, login va parolni kiriting!"}, status_code=400)
        
    auth_res = authenticate_user_credentials(username, password)
    if auth_res.get("success"):
        user = auth_res["user"]
        is_admin = user.get("role") == "admin"
        if custom_redirect:
            redirect_url = custom_redirect
        elif is_admin and username.lower() == "admin":
            redirect_url = "/admin"
        else:
            redirect_url = "/"

        res = JSONResponse({
            "success": True,
            "user": user,
            "role": user.get("role", "admin"),
            "redirect": redirect_url
        })
        cookie_val = urllib.parse.quote(json.dumps(user))
        for k in ["zooventure_session", "animind_session", "animora_session", "fauna_session"]:
            res.set_cookie(key=k, value=cookie_val, httponly=True, max_age=86400 * 30, samesite="lax", path="/")
        return res
    else:
        return JSONResponse({
            "success": False,
            "user_exists": auth_res.get("user_exists", True),
            "message": auth_res.get("message", "Login yoki parol noto'g'ri!")
        }, status_code=401)

@app.post("/api/auth/register")
@app.post("/api/auth/setup-credentials")
async def register_credentials_endpoint(request: Request, response: Response):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip()
    custom_redirect = data.get("redirect", "").strip()
    
    if not username or not password:
        return JSONResponse({"success": False, "message": "Login va parol kiritilishi shart!"}, status_code=400)
        
    reg_res = register_user_credentials(username, password, name=name, role="admin")
    if reg_res.get("success"):
        user = reg_res["user"]
        redirect_url = custom_redirect if custom_redirect else "/"
        res = JSONResponse({
            "success": True,
            "user": user,
            "role": user.get("role", "admin"),
            "redirect": redirect_url,
            "message": "Login va parolingiz muvaffaqiyatli saqlandi!"
        })
        cookie_val = urllib.parse.quote(json.dumps(user))
        for k in ["zooventure_session", "animind_session", "animora_session", "fauna_session"]:
            res.set_cookie(key=k, value=cookie_val, httponly=True, max_age=86400 * 30, samesite="lax", path="/")
        return res
    else:
        return JSONResponse({
            "success": False,
            "message": reg_res.get("message", "Ro'yxatdan o'tishda xatolik!")
        }, status_code=400)

@app.get("/api/auth/check-username")
async def check_username_endpoint(username: str):
    exists = check_username_exists(username)
    return JSONResponse({"exists": exists})

@app.post("/api/auth/demo-login")
async def demo_login(request: Request, response: Response):
    demo_users = [
        {"id": "d1", "name": "Zoolog Tadqiqotchi", "email": "zoolog@zooventure.uz", "picture": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80"},
        {"id": "d2", "name": "Biologiya Talabasi", "email": "talaba@zooventure.uz", "picture": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80"},
        {"id": "d3", "name": "Tabiat Havaskori", "email": "tabiat@zooventure.uz", "picture": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80"}
    ]
    import random
    user_session = random.choice(demo_users)
    user_session["role"] = "user"
    
    get_or_create_user(
        google_id=f"demo-{user_session['id']}",
        email=user_session["email"],
        name=user_session["name"],
        picture=user_session["picture"],
        role="user"
    )
    
    res = JSONResponse({
        "success": True,
        "user": user_session,
        "role": "user",
        "redirect": "/"
    })
    cookie_val = urllib.parse.quote(json.dumps(user_session))
    for k in ["zooventure_session", "animind_session", "animora_session", "fauna_session"]:
        res.set_cookie(key=k, value=cookie_val, httponly=True, max_age=86400 * 7, samesite="lax", path="/")
    return res

@app.get("/logout")
@app.post("/api/auth/logout")
async def logout(response: Response):
    res = RedirectResponse(url="/login")
    for k in ["zooventure_session", "animind_session", "animora_session", "fauna_session"]:
        res.delete_cookie(k, path="/")
    return res

# ================= MAIN PORTAL PAGES =================

@app.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request, 
    category: Optional[str] = None, 
    search: Optional[str] = None,
    page: int = 1
):
    current_lang = get_current_lang(request)
    per_page = 24
    if page < 1:
        page = 1
        
    total_count = get_animals_count(category=category, search=search)
    import math
    total_pages = max(1, math.ceil(total_count / per_page))
    if page > total_pages:
        page = total_pages
        
    offset = (page - 1) * per_page
    animals = get_all_animals(category=category, search=search, limit=per_page, offset=offset)
    localized_animals = localize_animals_list(animals, current_lang)
    stats = get_stats()
    
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    pages_range = list(range(start_page, end_page + 1))
    
    ctx = get_base_context(request, current_lang)
    ctx.update({
        "animals": localized_animals,
        "current_category": category or "all",
        "search_query": search or "",
        "stats": stats,
        "page": page,
        "total_pages": total_pages,
        "total_count": total_count,
        "per_page": per_page,
        "pages_range": pages_range,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
        "start_item": offset + 1 if total_count > 0 else 0,
        "end_item": min(offset + per_page, total_count)
    })
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=ctx
    )

@app.get("/animal/{animal_id}", response_class=HTMLResponse)
async def animal_detail(animal_id: int, request: Request):
    current_lang = get_current_lang(request)
    animal = get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Hayvon topilmadi")
        
    animal = localize_animal(animal, current_lang)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM animals WHERE category = ? AND id != ? LIMIT 4", (animal["category"], animal_id))
    similar_rows = [dict(r) for r in c.fetchall()]
    conn.close()
    similar_animals = [localize_animal(a, current_lang) for a in similar_rows]
    
    ctx = get_base_context(request, current_lang)
    ctx.update({
        "animal": animal,
        "similar_animals": similar_animals
    })
    return templates.TemplateResponse(
        request=request,
        name="animal_detail.html",
        context=ctx
    )

@app.get("/redbook", response_class=HTMLResponse)
async def redbook_page(
    request: Request, 
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1
):
    current_lang = get_current_lang(request)
    per_page = 24
    if page < 1:
        page = 1
        
    total_count = get_animals_count(red_book_only=True, search=search)
    import math
    total_pages = max(1, math.ceil(total_count / per_page))
    if page > total_pages:
        page = total_pages
        
    offset = (page - 1) * per_page
    animals = get_all_animals(red_book_only=True, search=search, limit=per_page, offset=offset)
    localized_animals = localize_animals_list(animals, current_lang)
    
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    pages_range = list(range(start_page, end_page + 1))
    
    ctx = get_base_context(request, current_lang)
    ctx.update({
        "animals": localized_animals,
        "status_filter": status_filter or "all",
        "search_query": search or "",
        "page": page,
        "total_pages": total_pages,
        "total_count": total_count,
        "pages_range": pages_range,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
        "start_item": offset + 1 if total_count > 0 else 0,
        "end_item": min(offset + per_page, total_count)
    })
    return templates.TemplateResponse(
        request=request,
        name="redbook.html",
        context=ctx
    )

@app.get("/compare", response_class=HTMLResponse)
async def compare_page(request: Request, left: Optional[int] = 1, right: Optional[int] = 5):
    current_lang = get_current_lang(request)
    all_animals = localize_animals_list(get_all_animals(limit=150), current_lang)
    
    left_animal = get_animal_by_id(left) or (all_animals[0] if all_animals else None)
    right_animal = get_animal_by_id(right) or (all_animals[1] if len(all_animals) > 1 else None)
    
    if left_animal:
        left_animal = localize_animal(left_animal, current_lang)
    if right_animal:
        right_animal = localize_animal(right_animal, current_lang)
        
    ctx = get_base_context(request, current_lang)
    ctx.update({
        "all_animals": all_animals,
        "left_animal": left_animal,
        "right_animal": right_animal
    })
    return templates.TemplateResponse(
        request=request,
        name="comparison.html",
        context=ctx
    )

@app.get("/ai-chat", response_class=HTMLResponse)
async def ai_chat_page(request: Request):
    current_lang = get_current_lang(request)
    ctx = get_base_context(request, current_lang)
    return templates.TemplateResponse(
        request=request,
        name="ai_chat.html",
        context=ctx
    )

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    current_lang = get_current_lang(request)
    ctx = get_base_context(request, current_lang)
    ctx["total_quiz_pool"] = get_quizzes_total_count()
    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context=ctx
    )


# ================= REAL NEURAL TTS (O'ZBEKCHA OVOZLI O'QISH) =================
_tts_cache = {}
TTS_VOICE_MAP = {
    "uz": "uz-UZ-MadinaNeural",
    "kaa": "uz-UZ-MadinaNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "en": "en-US-JennyNeural",
    "fr": "fr-FR-DeniseNeural"
}

@app.get("/api/tts")
async def api_tts(request: Request, text: str = Query(..., min_length=1, max_length=1500), lang: str = "uz", voice: Optional[str] = None):
    text_clean = text.replace("", '"').strip()
    if not text_clean:
        raise HTTPException(status_code=400, detail="Bo'sh matn")
        
    chosen_voice = voice or TTS_VOICE_MAP.get(lang.lower(), "uz-UZ-MadinaNeural")
    cache_key = hashlib.md5(f"{chosen_voice}:{text_clean}".encode("utf-8")).hexdigest()
    
    if cache_key in _tts_cache:
        return Response(
            content=_tts_cache[cache_key],
            media_type="audio/mpeg",
            headers={
                "Cache-Control": "public, max-age=604800, immutable",
                "Content-Disposition": "inline; filename=speech.mp3"
            }
        )
        
    try:
        import edge_tts
        comm = edge_tts.Communicate(text_clean, chosen_voice, rate="-2%")
        chunks = []
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        audio_bytes = b"".join(chunks)
        if audio_bytes:
            if len(_tts_cache) > 500:
                _tts_cache.clear()
            _tts_cache[cache_key] = audio_bytes
            return Response(
                content=audio_bytes,
                media_type="audio/mpeg",
                headers={
                    "Cache-Control": "public, max-age=604800, immutable",
                    "Content-Disposition": "inline; filename=speech.mp3"
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Audio generatsiya qilinmadi")
    except Exception as e:
        print(f"TTS xatosi: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quiz/session")
@app.post("/api/quiz/session")
async def api_quiz_session(request: Request):
    current_lang = get_current_lang(request)
    seen_raw = request.query_params.get("seen_ids", "")
    if not seen_raw and request.method == "POST":
        try:
            body = await request.json()
            seen_raw = body.get("seen_ids", [])
        except Exception:
            seen_raw = []
    
    exclude_ids = []
    if isinstance(seen_raw, str):
        exclude_ids = [int(x.strip()) for x in seen_raw.split(",") if x.strip().isdigit()]
    elif isinstance(seen_raw, list):
        exclude_ids = [int(x) for x in seen_raw if str(x).isdigit()]
        
    quizzes = get_random_quizzes(count=20, exclude_ids=exclude_ids, lang=current_lang)
    total_pool = get_quizzes_total_count()
    
    return JSONResponse({
        "success": True,
        "total_pool": total_pool,
        "session_count": len(quizzes),
        "seen_count": len(exclude_ids),
        "quizzes": quizzes
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    current_lang = get_current_lang(request)
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login?redirect=/admin")
        
    animals = get_all_animals(limit=100)
    users = get_all_users()
    stats = get_stats()
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM settings")
    settings_rows = c.fetchall()
    settings_dict = {row["key"]: row["value"] for row in settings_rows}
    conn.close()
    
    ctx = get_base_context(request, current_lang)
    ctx.update({
        "animals": animals,
        "users": users,
        "stats": stats,
        "settings": settings_dict
    })
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context=ctx
    )

# ================= API ENDPOINTS =================

@app.post("/api/ai/ask")
async def api_ai_ask(request: Request):
    body = await request.json()
    message = body.get("message", "").strip()
    lang = body.get("lang") or get_current_lang(request)
    if not message:
        no_msg = {
            "uz": "Iltimos, biror savol kiriting.",
            "kaa": "Iltimos, biror soraw kiritiń.",
            "ru": "Пожалуйста, введите вопрос.",
            "en": "Please enter a question.",
            "fr": "Veuillez entrer une question."
        }.get(lang, "Iltimos, biror savol kiriting.")
        return JSONResponse({"answer": no_msg})
    answer = ask_ai(message, lang=lang)
    return JSONResponse({"answer": answer})

@app.post("/api/upload")
async def api_upload(
    file: UploadFile = File(...),
    file_type: str = Form("image")
):
    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex[:10]}{ext}"
    
    if file_type == "audio":
        dest_dir = UPLOAD_AUD_DIR
        url_prefix = "/static/uploads/audio/"
    else:
        dest_dir = UPLOAD_IMG_DIR
        url_prefix = "/static/uploads/images/"
        
    dest_path = os.path.join(dest_dir, unique_name)
    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
        
    return JSONResponse({"url": f"{url_prefix}{unique_name}"})

@app.get("/api/animals/{animal_id}")
async def api_get_animal(animal_id: int, request: Request):
    lang = get_current_lang(request)
    animal = get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Hayvon topilmadi")
    animal = localize_animal(animal, lang)
    return JSONResponse(animal)

@app.post("/api/animals")
async def api_create_animal(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Faqat admin qo'sha oladi")
        
    data = await request.json()
    new_id = insert_animal(data)
    return JSONResponse({"success": True, "id": new_id})

@app.put("/api/animals/{animal_id}")
async def api_update_animal(animal_id: int, request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
        
    data = await request.json()
    update_animal(animal_id, data)
    return JSONResponse({"success": True})

@app.delete("/api/animals/{animal_id}")
async def api_delete_animal(animal_id: int, request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
        
    delete_animal(animal_id)
    return JSONResponse({"success": True})

@app.post("/api/settings")
async def api_save_settings(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
        
    body = await request.json()
    conn = get_connection()
    c = conn.cursor()
    for key, val in body.items():
        c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(val)))
    conn.commit()
    conn.close()
    return JSONResponse({"success": True})

@app.post("/api/github/push")
async def api_github_push(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
        
    body = await request.json()
    token = body.get("token", "").strip()
    if not token:
        return JSONResponse({"success": False, "message": "GitHub token kiritilmadi!"}, status_code=400)
        
    from dulwich import porcelain
    auth_url = f"https://java0918:{token}@github.com/java0918/animal.git"
    try:
        porcelain.push(BASE_DIR, auth_url, "refs/heads/main:refs/heads/main", force=True)
        return JSONResponse({"success": True, "message": "Barcha kodlar muvaffaqiyatli GitHub ga yuklandi!"})
    except Exception as e:
        return JSONResponse({"success": False, "message": f"GitHub xatosi: {str(e)}"}, status_code=500)


@app.get("/api/audio/resolve")
async def api_resolve_audio(scientific_name: Optional[str] = None, name_uz: Optional[str] = None, category: Optional[str] = None):
    res = resolve_animal_audio(scientific_name=scientific_name, name_uz=name_uz or "", category=category or "")
    return JSONResponse(res)

@app.get("/api/animals/{animal_id}/audio")
async def api_animal_audio(animal_id: int):
    animal = get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Hayvon topilmadi")
    audio_url = animal.get("audioUrl") or animal.get("audio_url") or animal.get("sound_file")
    if not audio_url:
        resolved = resolve_animal_audio(animal.get("name_latin"), animal.get("name_uz"), animal.get("category"))
        audio_url = resolved.get("audioUrl")
    return JSONResponse({
        "id": animal["id"],
        "name_uz": animal.get("name_uz"),
        "name_latin": animal.get("name_latin"),
        "audioUrl": audio_url,
        "soundType": animal.get("sound_type", "roar"),
        "soundDescription": animal.get("sound_description", "Tabiiy jonli tovush")
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
