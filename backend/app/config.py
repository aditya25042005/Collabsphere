import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    IS_PROD = FLASK_ENV == "production"

    NEON_DB_URL = os.getenv("NEON_DB_URL")

    ALLOWED_ORIGINS = [
        o.strip()
        for o in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,http://localhost:52843,http://127.0.0.1:3000",
        ).split(",")
    ]

    COOKIE_SECURE = IS_PROD
    COOKIE_SAMESITE = "None" if IS_PROD else "Lax"

    FIREBASE_KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "key.json")
