import os
import json
import uuid
import shutil
from typing import Optional, List
from fastapi import FastAPI, Request, Response, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
import aiofiles

from database import (
    init_db, get_all_animals, get_animal_by_id, insert_animal,
    update_animal, delete_animal, get_or_create_user, get_all_users,
    get_stats, get_connection
)
from ai_service import ask_ai

app = FastAPI(title="Fauna & Flora — Hayvonot Olami Portali")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_IMG_DIR = os.path.join(STATIC_DIR, "uploads", "images")
UPLOAD_AUD_DIR = os.path.join(STATIC_DIR, "uploads", "audio")

os.makedirs(UPLOAD_IMG_DIR, exist_ok=True)
os.makedirs(UPLOAD_AUD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

import urllib.parse

# Helper for current user from cookie
def get_current_user(request: Request) -> Optional[dict]:
    session_cookie = request.cookies.get("fauna_session")
    if not session_cookie:
        return None
    try:
        raw_val = urllib.parse.unquote(session_cookie)
        user_data = json.loads(raw_val)
        return user_data
    except Exception:
        return None

# Middleware for Closed Website Protection
class ClosedPortalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Public paths: static assets, login page, auth API endpoints
        public_prefixes = ["/static", "/login", "/api/auth"]
        if any(path.startswith(prefix) for prefix in public_prefixes):
            return await call_next(request)
            
        user = get_current_user(request)
        if not user:
            # If API request, return 401
            if path.startswith("/api/"):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Sayt yopiq. Avval Google hisob bilan kiring."}
                )
            # If browser request, redirect to login page
            return RedirectResponse(url="/login?redirect=" + path)
            
        # User is authenticated
        return await call_next(request)

app.add_middleware(ClosedPortalMiddleware)

@app.on_event("startup")
async def startup_event():
    init_db()

# ================= AUTH & LOGIN ROUTES =================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/")
        
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'google_client_id'")
    row = c.fetchone()
    google_client_id = row["value"] if row and row["value"] else ""
    conn.close()
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"google_client_id": google_client_id}
    )

@app.post("/api/auth/google")
async def google_auth(request: Request, response: Response):
    """
    Handle Google OAuth credential or token.
    Accepts credential token or simulated Google payload.
    """
    try:
        data = await request.json()
        credential = data.get("credential")
        # In case demo or custom payload:
        email = data.get("email")
        name = data.get("name")
        picture = data.get("picture")
        sub = data.get("sub", str(uuid.uuid4()))
        
        # If real Google JWT token provided, can decode or parse
        if credential and not email:
            import base64
            # JWT payload is 2nd part
            parts = credential.split(".")
            if len(parts) >= 2:
                payload_part = parts[1]
                padded = payload_part + "=" * (-len(payload_part) % 4)
                decoded = base64.b64decode(padded).decode("utf-8")
                jwt_data = json.loads(decoded)
                email = jwt_data.get("email", "user@gmail.com")
                name = jwt_data.get("name", "Google Foydalanuvchi")
                picture = jwt_data.get("picture", "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80")
                sub = jwt_data.get("sub", str(uuid.uuid4()))

        if not email:
            return JSONResponse({"success": False, "message": "Email topilmadi"}, status_code=400)

        # Check if email is admin
        role = "admin" if email in ["admin@hayvonlar.uz", "shamsiyev@gmail.com"] or "admin" in email.lower() else "user"
        user = get_or_create_user(sub, email, name, picture, role=role)
        
        user_session = {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "picture": user.get("picture") or "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80",
            "role": user["role"]
        }
        
        res = JSONResponse({"success": True, "user": user_session})
        cookie_val = urllib.parse.quote(json.dumps(user_session))
        res.set_cookie(
            key="fauna_session",
            value=cookie_val,
            httponly=True,
            max_age=86400 * 7, # 7 days
            samesite="lax"
        )
        return res
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

