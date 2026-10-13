import os
import sys
from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
REMOTE_URL = "https://github.com/java0918/animal.git"

def main():
    print(f"Loyiha manzili: {REPO_PATH}")
    
    # 1. Init git repository if not exists
    git_dir = os.path.join(REPO_PATH, ".git")
    if not os.path.exists(git_dir):
        print("Git repozitoriysi initsializatsiya qilinmoqda...")
        repo = porcelain.init(REPO_PATH)
    else:
        print("Mavjud Git repozitoriysi ochilmoqda...")
        repo = Repo(REPO_PATH)
        
    # 2. Add files
    print("Fayllar git ga qo'shilmoqda (git add)...")
    files_to_add = []
    for root, dirs, files in os.walk(REPO_PATH):
        # Ignore .git and __pycache__
        if ".git" in root or "__pycache__" in root:
            continue
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, REPO_PATH).replace("\\", "/")
            files_to_add.append(rel_path)
            
    porcelain.add(repo, files_to_add)
    print(f"{len(files_to_add)} ta fayl qo'shildi.")
    
    # 3. Commit
    try:
        commit_id = porcelain.commit(
            repo,
            message="Fauna & Flora — Hayvonot olami, Qizil kitob, AI yordamchi va audio portal",
            committer=b"Fauna Developer <developer@hayvonlar.uz>"
        )
        print(f"Commit yaratildi: {commit_id.decode() if isinstance(commit_id, bytes) else commit_id}")
    except Exception as e:
        print(f"Commit xabari: {e}")

    # 4. Set remote origin
    config = repo.get_config()
    section = (b'remote', b'origin')
    config.set(section, b'url', REMOTE_URL.encode())
    config.set(section, b'fetch', b'+refs/heads/*:refs/remotes/origin/*')
    config.write_to_path()
    print(f"Masofaviy repozitoriy (remote origin) bog'landi:\n -> {REMOTE_URL}")
    
    # Check remotes
    remotes = porcelain.remote_list(repo)
    print("Mavjud remote'lar:", remotes)
    
if __name__ == "__main__":
    main()
