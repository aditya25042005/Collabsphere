from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.mentor_controller import (
    list_mentors_controller,
    apply_mentors_controller,
    apply_mentors_takeback_controller,
    accept_mentor_controller,
)

mentor_bp = Blueprint("mentor", __name__)

mentor_bp.add_url_rule(
    "/list/mentors",
    view_func=firebase_uid_required(list_mentors_controller),
    methods=["POST"],
)
mentor_bp.add_url_rule(
    "/apply/mentors",
    view_func=firebase_uid_required(apply_mentors_controller),
    methods=["POST"],
)
mentor_bp.add_url_rule(
    "/apply/mentors/status/takeback",
    view_func=firebase_uid_required(apply_mentors_takeback_controller),
    methods=["POST"],
)
mentor_bp.add_url_rule(
    "/accept/mentors",
    view_func=firebase_uid_required(accept_mentor_controller),
    methods=["POST"],
)
