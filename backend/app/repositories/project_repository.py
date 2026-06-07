from sqlalchemy import text
from flask import jsonify
from datetime import date
from app.extensions import engine


def add_projects(data):
   with engine.connect() as conn:
       # check whether with same admin same name other project exist
       result=conn.execute(text("""select * from "Project" where admin_id=:val1 and title=:val2"""),{

          "val1":data['admin_id'],
          "val2":data['title']})

       conn.commit()
   if(result.rowcount>0):
         print(result)
           ### return can't be inserted change project name
         return jsonify({"project":"already exist"}), 401

   else:
    with engine.connect() as conn:
       # check whether with same admin same name other project exist
     try:
         result=conn.execute(text("""INSERT INTO "Project"
(admin_id, title, description, start_date, end_date, members_required, status, tags)
                                values
            (:val1,:val2,:val3,:val4,:val5,:val6,:val7,:val8)"""),{

          "val1":data['admin_id'],
          "val2":data['title'],
          "val3":data['description'],
          "val4":data['start_date'],
          "val5":data['end_date'],
         "val6":data['members_required'],
         "val7":data['status'],
         "val8":data['tags']

          })
         result1=conn.execute(text("""select project_id from "Project"
                                   where admin_id=:val1 and title=:val2""")
                                   ,{

"val1":data['admin_id'],
          "val2":data['title'],

                                   })
         project_id=result1.fetchall()[0].project_id
         query = """
INSERT INTO projectmembers (project_id, member_id, role)
VALUES (:val1, :val2, :val3)
"""

# Execute the query using bound parameters
         result2 = conn.execute(text(query), {
    "val1": project_id,
    "val2": data['admin_id'],
    "val3": "admin"
})
         conn.commit()

         return jsonify({"project":"added"})




     except Exception as e:
         return jsonify({"error": str(e)}), 500

def ranking():
      #changes for new db rating to project rating
    with engine.connect() as conn:
        result=conn.execute(text("""SELECT
    p.project_id,
    p.title,
    AVG(r.score)*0.7+0.3 * COUNT(r.comment) AS score
    FROM

    projectrating r
    JOIN
    "Project" p ON r.project_id = p.project_id
    GROUP BY
    p.project_id,
    p.title
    ORDER BY
    score DESC;
    """))
        conn.commit()

        rows=result.fetchall()

        data = [
    {"project_id": row[0], "title": row[1], "score": row[2]}
    for row in rows
]

        #print(data)
        return jsonify({"project": data})

def rankings():
      #changes for new db rating to project rating
    with engine.connect() as conn:
        result=conn.execute(text("""SELECT
    p.project_id,
    p.title,
    AVG(r.rating_value)*0.7+0.3 * COUNT(r.review) AS score
    FROM

    projectrating r
    JOIN
    "Project" p ON r.project_id = p.project_id
    GROUP BY
    p.project_id,
    p.title
    ORDER BY
    score DESC;
    """))
        conn.commit()

        rows=result.fetchall()

        data = [
    {"project_id": row[0], "title": row[1], "score": row[2]}
    for row in rows
]

        #print(data)
        return jsonify({"project": data})

def list_projects_sql(data):
    user_id = data['user_id']
    limit = int(data.get('limit', 10))
    offset = int(data.get('offset', 0))

    with engine.connect() as conn:
     try:
          total_row = conn.execute(text('SELECT COUNT(*) FROM "Project"')).fetchone()
          total = total_row[0] if total_row else 0

          result = conn.execute(text(
             """SELECT
    p.*,
    CASE
        WHEN pm.member_id IS NOT NULL THEN 'Part'
        WHEN p.status IN ('Completed', 'Active') THEN 'Closed'
        WHEN pa.status = 'Pending' THEN 'Pending'
        ELSE 'Apply Now'
    END AS status,
    u.name AS admin_name,
    (SELECT COUNT(*) FROM projectmembers WHERE project_id = p.project_id) AS current_members
FROM "Project" AS p
LEFT JOIN projectmembers AS pm
    ON p.project_id = pm.project_id AND pm.member_id = :val1
LEFT JOIN projectapplication AS pa
    ON p.project_id = pa.project_id AND pa.user_id = :val1
LEFT JOIN "User" u ON u.roll_no = p.admin_id
ORDER BY p.project_id DESC
LIMIT :limit OFFSET :offset
"""
          ), {'val1': user_id, 'limit': limit, 'offset': offset})

          rows = result.fetchall()
          projects = [
              {
                  "project_id": row[0],
                  "admin_id": row[1],
                  "title": row[2],
                  "description": row[3],
                  "start_date": row[4],
                  "end_date": row[5],
                  "members_required": row[6],
                  "status": row[9],
                  "project_status": row[7],
                  "tags": row[8],
                  "admin_name": row[10],
                  "current_members": row[11]
              }
              for row in rows
          ]

          return jsonify({"project": projects, "total": total, "offset": offset, "limit": limit})
     except Exception as e:
            return jsonify({"error": str(e)}), 500


