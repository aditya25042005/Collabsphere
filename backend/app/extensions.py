import firebase_admin
from firebase_admin import credentials, firestore
from sqlalchemy import create_engine
from app.config import Config

# SQLAlchemy engine (shared across the whole app)
engine = create_engine(Config.NEON_DB_URL, echo=True)

# Firebase Admin SDK initialisation (idempotent – safe to import multiple times)
if not firebase_admin._apps:
    _cred = credentials.Certificate(Config.FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(_cred)

# Firestore client and top-level 'users' collection reference
db = firestore.client()
users_collection = db.collection("users")
