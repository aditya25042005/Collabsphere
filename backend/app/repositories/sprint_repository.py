from sqlalchemy import text
from flask import jsonify
from app.extensions import engine


def get_sprints(project_id):
    try:
        with engine.connect() as conn:
            sprints = conn.execute(text("""
                SELECT sprint_id, name, start_date, end_date, status FROM sprint
                WHERE project_id = :project_id
                ORDER BY sprint_id
            """),{"project_id": project_id}).fetchall()
            return sprints
    except Exception as e:
        print(f"Error getting sprints: {e}")
        return None


def get_sprint_status(project_id, sprint_number):
    """Fetch the status of a given sprint."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT status FROM sprint
            WHERE project_id = :project_id AND sprint_id = :sprint_number
        """), {"project_id": project_id, "sprint_number": sprint_number}).fetchone()

        return result[0] if result else None


def get_last_sprint_status(project_id):
    """Fetch the latest sprint's status."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT status FROM sprint
            WHERE project_id = :project_id
            ORDER BY sprint_id DESC LIMIT 1
        """), {"project_id": project_id}).fetchone()
        return result[0] if result else "closed"

def change_sprint_status_sql(data):
    #check for particular project and sprint

    try:
        # Check if all task are done or not
        with engine.connect() as conn:
            result = conn.execute(text("""
               select * from sprint where project_id=:project_id and sprint_number=:sprint_id  and status not in 'done'

            """), {

                "project_id": data["project_id"],
                "sprint_id": data["sprint_id"]

            })
            conn.commit()
            if result.scalar > 0:
                return jsonify({"sprint": "complete previous"}), 404




        with engine.connect() as conn:
            result = conn.execute(text("""
                UPDATE sprint
                SET status = :status
                WHERE project_id = :project_id AND sprint_id = :sprint_id;
            """), {
                "status": data["status"],
                "project_id": data["project_id"],
                "sprint_id": data["sprint_id"]
            })
            conn.commit()

            if result.rowcount == 0:
                return jsonify({"error": "Sprint not found"}), 404

            return jsonify({"sprint": "updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def is_admin_or_mod(user_id, project_id):
    """Check if the user is an admin or moderator of the project."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT role FROM projectmembers
                WHERE project_id = :project_id AND member_id = :user_id
            """), {"project_id": project_id, "user_id": user_id}).fetchone()
            return result and result[0] in ["admin", "moderator"]
    except Exception as e:
        print(f"Error checking admin/mod status: {e}")
        return False


def create_sprint(user_id, project_id, name, start_date, end_date):
    """Create a new sprint only if the previous one is completed and the user is an admin/mod."""
    if not is_admin_or_mod(user_id, project_id):
        return jsonify({"error": "Only an admin or mod can create a sprint."}), 403

    last_sprint_status = get_last_sprint_status(project_id)
    print(last_sprint_status)
    if last_sprint_status != "closed":
        return jsonify({"error": "Previous sprint must be completed before creating a new one."}), 400
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO sprint (project_id, name, start_date, end_date, status)
                VALUES (:project_id, :name, :start_date, :end_date, 'open')
            """), {"project_id": project_id, "name": name, "start_date": start_date, "end_date": end_date})
        return jsonify({"message": "Sprint created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


__all__ = [
    "get_sprints",
    "get_sprint_status",
    "get_last_sprint_status",
    "change_sprint_status_sql",
    "create_sprint",
]