def list_current_projects_sql(data):
   user_id = data.get('user_id')
   if not user_id:
       return jsonify({"error": "user_id required"}), 400
   with engine.connect() as conn:

    try:
       result=conn.execute(text("""select p.*, pm.role, u.name as admin_name,
                                (SELECT COUNT(*) FROM projectmembers WHERE project_id = p.project_id) AS current_members
                                from "Project" as p
                                join projectmembers as pm
                                on  p.project_id=pm.project_id
                                left join "User" u on u.roll_no = p.admin_id
                                 WHERE pm.member_id = :val1
                                and p.status in ('Planning','Active')
       """),
                           {'val1': user_id})
       rows=result.fetchall()
       data = [
    {
        "project_id": row[0],
        "admin_id": row[1],
        "title": row[2],
        "description": row[3],
        "start_date": row[4],
        "end_date": row[5],
        "members_required": row[6],
        "status": row[7],
        "tags": row[8],
        "role": row[9],
        "admin_name": row[10],
        "current_members": row[11]
    }
      for row in rows
]


       return jsonify({"project":data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def list_past_projects_sql(data):
       user_id = data.get('user_id')
       if not user_id:
           return jsonify({"error": "user_id required"}), 400
       with engine.connect() as conn:
          try:
             result=conn.execute(text("""select p.*, pm.role, u.name as admin_name,
                                (SELECT COUNT(*) FROM projectmembers WHERE project_id = p.project_id) AS current_members
                                from "Project" as p
                                join projectmembers as pm
                                on  p.project_id=pm.project_id
                                left join "User" u on u.roll_no = p.admin_id
                                 WHERE pm.member_id = :val1
                                and p.status ='Completed'
       """),
                                 {'val1': user_id})
             rows=result.fetchall()
             data = [
    {
        "project_id": row[0],
        "admin_id": row[1],
        "title": row[2],
        "description": row[3],
        "start_date": row[4],
        "end_date": row[5],
        "members_required": row[6],
        "status": row[7],
        "tags": row[8],
        "role": row[9],
        "admin_name": row[10],
        "current_members": row[11]
    }
      for row in rows
]
             return jsonify({"project":data})


          except Exception as e:
                     return jsonify({"error": str(e)}), 500


def list_myprojects_sql(data):
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    with engine.connect() as conn:
     try:
          result=conn.execute(text(
             """SELECT
    p.*,
    CASE
        WHEN pm.member_id IS NOT NULL AND p.status IN ('Planning','Active') THEN 'Active'
        WHEN pm.member_id IS NOT NULL AND p.status = 'Completed' THEN 'Completed'
        WHEN pa.status = 'Pending' THEN 'Applied'
        ELSE 'Apply Now'
    END AS status,
    u.name AS admin_name,
    (SELECT COUNT(*) FROM projectmembers WHERE project_id = p.project_id) AS current_members,
    pm.role AS user_role
FROM "Project" AS p
LEFT JOIN projectmembers AS pm
    ON p.project_id = pm.project_id AND pm.member_id = :val1
LEFT JOIN projectapplication AS pa
    ON p.project_id = pa.project_id AND pa.user_id = :val1
LEFT JOIN "User" u ON u.roll_no = p.admin_id
    WHERE pm.project_id IS NOT NULL OR pa.project_id IS NOT NULL;


"""
          ),{
  'val1': user_id
          })
          rows = result.fetchall()
          rows_data = [
    {
        "project_id": row[0],
        "admin_id": row[1],
        "title": row[2],
        "description": row[3],
        "start_date": str(row[4]) if row[4] else None,
        "end_date": str(row[5]) if row[5] else None,
        "members_required": row[6],
        "status": row[9],
        "tags": row[8],
        "admin_name": row[10],
        "current_members": row[11],
        "user_role": row[12]
    }
    for row in rows
]
          return jsonify({"project": rows_data})
     except Exception as e:
            return jsonify({"error": str(e)}), 500


def get_project_details(project_id, user_id=None):
    try:
        with engine.connect() as conn:
            project_query = text("""
                SELECT
                    description,
                    title,
                    start_date,
                    end_date,
                    members_required,
                    status,
                    tags,
                    admin_id
                FROM "Project"
                WHERE project_id = :project_id
            """)
            project = conn.execute(project_query, {"project_id": int(project_id)}).fetchone()

            #print(f"Fetched project: {project}")

            if not project:
                return None

            _status_map = {"Planning": "planning", "Active": "running", "Completed": "completed"}
            project_details = {
                "description": project[0],
                "title": project[1],
                "start_date": project[2].isoformat() if project[2] else None,
                "end_date": project[3].isoformat() if project[3] else None,
                "project_size": project[4],
                "project_type": project[5],
                "status": _status_map.get(project[5], "planning"),
                "github_link": None,
                "tech_stack": project[6] if project[6] else [],
                "team_members": [],
                "is_member": False,
                "admin_id": project[7],
            }

            members_query = text("""
                SELECT u.name
                FROM projectmembers pm
                JOIN "User" u ON pm.member_id = u.roll_no
                WHERE pm.project_id = :project_id
            """)
            members = conn.execute(members_query, {"project_id": project_id}).fetchall()

            project_details["team_members"] = [member[0] for member in members]

            if user_id:
                membership = conn.execute(
                    text("SELECT 1 FROM projectmembers WHERE project_id = :project_id AND member_id = :user_id"),
                    {"project_id": project_id, "user_id": user_id}
                ).fetchone()
                project_details["is_member"] = membership is not None

                existing_rating = conn.execute(
                    text("SELECT 1 FROM projectrating WHERE project_id = :project_id AND user_id = :user_id"),
                    {"project_id": project_id, "user_id": user_id}
                ).fetchone()
                project_details["has_rated"] = existing_rating is not None

            rating_row = conn.execute(
                text("SELECT COUNT(*) as cnt, AVG(score) as avg FROM projectrating WHERE project_id = :project_id"),
                {"project_id": project_id}
            ).fetchone()
            rating_count = rating_row[0] if rating_row else 0
            avg_score = float(rating_row[1]) if rating_row and rating_row[1] else None
            project_details["rating_count"] = rating_count
            project_details["rating"] = round(avg_score, 1) if avg_score is not None else None

        return project_details
    except Exception as e:
        print(f"Error in get_project_details: {e}")
        return None


def get_project_analytics(project_id):
    try:
        project_id = int(project_id)

        with engine.connect() as conn:
            # Fetch project start_date and end_date
            proj_query = text("""
                SELECT start_date, end_date
                FROM "Project"
                WHERE project_id = :project_id
            """)
            project = conn.execute(proj_query, {"project_id": project_id}).mappings().fetchone()

            if not project:
                print(f"Project {project_id} not found")
                return None

            # Fetch sprint start and end dates
            sprint_query = text("""
                SELECT sprint_id, name, start_date, end_date
                FROM sprint
                WHERE project_id = :project_id
                ORDER BY sprint_id
            """)
            sprints = conn.execute(sprint_query, {"project_id": project_id}).mappings().all()

            sprint_data = [
                {
                    "sprint_id": s["sprint_id"],
                    "name": s["name"],
                    "start_date": s["start_date"],
                    "end_date": s["end_date"]
                }
                for s in sprints
            ]

            # Fetch tasks
            tasks_query = text("""
                SELECT sprint_number, status, points
                FROM task
                WHERE project_id = :project_id
            """)
            tasks = conn.execute(tasks_query, {"project_id": project_id}).mappings().all()

            # Calculate task stats
            total_tasks = len(tasks)
            completed_tasks = [t for t in tasks if t["status"] == "done"]
            total_completed = len(completed_tasks)
            percentage_completed = (total_completed / total_tasks * 100) if total_tasks > 0 else 0

            # Sprint analysis
            sprint_numbers = [t["sprint_number"] for t in tasks if t["sprint_number"] is not None]
            latest_sprint = max(sprint_numbers, default=None)
            sprint_velocity = (
                sum(t["points"] for t in tasks if t["sprint_number"] == latest_sprint and t["status"] == "done")
                if latest_sprint is not None else 0
            )

            # Team size
            team_query = text("""
                SELECT COUNT(*) as team_count
                FROM projectmembers
                WHERE project_id = :project_id
            """)
            team_result = conn.execute(team_query, {"project_id": project_id}).mappings().fetchone()
            team_count = team_result["team_count"] if team_result else 0

            # Team efficiency
            total_completed_points = sum(t["points"] for t in tasks if t["status"] == "done")
            team_efficiency = len(completed_tasks)/ total_tasks if total_tasks > 0 else 0

            # Pending days calculation
            pending_days = 0
            if project["end_date"]:
                delta = project["end_date"] - date.today()
                pending_days = max(delta.days, 0)

            # Sprint burndown chart
            sprint_progress = {}
            for t in tasks:
                sprint = t["sprint_number"] or 0
                if sprint not in sprint_progress:
                    sprint_progress[sprint] = {"planned": 0, "completed": 0}
                sprint_progress[sprint]["planned"] += t["points"]
                if t["status"] == "done":
                    sprint_progress[sprint]["completed"] += t["points"]

            burndown_data = [
                {
                    "sprint_number": sprint,
                    "planned_points": data["planned"],
                    "completed_points": data["completed"]
                }
                for sprint, data in sorted(sprint_progress.items())
            ]

            velocity_trend = [
                {"sprint_number": sprint, "velocity": data["completed"]}
                for sprint, data in sorted(sprint_progress.items())
            ]

            # Team performance
            performance_query = text("""
                SELECT t.assigned_to::TEXT, COUNT(*) as total_tasks,
                    SUM(CASE WHEN t.status = 'done' THEN 1 ELSE 0 END) as done_tasks
                FROM task t
                WHERE t.project_id = :project_id
                GROUP BY t.assigned_to::TEXT
            """)
            performance = conn.execute(performance_query, {"project_id": project_id}).mappings().all()

            team_performance = []
            for p in performance:
                name_query = text("SELECT name FROM \"User\" WHERE roll_no = :roll_no")
                user = conn.execute(name_query, {"roll_no": p["assigned_to"]}).mappings().fetchone()
                member_name = user["name"] if user else p["assigned_to"]

                completion_rate = (p["done_tasks"] / p["total_tasks"] * 100) if p["total_tasks"] > 0 else 0
                team_performance.append({
                    "member": member_name,
                    "done_tasks": p["done_tasks"],
                    "total_tasks": p["total_tasks"],
                    "completion_rate": round(completion_rate, 2)
                })

            summary = {
                "total_tasks": total_tasks,
                "completed_tasks": total_completed,
                "total_points": sum(t["points"] for t in tasks),
                "completed_points": total_completed_points,
                "team_size": team_count
            }

            analytics = {
                "project_start_date": project["start_date"].isoformat() if project["start_date"] else None,
                "project_end_date": project["end_date"].isoformat() if project["end_date"] else None,
                "sprints": sprint_data,
                "percentage_completed": round(percentage_completed, 2),
                "sprint_velocity": sprint_velocity,
                "team_efficiency": round(team_efficiency, 2),
                "pending_days": pending_days,
                "burndown_data": burndown_data,
                "velocity_trend": velocity_trend,
                "team_performance": team_performance,
                "summary": summary
            }
            print(analytics,"dddddd")
            print(f"Analytics generated for project {project_id}")
            return analytics

    except Exception as e:
        print(f"Error in get_project_analytics: {e}")
        import traceback
        traceback.print_exc()
        return None


def update_project_status(project_id, user_id, new_status):
    """Admin-only: change project status. Accepts 'planning'|'running'|'completed'."""
    STATUS_MAP = {
        "planning": "Planning",
        "running": "Active",
        "completed": "Completed",
    }
    db_status = STATUS_MAP.get(new_status.lower() if new_status else "")
    if not db_status:
        return False, f"Invalid status '{new_status}'"

    try:
        with engine.connect() as conn:
            admin_row = conn.execute(
                text('SELECT admin_id FROM "Project" WHERE project_id = :project_id'),
                {"project_id": project_id}
            ).fetchone()
            if not admin_row:
                return False, "Project not found"
            if str(admin_row[0]) != str(user_id):
                return False, "Only the project admin can change status"

            conn.execute(
                text('UPDATE "Project" SET status = :status WHERE project_id = :project_id'),
                {"status": db_status, "project_id": project_id}
            )
            conn.commit()
        return True, db_status
    except Exception as e:
        print(f"Error updating project status: {e}")
        return False, "Internal server error"


def close_project(project_id, user_id):
    """Set project status to Completed. Only the admin may do this."""
    try:
        with engine.connect() as conn:
            admin_row = conn.execute(
                text('SELECT admin_id FROM "Project" WHERE project_id = :project_id'),
                {"project_id": project_id}
            ).fetchone()

            if not admin_row:
                return False, "Project not found"

            if str(admin_row[0]) != str(user_id):
                return False, "Only the project admin can close this project"

            conn.execute(
                text('UPDATE "Project" SET status = :status WHERE project_id = :project_id'),
                {"status": "Completed", "project_id": project_id}
            )
            conn.commit()
        return True, "Project closed successfully"
    except Exception as e:
        print(f"Error closing project: {e}")
        return False, "Internal server error"


__all__ = [
    "add_projects",
    "ranking",
    "rankings",
    "list_projects_sql",
    "list_current_projects_sql",
    "list_past_projects_sql",
    "list_myprojects_sql",
    "get_project_details",
    "get_project_analytics",
    "close_project",
    "update_project_status",
]
