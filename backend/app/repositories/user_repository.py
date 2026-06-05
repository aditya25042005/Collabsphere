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


def list_users_sql():
   #for students only:
   with engine.connect() as conn:
        try:
            query = text("""
                SELECT
                    u.*,

                    COUNT(u.roll_no) AS project_count
                FROM
                    "User" u
                LEFT JOIN
                    "projectmembers" p ON u.roll_no = p.member_id
                left JOIN
                    "Project" pa ON p.project_id = pa.project_id

                GROUP BY
                    u.roll_no
            """)

            result = conn.execute(query)
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
                    "name":row[10],
                    "project_count": row[11]   # Count of users per project
                }
                for row in rows
            ]

            return jsonify({"projects": data})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


__all__ = [
    "insert",
    "user_insert_google_sql",
    "first_logins",
    "profile_views",
    "update_profile_sql",
    "list_users_sql",
]
