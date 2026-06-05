from app.repositories.sprint_repository import (
    get_sprints,
    get_sprint_status,
    change_sprint_status_sql,
    create_sprint,
)


def get_sprints_service(project_id):
    return get_sprints(project_id)


def get_sprint_status_service(project_id, sprint_number):
    return get_sprint_status(project_id, sprint_number)


def change_sprint_status_service(data):
    return change_sprint_status_sql(data)


def create_sprint_service(user_id, project_id, name, start_date, end_date):
    return create_sprint(user_id, project_id, name, start_date, end_date)
