from flask import Blueprint
from app.controllers.auth_controller import (
    verify_email_controller,
    verify_google_controller,
    auto_login_controller,
    logout_controller,
)

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/verify/user_id", view_func=verify_email_controller, methods=["POST"])
auth_bp.add_url_rule("/verify/google", view_func=verify_google_controller, methods=["POST"])
auth_bp.add_url_rule("/auto_login", view_func=auto_login_controller, methods=["GET"])
auth_bp.add_url_rule("/logout", view_func=logout_controller, methods=["GET"])
