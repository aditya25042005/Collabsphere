from sqlalchemy import text
from flask import jsonify
from app.extensions import engine


def insert():
    # Insert user data into the database
    with engine.connect() as conn:
        query = text("""
            INSERT INTO "User" (roll_no, name, email)
            VALUES (:roll_no, :name, :email)
        """)
        conn.execute(query, {
            "roll_no": "sds",
            "name":"Adi",
            "email": "wwd"
        })
        conn.commit()  # Commit the transaction
        return jsonify({"project":"added"})


def user_insert_google_sql(data):
    try:
        with engine.connect() as conn:
            # Upsert: insert if not exists, update name/email if already registered
            query = text("""
                INSERT INTO "User" (roll_no, name, email)
                VALUES (:roll_no, :name, :email)
                ON CONFLICT (roll_no) DO UPDATE
                    SET name  = EXCLUDED.name,
                        email = EXCLUDED.email
            """)
            conn.execute(query, {
                "roll_no": data["roll_no"],
                "name":    data["user_name"],
                "email":   data["email"],
            })
            conn.commit()
        return jsonify({"user": "ok"})
    except Exception as e:
        return f"Error: {str(e)}"

def first_logins(data):
       with engine.connect() as conn:
           try:
            result=conn.execute(text("""select * from "User" where roll_no=:val1"""),{
               "val1":data.get('roll_no')})

            conn.commit()
            if(result.rowcount>0):
               return jsonify ({"user":True})
            else:
             return jsonify ({"user":False})
           except Exception as e:
               return jsonify({"error": str(e)}), 500

def profile_views(data):
    #user profile view
    with engine.connect() as conn:
        try:
          result=conn.execute(text("""select * from "User" where roll_no=:val1"""),{

              "val1":data.get('roll_no')})

          conn.commit()
          rows=result.fetchall()
          data = [
    {
        "roll_no": row[0],
        "email": row[1],
        "past_experience": row[2],
        "tech_stack": row[3],
        "github_profile": row[4],
        "linkedin_profile": row[5],
        "role_type": row[6],
        "rating": row[7]  ,
        "email_update": row[8],
        "project_update": row[9],
        "name":row[10]
    }
    for row in rows
]
          if(result.rowcount==0):
              return jsonify({"user":False})
          else:
           return jsonify({"user": data})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

def update_profile_sql(data):
   with engine.connect() as conn:
        try:
            query = text("""
        UPDATE "User"
        SET

            past_experience = :past_experience,
            tech_stack = :tech_stack,
            github_profile = :github_profile,
            linkedin_profile = :linkedin_profile



        WHERE roll_no = :roll_no
    """)

            conn.execute(query, {

        "past_experience": data["past_experience"],
        "tech_stack": data["tech_stack"],
        "github_profile": data["github_profile"],
        "linkedin_profile": data["linkedin_profile"],
        "roll_no":data["roll_no"]



    })

            conn.commit()
            return jsonify({"profile":"updated"})
        except Exception as e:

            print(e,"s")
            return jsonify({"error": str(e)}), 500
            print(e,"s")


def list_users_sql(limit=10, offset=0, search="", skills=None):
    """List users with optional full-text search and skill filtering, paginated."""
    with engine.connect() as conn:
        try:
            search_param = f"%{search}%" if search else "%"
            params = {"search": search_param, "limit": limit, "offset": offset}

            # Build skill filter clauses — each skill must appear in tech_stack (case-insensitive)
            skill_clauses = ""
            if skills:
                for i, skill in enumerate(skills):
                    key = f"skill_{i}"
                    skill_clauses += f"""
                        AND EXISTS (
                            SELECT 1 FROM unnest(u.tech_stack) s
                            WHERE s ILIKE :{key}
                        )"""
                    params[key] = skill

            count_sql = f"""
                SELECT COUNT(DISTINCT u.roll_no)
                FROM "User" u
                WHERE (u.name ILIKE :search OR u.email ILIKE :search)
                {skill_clauses}
            """
            total_row = conn.execute(text(count_sql), params).fetchone()
            total = total_row[0] if total_row else 0

            query_sql = f"""
                SELECT
                    u.*,
                    COUNT(p.project_id) AS project_count
                FROM "User" u
                LEFT JOIN "projectmembers" p ON u.roll_no = p.member_id
                WHERE (u.name ILIKE :search OR u.email ILIKE :search)
                {skill_clauses}
                GROUP BY u.roll_no
                ORDER BY u.name ASC
                LIMIT :limit OFFSET :offset
            """
            result = conn.execute(text(query_sql), params)
            rows = result.fetchall()

            data = [
                {
                    "roll_no": row[0],
                    "email": row[1],
                    "past_experience": row[2],
                    "tech_stack": row[3],
                    "github_profile": row[4],
                    "linkedin_profile": row[5],
                    "role_type": row[6],
                    "rating": row[7],
                    "email_update": row[8],
                    "project_update": row[9],
                    "name": row[10],
                    "project_count": row[11]
                }
                for row in rows
            ]

            return jsonify({"projects": data, "total": total, "offset": offset, "limit": limit})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


def list_skills_sql():
    """Return all unique skills from tech_stack, lowercased and deduplicated."""
    with engine.connect() as conn:
        try:
            rows = conn.execute(text("""
                SELECT DISTINCT lower(skill) AS skill
                FROM "User", unnest(tech_stack) AS skill
                WHERE skill IS NOT NULL AND skill <> ''
                ORDER BY skill ASC
            """)).fetchall()
            return jsonify({"skills": [row[0] for row in rows]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


__all__ = [
    "insert",
    "user_insert_google_sql",
    "first_logins",
    "profile_views",
    "update_profile_sql",
    "list_users_sql",
    "list_skills_sql",
]
