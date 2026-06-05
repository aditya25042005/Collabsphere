from sqlalchemy import text
from flask import jsonify
from app.extensions import engine


def member_sql(data):
    query = text("""
        SELECT *
        FROM projectmembers
        WHERE project_id = :project_id AND member_id = :member_id
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "project_id":data['project_id'],
            "member_id": data['member_id']
        })

        row=result.fetchone()

        if(row):

            return jsonify({"member":"yes","role":row[2]}), 200


        else:
            return jsonify({"member":"no"}), 401

def get_eligible_users_for_mod(project_id):
    try:
        with engine.connect() as conn:
            users = conn.execute(text("""
                SELECT member_id, name
                FROM projectmembers pm
                JOIN "User" u ON pm.member_id = u.roll_no
                WHERE pm.project_id = :project_id
            """), {"project_id": project_id}).fetchall()

            return users

    except Exception as e:
        print(f"Error getting eligible users: {e}")
        return None


def promote_to_moderator(conn, project_id, user_id):
    try:
        with conn.begin():
            # Fetch the current role of the user
            result = conn.execute(text("""
                SELECT role FROM projectmembers
                WHERE project_id = :project_id AND member_id = :user_id
            """), {"project_id": project_id, "user_id": user_id}).fetchone()

            # If no record is found, the user is not in the project
            if not result:
                return False, "User is not a member of this project."

            current_role = result[0]

            # If the user is already a mod or admin, prevent the update
            if current_role in ["moderator", "admin"]:
                return False, f"User is already a {current_role}."

            # Promote user to moderator
            conn.execute(text("""
                UPDATE projectmembers
                SET role = 'moderator'
                WHERE project_id = :project_id AND member_id = :user_id
            """), {"project_id": project_id, "user_id": user_id})

            return True, f"User {user_id} promoted to Moderator."

    except Exception as e:
        print(f"Error promoting user: {e}")
        return False, "Database error occurred."

def remove_moderator(project_id, user_id):
    try:
        with engine.begin() as conn:
            result = conn.execute(text("""
                UPDATE projectmembers
                SET role = 'member'
                WHERE project_id = :project_id
                AND member_id = :user_id
                AND role = 'moderator'
                RETURNING member_id;
            """), {"project_id": project_id, "user_id": user_id})

            updated_user = result.fetchone()

            if updated_user:
                return True
            else:
                return False

    except Exception as e:
        print(f"Error demoting user: {e}")
        return False

def is_valid_member(project_id, user_id):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 1 FROM projectmembers
                WHERE project_id = :project_id AND member_id = :user_id
            """), {"project_id": project_id, "user_id": user_id}).fetchone()
            return result is not None
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def is_team_member(user_id, project_id):
    """Check if the user is a member of the project"""
    try:
        query = text("""
            SELECT 1 FROM projectmembers
            WHERE member_id = :user_id AND project_id = :project_id
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {"user_id": user_id, "project_id": project_id}).fetchone()
            print(f"DEBUG: is_team_member check for {user_id} in project {project_id}: {result}")
            return result is not None
    except Exception as e:
        print(f"Error checking team membership: {e}")
        return True

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


__all__ = [
    "member_sql",
    "get_eligible_users_for_mod",
    "promote_to_moderator",
    "remove_moderator",
    "is_valid_member",
    "is_team_member",
    "is_admin_or_mod",
]
