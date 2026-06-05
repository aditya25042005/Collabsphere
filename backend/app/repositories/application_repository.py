from sqlalchemy import text
from flask import jsonify, request
from app.extensions import engine


def apply_project_sql(data):

   #apply for role in project
   with engine.connect() as conn:
      try:
         result=conn.execute(text("""Insert into "projectapplication" (user_id,project_id,role,remarks)
    VALUES(:val1,:val2,:val3,:val4);"""),{
       "val1":data['user_id'],
       "val2":data['project_id'],
        "val3":data['role'],
        "val4":data['remarks']
         })
         conn.commit()
         return jsonify({"project":"applied"})
      except Exception as e:
            return jsonify({"error": str(e)}), 500


def apply_project_status_sql(data):
   with engine.connect() as conn:
      try:
          #for single project and a user application status
         result=conn.execute(text("""select * from "projectapplication" where user_id=:val1 and project_id=:val2"""),{
       "val1":data['user_id'],
       "val2":data['project_id']
         })
         conn.commit()
         rows=result.fetchall()
         data = [
    {
          "application_id": row[0],
        "user_id":row[1],
        "project_id":row[2],
        "role":row[3],
        "status":row[4],
        "remarks":row[5]

    }
        for row in rows
]

         return jsonify({"project_status":data})

      except Exception as e:
            return jsonify({"error": str(e)}), 500


def apply_project_status_takeback_sql(data):

   with engine.connect() as conn:
      try:
         result=conn.execute(text("""DELETE FROM "projectapplication" WHERE user_id = :val1 AND project_id = :val2;"""),{
           "val1":data["user_id"],
           "val2":data["project_id"]
         })
         print(data["user_id"],data["project_id"])
         conn.commit()
         return jsonify({"request":"taken"})
      except Exception as e:
          return jsonify({"error": str(e)}), 500


def list_apply_project_sql(data):
   # for single project how many people applied
   with engine.connect() as conn:
        try:
          result=conn.execute(text("""select * from "projectapplication" where project_id=:val1"""),{
              "val1":data['project_id']
          })

          rows=result.fetchall()
          data = [
    {
          "application_id": row[0],
        "user_id":row[1],
        "project_id":row[2],
        "role":row[3],
        "status":row[4],
        "remarks":row[5]

    }
        for row in rows
]
          return jsonify({"project_list":data})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

def update_project_application_status_sql(data):
# ak update status by admin and add in project members table
    # update /apply/takeback project applied
    #user_id which sent
    with engine.connect() as conn:
      try:
         results = conn.execute(text("""
                UPDATE projectapplication
                SET status = :status
                WHERE user_id = :user_id AND project_id = :project_id
            """), {
                "status": data["status"],
                "user_id": data["user_id"],
                "project_id": data["project_id"]
            })

         conn.commit()

         if results.rowcount == 0:
                return jsonify({"error": "Application not found"}), 404

         else:
            with engine.connect() as conn:

                  if data["status"] =="Accepted":

                    #take role from project application table
                       # include in pm table
                       #delete from project application table
                    result1=conn.execute(text("""select * from projectapplication

                      where user_id=:val1 and project_id=:val2



                                              """),{

                "val1":data["user_id"],
                "val2":data["project_id"]


                                              })

                    rows=result1.fetchall()
                    datas = [
    {
          "application_id": row[0],
        "user_id":row[1],
        "project_id":row[2],
        "role":row[3],
        "status":row[4],
        "remarks":row[5]

    }
        for row in rows
]


                                         # include in pm table
                    with engine.connect() as conn:
                        res=conn.execute(text(""" INSERT INTO "projectmembers" (project_id, member_id, role)
        VALUES (:project_id, :member_id, :role)"""),{
  "member_id": data["user_id"],
                    "project_id": data["project_id"],
                    "role": datas[0]["role"] #add later

        })
                        conn.commit()



                    with engine.connect() as conn:
                      result3=conn.execute(text("""

DELETE FROM projectapplication WHERE user_id = :val1 and project_id=:val2


                                            """),{


"val1":data["user_id"],
"val2":data["project_id"]


                                            })
                      conn.commit()



                  else:
                       result4=conn.execute(text("""

DELETE FROM projectapplication WHERE user_id = :val1


                                            """),{


"val1":data["user_id"]


                                            })
                       conn.commit()

         return jsonify({"project":"updated"})



      except Exception as e:
            return jsonify({"error": str(e)}), 500


