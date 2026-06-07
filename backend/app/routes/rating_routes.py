from flask import Blueprint
from app.middleware.auth import firebase_uid_required
from app.controllers.rating_controller import (
    rate_member_controller,
    rate_project_controller,
    get_project_ratings_controller,
    get_ratings_given_controller,
    get_member_ratings_received_controller,
)

rating_bp = Blueprint("rating", __name__)

rating_bp.add_url_rule(
    "/rate_member",
    view_func=firebase_uid_required(rate_member_controller),
    methods=["POST"],
)
rating_bp.add_url_rule(
    "/rate_project",
    view_func=firebase_uid_required(rate_project_controller),
    methods=["POST"],
)
rating_bp.add_url_rule(
    "/project/ratings",
    view_func=get_project_ratings_controller,
    methods=["GET"],
)
rating_bp.add_url_rule(
    "/user/ratings/given",
    view_func=get_ratings_given_controller,
    methods=["GET"],
)
rating_bp.add_url_rule(
    "/user/ratings/received",
    view_func=get_member_ratings_received_controller,
    methods=["GET"],
)
