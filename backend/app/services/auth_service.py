from datetime import datetime
from firebase_admin import auth
from app.extensions import db
from app.repositories.user_repository import user_insert_google_sql
from app.utils.firebase import get_roll_no
from google.cloud.firestore_v1 import FieldFilter


def verify_uid_service(id_token: str, uid: str, user_email: str):
    """Verify a plain uid/idToken login and write session to Firestore."""
    decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)
    if decoded_token["uid"] != uid:
        return None, "uid_mismatch"

    user_doc = db.collection("users").document(user_email)
    user_doc.set({"uid": uid, "fingerprint": None, "created_at": datetime.utcnow()})
    return decoded_token, None


def verify_google_service(id_token: str, uid: str, email: str, fingerprint: str):
    """Verify a Google-sign-in token, write to Firestore, and upsert in Postgres."""
    decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)
    if decoded_token["uid"] != uid:
        return None, "uid_mismatch"

    user_name = decoded_token.get("name", "")
    user_name = user_name.replace("-IIITK", "").strip()
    roll_no = email.split("@")[0]

    # Firestore write
    doc_ref = db.collection("users").document(roll_no)
    doc_ref.set({"uid": uid, "fingerprint": fingerprint, "created_at": datetime.utcnow()})

    # Postgres upsert (non-fatal)
    try:
        user_insert_google_sql({"roll_no": roll_no, "user_name": user_name, "email": email})
    except Exception as sql_err:
        print("SQL insert failed (non-fatal):", sql_err)

    return {"roll_no": roll_no, "user_name": user_name}, None


def auto_login_service(uid: str, fingerprint: str):
    """Return (roll_no, authenticated) by checking Firestore session."""
    users_ref = db.collection("users")
    result = (
        users_ref
        .where(filter=FieldFilter("uid", "==", uid))
        .where(filter=FieldFilter("fingerprint", "==", fingerprint))
        .get()
    )
    if not result:
        return None, False

    try:
        roll_no = get_roll_no(uid)
    except Exception:
        roll_no = None

    return roll_no, True
