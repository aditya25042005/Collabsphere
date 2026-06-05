from flask import Blueprint
from app.controllers.user_controller import (
    list_users_controller,
    first_login_controller,
    profile_view_controller,
    update_profile_controller,
)
from app.middleware.auth import firebase_uid_required

user_bp = Blueprint("user", __name__)

user_bp.add_url_rule("/list/users", view_func=list_users_controller, methods=["GET"])
user_bp.add_url_rule("/first_login", view_func=first_login_controller, methods=["POST"])
user_bp.add_url_rule("/profile/view", view_func=profile_view_controller, methods=["POST"])
user_bp.add_url_rule(
    "/update/profile",
    view_func=firebase_uid_required(update_profile_controller),
    methods=["POST"],
)
