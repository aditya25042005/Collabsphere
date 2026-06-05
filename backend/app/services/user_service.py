from app.repositories.user_repository import (
    insert,
    first_logins,
    profile_views,
    update_profile_sql,
    list_users_sql,
)


def check_service():
    return insert()


def first_login_service(data):
    return first_logins(data)


def profile_view_service(data):
    return profile_views(data)


def update_profile_service(data):
    return update_profile_sql(data)


def list_users_service():
    return list_users_sql()
