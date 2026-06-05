from sqlalchemy import text
from app.extensions import engine


def get_sprint_tasks(project_id):
    try:
        project_id = int(project_id)

        with engine.connect() as conn:
            project_check = text("""
                SELECT project_id FROM "Project"
                WHERE project_id = :project_id
            """)
            project = conn.execute(project_check, {"project_id": project_id}).mappings().fetchone()
            if not project:
                print(f"Project {project_id} not found")
                return None

            sprint_query = text("""
                SELECT DISTINCT sprint_number,
                (SELECT COUNT(*) FROM task t2 WHERE t2.project_id = :project_id AND t2.sprint_number = t.sprint_number) AS total_tasks,
                (SELECT COUNT(*) FROM task t2 WHERE t2.project_id = :project_id AND t2.sprint_number = t.sprint_number AND t2.status = 'done') AS completed_tasks
                FROM task t
                WHERE t.project_id = :project_id AND t.sprint_number IS NOT NULL
                ORDER BY sprint_number
            """)
            sprints = conn.execute(sprint_query, {"project_id": project_id}).mappings().all()

            if not sprints:
                unassigned_check = text("""
                    SELECT COUNT(*) as count FROM task
                    WHERE project_id = :project_id
                """)
                unassigned = conn.execute(unassigned_check, {"project_id": project_id}).mappings().fetchone()
                if unassigned and unassigned["count"] > 0:
                    sprints = [{
                        "sprint_number": None,
                        "total_tasks": unassigned["count"],
                        "completed_tasks": 0
                    }]

            sprint_data = []

            column_check = text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'task' AND column_name = 'title'
            """)
            title_exists = conn.execute(column_check).fetchone() is not None

            for sprint in sprints:
                sprint_number = sprint["sprint_number"]

                task_query = text(f"""
                    SELECT id, description, assigned_to, points, status
                    {', title' if title_exists else ''}
                    FROM task
                    WHERE project_id = :project_id
                      AND (sprint_number = :sprint_number OR (:sprint_number IS NULL AND sprint_number IS NULL))
                    ORDER BY status
                """)
                tasks = conn.execute(task_query, {"project_id": project_id, "sprint_number": sprint_number}).mappings().all()

                categorized_tasks = {"todo": [], "in_progress": [], "completed": []}
                completed_count = 0

                for task in tasks:
                    assignee_name = None
                    if task["assigned_to"]:
                        name_query = text("SELECT name FROM \"User\" WHERE roll_no = :roll_no")
                        user = conn.execute(name_query, {"roll_no": task["assigned_to"]}).mappings().fetchone()
                        assignee_name = user["name"] if user else task["assigned_to"]

                    task_data = {
                        "id": task["id"],
                        "description": task["description"],
                        "assigned_to": task["assigned_to"],
                        "assignee_name": assignee_name,
                        "points": task["points"],
                    }
                    if title_exists:
                        task_data["title"] = task["title"]

                    status = task["status"].lower() if task["status"] else "pending"
                    if status in ["pending", "todo"]:
                        categorized_tasks["todo"].append(task_data)
                    elif status in ["review", "in_progress", "progress"]:
                        categorized_tasks["in_progress"].append(task_data)
                    elif status in ["done", "completed"]:
                        categorized_tasks["completed"].append(task_data)
                        completed_count += 1
                    else:
                        categorized_tasks["todo"].append(task_data)

                if sprint_number is None:
                    sprint["completed_tasks"] = completed_count

                total = int(sprint["total_tasks"])
                completed = int(sprint["completed_tasks"])
                completion_percentage = (completed / total * 100) if total > 0 else 0

                sprint_data.append({
                    "sprint_number": sprint_number,
                    "sprint_name": f"Sprint {sprint_number}" if sprint_number is not None else "Unassigned Tasks",
                    "total_tasks": total,
                    "completed_tasks": completed,
                    "completion_percentage": round(completion_percentage, 2),
                    "tasks": categorized_tasks
                })

            return sprint_data

    except Exception as e:
        print(f"Error in get_sprint_tasks: {e}")
        import traceback
        traceback.print_exc()
        return None

def add_task(project_id, sprint_number, description, assigned_to, points, status):
    """Insert a new task into the 'task' table."""
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO task (project_id, sprint_number, description, assigned_to, status, points)
                VALUES (:project_id, :sprint_number, :description, :assigned_to, 'pending', :points)
            """), {
                "project_id": project_id,
                "sprint_number": sprint_number,
                "description": description,
                "assigned_to": assigned_to,
                "points": points,
                "status": status
            })
            conn.commit()
        return True, "Task added successfully"
    except Exception as e:
        print(f"Error adding task: {e}")
        return False, str(e)

def update_task(task_id, **updates):
    """Updates only the provided fields for a given task_id."""
    if not updates:
        print("No fields to update")
        return False

    try:
        set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
        updates["task_id"] = task_id
        with engine.connect() as conn:
            conn.execute(text(f"""
                UPDATE task
                SET {set_clause}
                WHERE id = :task_id
            """), updates)
            conn.commit()

        return True

    except Exception as e:
        print(f"Error updating task: {e}")
        return False


def update_task_status(task_id, new_status):
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE task SET status = :status WHERE id = :task_id
            """), {"status": new_status, "task_id": task_id})
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task status: {e}")
        return False


__all__ = [
    "get_sprint_tasks",
    "add_task",
    "update_task",
    "update_task_status",
]
