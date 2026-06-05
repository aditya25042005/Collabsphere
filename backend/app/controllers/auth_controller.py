from flask import request, jsonify, make_response
from app.services.auth_service import (
    verify_uid_service,
    verify_google_service,
    auto_login_service,
)
from app.config import Config


def verify_email_controller():
    data = request.json
    id_token = data.get("idToken")
    uid = data.get("uid")
    user_email = data.get("user_email")
    fingerprint = data.get("fingerprint")

    try:
        _, err = verify_uid_service(id_token, uid, user_email)
        if err:
            return jsonify({"user_verified": False}), 403

        response = make_response(jsonify({"user_verified": True, "message": "Cookie Set"}))
        response.set_cookie(
            "uid", uid,
            httponly=True, secure=Config.COOKIE_SECURE, samesite=Config.COOKIE_SAMESITE,
            max_age=60 * 60 * 24 * 3,
        )
        response.set_cookie(
            "fingerprint", fingerprint,
            httponly=True, secure=Config.COOKIE_SECURE, samesite=Config.COOKIE_SAMESITE,
            max_age=60 * 60 * 24 * 3,
        )
        return response
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def verify_google_controller():
    data = request.json
    id_token = data.get("idToken")
    uid = data.get("uid")
    email = data.get("email")
    fingerprint = data.get("fingerprint")

    try:
        result, err = verify_google_service(id_token, uid, email, fingerprint)
        if err:
            return jsonify({"user_verified": False}), 403

        response = make_response(
            jsonify({
                "user_verified": True,
                "message": "cookie set",
                "roll_no": result["roll_no"],
            })
        )
        response.set_cookie(
            "fingerprint", fingerprint,
            httponly=True, secure=Config.COOKIE_SECURE, samesite=Config.COOKIE_SAMESITE,
            max_age=60 * 60 * 24 * 3,
        )
        response.set_cookie(
            "uid", uid,
            httponly=True, secure=Config.COOKIE_SECURE, samesite=Config.COOKIE_SAMESITE,
            max_age=60 * 60 * 24 * 3,
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 401


def auto_login_controller():
    uid = request.cookies.get("uid")
    fingerprint = request.cookies.get("fingerprint")

    if not uid or not fingerprint:
        return jsonify({"authenticated": False, "message": "No session"}), 401

    try:
        roll_no, authenticated = auto_login_service(uid, fingerprint)
        if authenticated:
            return jsonify({"authenticated": True, "roll_no": roll_no})
        return jsonify({"authenticated": False, "message": "Invalid session"}), 401
    except Exception as e:
        print("auto_login error:", e)
        return jsonify({"authenticated": False, "message": "Invalid session"}), 401


def logout_controller():
    try:
        response = make_response(jsonify({"success": True}))
        response.delete_cookie("uid", samesite=Config.COOKIE_SAMESITE, secure=Config.COOKIE_SECURE)
        response.delete_cookie("fingerprint", samesite=Config.COOKIE_SAMESITE, secure=Config.COOKIE_SECURE)
        return response
    except Exception:
        return jsonify({"deleted": False}), 500
