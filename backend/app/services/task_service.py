from app.repositories.task_repository import (
    get_sprint_tasks,
    add_task,
    update_task,
    update_task_status,
)
from app.repositories.sprint_repository import get_sprint_status

STATUS_MAPPING = {
    "to do": "pending",
    "in progress": "review",
    "completed": "done",
}


def view_sprint_tasks_service(project_id):
    return get_sprint_tasks(project_id)


def add_task_service(data):
    project_id = data.get("project_id")
    sprint_number = data.get("sprint_number")
    description = data.get("description")
    assigned_to = data.get("assigned_to")
    points = data.get("points")
    status_raw = "To Do"

    sprint_status = get_sprint_status(project_id, sprint_number)
    if sprint_status != "open":
        return False, "Sprint is not open"

    db_status = STATUS_MAPPING.get(status_raw.lower())
    if not db_status:
        return False, "Invalid status value"

    add_task(project_id, sprint_number, description, assigned_to, points, db_status)
    return True, "Task added successfully"


def update_task_status_service(task_id, frontend_status):
    db_status = STATUS_MAPPING.get(frontend_status.lower() if frontend_status else "")
    if not db_status:
        return False, f"Invalid status: {frontend_status}"
    success = update_task_status(task_id, db_status)
    return success, "Updated" if success else "Failed"


def update_task_service(task_id, updates: dict):
    if "status" in updates:
        db_status = STATUS_MAPPING.get(updates["status"].lower() if updates["status"] else "")
        if not db_status:
            return False, f"Invalid status: {updates['status']}"
        updates["status"] = db_status
    success = update_task(task_id, **updates)
    return success, "Updated" if success else "Failed"


def change_task_status_service(task_id, frontend_status):
    """Generic helper used by start / complete / reopen routes."""
    db_status = STATUS_MAPPING.get(frontend_status.lower() if frontend_status else "")
    if not db_status:
        return False, f"Invalid status: {frontend_status}"
    success = update_task(task_id, status=db_status)
    return success, None
