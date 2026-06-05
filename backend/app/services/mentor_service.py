from app.repositories.mentor_repository import (
    list_of_mentors_sql,
    apply_mentors_sql,
    apply_mentors_takeback_sql,
    accept_mentor_sql,
)


def list_mentors_service(data):
    return list_of_mentors_sql(data)


def apply_mentors_service(data):
    return apply_mentors_sql(data)


def apply_mentors_takeback_service(data):
    return apply_mentors_takeback_sql(data)


def accept_mentor_service(data):
    return accept_mentor_sql(data)
