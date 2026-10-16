@echo off
chcp 65001 > nul
echo ========================================================
echo   🌿 Animore — Hayvonot Olami Portali Ishga Tushmoqda...
echo ========================================================
echo.
echo Brauzerda ochish manzili: http://127.0.0.1:8000
echo.
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
