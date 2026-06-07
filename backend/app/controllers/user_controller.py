from flask import request, jsonify
from app.services.user_service import (
    check_service,
    first_login_service,
    profile_view_service,
    update_profile_service,
    list_users_service,
    list_skills_service,
)
from app.schemas import FirstLoginSchema, UserSchema


def check_controller():
    return check_service()


def list_users_controller():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    search = request.args.get("search", "").strip()
    skills = request.args.getlist("skill")  # ?skill=React&skill=Python
    return list_users_service(limit=limit, offset=offset, search=search, skills=skills or None)


def list_skills_controller():
    return list_skills_service()


def first_login_controller():
    data = request.json
    errors = FirstLoginSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return first_login_service(data)


def profile_view_controller():
    data = request.json
    errors = FirstLoginSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return profile_view_service(data)


def update_profile_controller():
    data = request.json
    return update_profile_service(data)
