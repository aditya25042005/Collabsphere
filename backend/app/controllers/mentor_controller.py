from flask import request, jsonify
from app.services.mentor_service import (
    list_mentors_service,
    apply_mentors_service,
    apply_mentors_takeback_service,
    accept_mentor_service,
)
from app.schemas import (
    ListOfMentorsSchema,
    ApplyMentorsSchema,
    ApplyMentorsStatusTakebackSchema,
    AcceptMentorSchema,
)


def list_mentors_controller():
    data = request.json
    errors = ListOfMentorsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return list_mentors_service(data)


def apply_mentors_controller():
    data = request.json
    errors = ApplyMentorsSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return apply_mentors_service(data)


def apply_mentors_takeback_controller():
    data = request.json
    errors = ApplyMentorsStatusTakebackSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return apply_mentors_takeback_service(data)


def accept_mentor_controller():
    data = request.json
    errors = AcceptMentorSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    return accept_mentor_service(data)
