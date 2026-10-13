@echo off
chcp 65001 > nul
echo ========================================================
echo   🐙 GitHub ga Yuklash (https://github.com/java0918/animal.git)
echo ========================================================
echo.
set /p GITHUB_TOKEN="GitHub Personal Access Token (PAT) kiriting: "
if "%GITHUB_TOKEN%"=="" (
    echo Xatolik: Token kiritilmadi!
    pause
    exit /b
)
python push_to_github.py %GITHUB_TOKEN%
echo.
pause
