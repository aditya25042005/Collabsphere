from app.repositories.project_repository import (
    add_projects,
    ranking,
    list_projects_sql,
    list_current_projects_sql,
    list_past_projects_sql,
    list_myprojects_sql,
    get_project_details,
    get_project_analytics,
)


def add_project_service(data):
    return add_projects(data)


def best_projects_service():
    return ranking()


def list_projects_service(data):
    return list_projects_sql(data)


def list_current_projects_service(data):
    return list_current_projects_sql(data)


def list_past_projects_service(data):
    return list_past_projects_sql(data)


def list_myprojects_service(data):
    return list_myprojects_sql(data)


def view_project_details_service(project_id):
    return get_project_details(project_id)


def project_analytics_service(project_id):
    return get_project_analytics(project_id)
