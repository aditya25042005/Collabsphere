from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth


def firebase_uid_required(f):
    """Decorator that verifies the Firebase UID stored in the 'uid' cookie."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        uid = request.cookies.get("uid")
        if not uid:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            user = auth.get_user(uid)
        except firebase_admin.exceptions.FirebaseError:
            return jsonify({"message": "Unauthorized"}), 401

        request.user = user
        return f(*args, **kwargs)

    return decorated_function
