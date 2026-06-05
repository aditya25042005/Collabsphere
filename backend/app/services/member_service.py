from app.repositories.member_repository import (
    member_sql,
    get_eligible_users_for_mod,
    promote_to_moderator,
    remove_moderator,
)
from app.extensions import engine


def verify_member_service(data):
    return member_sql(data)


def get_eligible_users_service(project_id):
    return get_eligible_users_for_mod(project_id)


def promote_moderator_service(project_id, user_id):
    with engine.connect() as conn:
        return promote_to_moderator(conn, project_id, user_id)


def remove_moderator_service(project_id, user_id):
    return remove_moderator(project_id, user_id)
