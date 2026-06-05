from app.repositories.rating_repository import (
    add_member_rating,
    add_project_rating,
)


def rate_member_service(rated_by, rated_user, project_id, score, comment):
    return add_member_rating(rated_by, rated_user, project_id, score, comment)


def rate_project_service(user_id, project_id, score, comment):
    return add_project_rating(user_id, project_id, score, comment)