@app.post("/api/auth/demo-login")
async def demo_login(request: Request, response: Response):
    """Instant Google login simulation for testing"""
    body = await request.json()
    role = body.get("role", "user")
    
    if role == "admin":
        user_session = {
            "id": 1,
            "email": "admin@hayvonlar.uz",
            "name": "Bosh Administrator",
            "picture": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80",
            "role": "admin"
        }
    else:
        user_session = {
            "id": 2,
            "email": "tadqiqotchi@gmail.com",
            "name": "Azizbek Olimov (Google)",
            "picture": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
            "role": "user"
        }
    
    get_or_create_user(
        google_id=f"demo-{user_session['id']}",
        email=user_session["email"],
        name=user_session["name"],
        picture=user_session["picture"],
        role=user_session["role"]
    )
    
    res = JSONResponse({"success": True, "user": user_session})
    cookie_val = urllib.parse.quote(json.dumps(user_session))
    res.set_cookie(
        key="fauna_session",
        value=cookie_val,
        httponly=True,
        max_age=86400 * 7,
        samesite="lax"
    )
    return res

@app.get("/logout")
@app.post("/api/auth/logout")
async def logout(response: Response):
    res = RedirectResponse(url="/login")
    res.delete_cookie("fauna_session")
    return res

# ================= MAIN PORTAL PAGES =================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, category: Optional[str] = None, search: Optional[str] = None):
    user = get_current_user(request)
    animals = get_all_animals(category=category, search=search)
    stats = get_stats()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
            "animals": animals,
            "current_category": category or "all",
            "search_query": search or "",
            "stats": stats
        }
    )

@app.get("/animal/{animal_id}", response_class=HTMLResponse)
async def animal_detail(animal_id: int, request: Request):
    user = get_current_user(request)
    animal = get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Hayvon topilmadi")
        
    all_animals = get_all_animals()
    similar_animals = [a for a in all_animals if a["id"] != animal_id and a["category"] == animal["category"]][:4]
    
    return templates.TemplateResponse(
        request=request,
        name="animal_detail.html",
        context={
            "user": user,
            "animal": animal,
            "similar_animals": similar_animals
        }
    )

@app.get("/redbook", response_class=HTMLResponse)
async def redbook_page(request: Request, status_filter: Optional[str] = None):
    user = get_current_user(request)
    all_animals = get_all_animals()
    
    # Filter red book animals
    red_animals = []
    for a in all_animals:
        is_uz_red = a["uz_red_book_status"] != "Kiritilmagan"
        is_iucn_red = a["iucn_status"] in ["CR", "EN", "VU"]
        if is_uz_red or is_iucn_red:
            if not status_filter or status_filter == "all" or status_filter in a["uz_red_book_status"] or status_filter == a["iucn_status"]:
                red_animals.append(a)
                
    return templates.TemplateResponse(
        request=request,
        name="redbook.html",
        context={
            "user": user,
            "animals": red_animals,
            "status_filter": status_filter or "all"
        }
    )

@app.get("/compare", response_class=HTMLResponse)
async def compare_page(request: Request, left: Optional[int] = 1, right: Optional[int] = 5):
    user = get_current_user(request)
    all_animals = get_all_animals()
    
    left_animal = get_animal_by_id(left) or (all_animals[0] if all_animals else None)
    right_animal = get_animal_by_id(right) or (all_animals[1] if len(all_animals) > 1 else None)
    
    return templates.TemplateResponse(
        request=request,
        name="comparison.html",
        context={
            "user": user,
            "all_animals": all_animals,
            "left_animal": left_animal,
            "right_animal": right_animal
        }
    )

@app.get("/ai-chat", response_class=HTMLResponse)
async def ai_chat_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(
        request=request,
        name="ai_chat.html",
        context={"user": user}
    )

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={"user": user}
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/?error=unauthorized")
        
    animals = get_all_animals()
    users = get_all_users()
    stats = get_stats()
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM settings")
    settings_rows = c.fetchall()
    settings_dict = {row["key"]: row["value"] for row in settings_rows}
    conn.close()
    
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "user": user,
            "animals": animals,
            "users": users,
            "stats": stats,
            "settings": settings_dict
        }
    )

# ================= API ENDPOINTS =================

@app.post("/api/ai/ask")
async def api_ai_ask(request: Request):
    body = await request.json()
    message = body.get("message", "").strip()
    if not message:
        return JSONResponse({"answer": "Iltimos, biror savol kiriting."})
    answer = ask_ai(message)
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

if __name__ == "__main__":

    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
