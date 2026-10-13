import sys
import os
import getpass
from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
REMOTE_URL = "https://github.com/java0918/animal.git"

def push(token=None, username="java0918"):
    if not token:
        if len(sys.argv) > 1:
            token = sys.argv[1].strip()
        else:
            print("==================================================")
            print(" GitHub ga yuklash (Push to GitHub)")
            print(f" Repozitoriy: {REMOTE_URL}")
            print("==================================================")
            token = input("GitHub Personal Access Token (PAT) kiriting: ").strip()

    if not token:
        print("Xatolik: Token kiritilmadi!")
        return False

    # Construct authenticated URL: https://<token>@github.com/java0918/animal.git
    auth_url = f"https://{username}:{token}@github.com/java0918/animal.git"

    print("GitHub ga push qilinmoqda...")
    try:
        porcelain.push(REPO_PATH, auth_url, "refs/heads/main:refs/heads/main", force=True)
        print("✅ MUVAFFAQIYATLI YUKLANDI! Barcha fayllar GitHub ga yuborildi.")
        print(f"👉 Ko'rish uchun havola: https://github.com/java0918/animal")
        return True
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        print("\nEslatma: GitHub Token yaratish uchun:")
        print("1. https://github.com/settings/tokens ga kiring (Classic yoki Fine-grained)")
        print("2. 'repo' huquqini belgilab token oling")
        print("3. python push_to_github.py <token> buyrug'ini ishga tushiring")
        return False

if __name__ == "__main__":
    push()
