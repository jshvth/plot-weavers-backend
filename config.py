import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 🔐 Security
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")

    # 🗄️ Datenbank
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        # Render nutzt manchmal noch das alte postgres:// Format → korrigieren
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f"sqlite:///{os.path.join(BASE_DIR, 'plotweavers.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📁 Upload-Verzeichnisse
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    UPLOAD_FOLDER_PROFILES = os.path.join(UPLOAD_FOLDER, "profiles")
    UPLOAD_FOLDER_STORIES = os.path.join(UPLOAD_FOLDER, "stories")

    # 🧹 Optional: Stelle sicher, dass Upload-Ordner existieren
    os.makedirs(UPLOAD_FOLDER_PROFILES, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER_STORIES, exist_ok=True)
