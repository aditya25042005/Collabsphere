from flask import request, jsonify
from app.services.user_service import (
    check_service,
    first_login_service,
    profile_view_service,
    update_profile_service,
    list_users_service,
)
from app.schemas import FirstLoginSchema, UserSchema


def check_controller():
    return check_service()


def list_users_controller():
    return list_users_service()


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
