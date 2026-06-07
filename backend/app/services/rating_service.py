from app.repositories.rating_repository import (
    add_member_rating,
    add_project_rating,
    get_project_ratings,
    get_ratings_given_by_user,
    get_member_ratings_received,
)


def rate_member_service(rated_by, rated_user, project_id, score, comment):
    return add_member_rating(rated_by, rated_user, project_id, score, comment)


def rate_project_service(user_id, project_id, score, comment):
    success, reason = add_project_rating(user_id, project_id, score, comment)
    return success, reason


def get_project_ratings_service(project_id):
    return get_project_ratings(project_id)


def get_ratings_given_by_user_service(user_id):
    return get_ratings_given_by_user(user_id)


def get_member_ratings_received_service(user_id):
    return get_member_ratings_received(user_id)
