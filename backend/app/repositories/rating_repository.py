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
    """Insert a project rating — only for completed projects, only by non-members."""
    if is_team_member(user_id, project_id):
        print(f"User {user_id} is a team member of project {project_id}, cannot rate.")
        return False, "team_member"

    try:
        with engine.connect() as conn:
            status_row = conn.execute(
                text('SELECT status FROM "Project" WHERE project_id = :pid'),
                {"pid": project_id}
            ).fetchone()
        if not status_row or status_row[0] != "Completed":
            return False, "not_completed"

        with engine.connect() as conn:
            already = conn.execute(
                text("SELECT 1 FROM projectrating WHERE user_id = :u AND project_id = :p"),
                {"u": user_id, "p": project_id}
            ).fetchone()
        if already:
            return False, "already_rated"

        db_score = round(score / 2, 1)  # convert 1-10 frontend scale to 0-5 DB constraint
        query = text("""
            INSERT INTO projectrating (user_id, project_id, score, comment)
            VALUES (:user_id, :project_id, :score, :comment)
        """)
        with engine.begin() as conn:
            conn.execute(query, {"user_id": user_id, "project_id": project_id, "score": db_score, "comment": comment})

        print(f"User {user_id} successfully rated project {project_id} with score {score}.")
        return True, "ok"
    except Exception as e:
        print(f"Error adding project rating: {e}")
        return False, "error"


def get_project_ratings(project_id):
    """Return all ratings + comments for a project."""
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT pr.score, pr.comment, u.name
                FROM projectrating pr
                LEFT JOIN "User" u ON u.roll_no = pr.user_id
                WHERE pr.project_id = :project_id
                ORDER BY pr.score DESC
            """), {"project_id": project_id}).fetchall()
        return [
            {
                "score": row[0],
                "comment": row[1],
                "reviewer_name": row[2] or "Anonymous",
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching project ratings: {e}")
        return []


def get_ratings_given_by_user(user_id):
    """Return all project ratings submitted by a user, with project title."""
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT pr.score, pr.comment, pr.created_at, p.title, p.project_id
                FROM projectrating pr
                JOIN "Project" p ON p.project_id = pr.project_id
                WHERE pr.user_id = :user_id
                ORDER BY pr.created_at DESC
            """), {"user_id": user_id}).fetchall()
        return [
            {
                "score": row[0],
                "comment": row[1],
                "created_at": row[2].isoformat() if row[2] else None,
                "project_title": row[3],
                "project_id": row[4],
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching ratings given by user: {e}")
        return []


def get_member_ratings_received(user_id):
    """Return all member ratings received by a user, with project title and rater name."""
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT mr.score, mr.comment, mr.created_at, p.title, p.project_id, u.name
                FROM memberrating mr
                JOIN "Project" p ON p.project_id = mr.project_id
                LEFT JOIN "User" u ON u.roll_no = mr.rated_by
                WHERE mr.rated_user = :user_id
                ORDER BY mr.created_at DESC
            """), {"user_id": user_id}).fetchall()
        return [
            {
                "score": row[0],
                "comment": row[1],
                "created_at": row[2].isoformat() if row[2] else None,
                "project_title": row[3],
                "project_id": row[4],
                "rated_by_name": row[5] or "Anonymous",
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching member ratings received: {e}")
        return []


__all__ = [
    "add_member_rating",
    "add_project_rating",
    "get_project_ratings",
    "get_ratings_given_by_user",
    "get_member_ratings_received",
]
