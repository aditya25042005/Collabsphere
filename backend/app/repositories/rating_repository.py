from sqlalchemy import text
from app.extensions import engine


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


def add_member_rating(rated_by, rated_user, project_id, score, comment):
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO memberrating (rated_by, rated_user, project_id, score, comment)
                VALUES (:rated_by, :rated_user, :project_id, :score, :comment)
            """), {
                "rated_by": rated_by,
                "rated_user": rated_user,
                "project_id": project_id,
                "score": score,
                "comment": comment
            })
            conn.commit()
        return True
    except Exception as e:
        print(f"Error adding member rating: {e}")
        return False

def add_project_rating(user_id, project_id, score, comment):
    """Insert a project rating if the user is NOT a project member"""
    if is_team_member(user_id, project_id):
        print(f"User {user_id} is a team member of project {project_id}, cannot rate.")
        return False

    try:
        query = text("""
            INSERT INTO projectrating (user_id, project_id, score, comment)
            VALUES (:user_id, :project_id, :score, :comment)
        """)
        with engine.begin() as conn:
            conn.execute(query, {"user_id": user_id, "project_id": project_id, "score": score, "comment": comment})

        print(f"User {user_id} successfully rated project {project_id} with score {score}.")
        return True
    except Exception as e:
        print(f"Error adding project rating: {e}")
        return False


__all__ = [
    "add_member_rating",
    "add_project_rating",
]
