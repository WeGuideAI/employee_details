import os
from datetime import timedelta


def _normalize_database_url(url: str) -> str:
    # Railway/Heroku-style URLs may use postgres:// which SQLAlchemy 2 rejects.
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-change-me")
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///weguide.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }
    # Default: 16 MB for employee photos/logos; override via env as needed.
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(16 * 1024 * 1024)))
    UPLOAD_EMPLOYEE_FOLDER = os.path.join("app", "static", "uploads", "employees")
    UPLOAD_LOGO_FOLDER = os.path.join("app", "static", "uploads", "logos")
    QR_FOLDER = os.path.join("app", "static", "uploads", "qrcodes")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "")
    USE_CLOUDINARY = os.getenv("USE_CLOUDINARY", "false").lower() == "true"
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": Config,
}