def admin_request_sql(data):
     with engine.connect() as conn:
      try:
         result=conn.execute(text("""Insert into "projectjoin" (user_id,project_id,role,remarks)
    VALUES(:val1,:val2,:val3,:val4);"""),{
       "val1":data['to_user_id'],
       "val2":data['project_id'],
        "val3":data['role'],
        "val4":data['remarks']
         })
         conn.commit()
         return jsonify({"user":"requested"})
      except Exception as e:
            return jsonify({"error": str(e)}), 500


def admin_request_accept_sql(data):
    data = request.json
    query_check_exists = text("""
        SELECT COUNT(*) FROM "projectjoin"
        WHERE user_id = :user_id AND project_id = :project_id;
    """)
    query_update = text("""
        UPDATE "projectjoin"
        SET status = :status
        WHERE user_id = :user_id AND project_id = :project_id;
    """)

    query_insert_member = text("""
        INSERT INTO "projectmembers" (project_id, member_id, role)
        VALUES (:project_id, :member_id, :role)
    """)

    query_delete_others = text("""
        DELETE FROM "projectjoin"
        WHERE project_id = :project_id
        AND user_id = :user_id;
    """)

    try:
        with engine.connect() as conn:
            result = conn.execute(query_check_exists, {
                "user_id": data["user_id"],
                "project_id": data["project_id"]
            })
            request_exists = result.scalar() # Get the count result
            print(request_exists,"ss")
            if request_exists == 0:
                return jsonify({"error": "No join request found"}), 400
            conn.execute(query_update, {
                "status": data["status"],
                "user_id": data["user_id"],
                "project_id": data["project_id"]
            })

            if data["status"] == "Accepted":
                 result1=conn.execute(text("""select * from projectjoin

                      where user_id=:val1 and project_id=:val2



                                              """),{

                "val1":data["user_id"],
                "val2":data["project_id"]


                                              })

                 rows=result1.fetchall()
                 datas = [
    {
          "application_id": row[0],
        "user_id":row[1],
        "project_id":row[2],
        "role":row[3],
        "status":row[4],
        "remarks":row[5]

    }
        for row in rows
]

                 conn.execute(query_insert_member, {
                    "member_id": data["user_id"],
                    "project_id": data["project_id"],
                    "role": datas[0]["role"] #add later
                })

                 conn.execute(query_delete_others, {
                    "project_id": data["project_id"],
                    "user_id": data["user_id"]
                })

                 conn.commit()
            else:
              conn.execute(query_delete_others, {
                    "project_id": data["project_id"],
                    "user_id": data["user_id"]
                })
              conn.commit()
            return jsonify({"request": "updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def notification_sql(data):
 print(data,"sd")
 with engine.connect() as conn:
    result = conn.execute(text("""
    SELECT *
    FROM projectapplication AS pa
    JOIN "Project" AS p

    ON p.project_id = pa.project_id
    WHERE p.admin_id=:user_id
    AND pa.status = 'Pending'
"""), {"user_id": data["user_id"]})
    pending_applications = result.fetchall()

    applications_json = [
    {
        "application_id": application[0],
        "user_id": application[1],
        "project_id": application[2],
        "role": application[3],
        "status": application[4],
        "applied_at": application[5].isoformat(),  # Convert timestamp to ISO format string
        "remarks": application[6],
        "applied":"user",
        "title":application[9]
    }
    for application in pending_applications
    ]

    result = conn.execute(text("""
    SELECT *
    FROM projectjoin
    WHERE user_id = :user_id
    AND status = 'Pending';
"""), {"user_id": data["user_id"]})


    project_join_results = result.fetchall()

    project_joins_json = [
    {
        "application_id": application[0],
        "user_id": application[1],
        "project_id": application[2],
        "role": application[3],
        "status": application[4],
        "applied_at": application[5].isoformat(),  # Convert timestamp to ISO format string
        "remarks": application[6],
        "applied":"admin"
    }
    for application in project_join_results
    ]
    all_notifications_json = applications_json + project_joins_json
    return jsonify({"notification":all_notifications_json}),200


__all__ = [
    "apply_project_sql",
    "apply_project_status_sql",
    "apply_project_status_takeback_sql",
    "list_apply_project_sql",
    "update_project_application_status_sql",
    "admin_request_sql",
    "admin_request_accept_sql",
    "notification_sql",
]
