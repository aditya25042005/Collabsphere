from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.member_controller import (
    verify_member_controller,
    get_eligible_users_controller,
    promote_moderator_controller,
    demote_moderator_controller,
    notification_controller,
)

member_bp = Blueprint("member", __name__)

member_bp.add_url_rule(
    "/verify/member",
    view_func=firebase_uid_required(verify_member_controller),
    methods=["POST"],
)
member_bp.add_url_rule(
    "/notification",
    view_func=firebase_uid_required(notification_controller),
    methods=["POST"],
)
member_bp.add_url_rule(
    "/project/add_mod/eligible_users",
    view_func=firebase_uid_required(get_eligible_users_controller),
    methods=["GET"],
)
member_bp.add_url_rule(
    "/project/add_mod/promote",
    view_func=firebase_uid_required(promote_moderator_controller),
    methods=["POST"],
)
member_bp.add_url_rule(
    "/project/add_mod/demote",
    view_func=firebase_uid_required(demote_moderator_controller),
    methods=["POST"],
)
