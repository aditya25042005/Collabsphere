from sqlalchemy import text
from flask import jsonify
from app.extensions import engine


def list_of_mentors_sql(data):
   #list of mentors  # addxtaus of reject applied pending
   ##first check whether project  has mentor or not.
 with engine.connect() as conn:

   result0=conn.execute(text("""select * from "projectmembers" where project_id=:val1 and role=:val2"""),{


        "val1":data['project_id'],
        "val2":"mentor"
   })
   if result0.rowcount>0:
        return jsonify({"mentor":"already exist"})
   else:
     project_id=data['project_id']
     with engine.connect() as conn:
      try:
        # return   in it the alumini professr to whom he applied status
         query = text("""
   SELECT
    u.*,
    CASE
        WHEN m.status = 'Pending' THEN 'Pending'
        ELSE 'Apply'
    END AS status
FROM "User" u
LEFT JOIN "mentorrequest" m
    ON u.roll_no = m.mentor_id
    AND m.project_id = :project_id  -- Filter for a specific project
WHERE u.role_type IN ('professor', 'alumni');

""")

         result = conn.execute(query, {"project_id": project_id})
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
        "name":row[10],
        "status": row[11]

    }
        for row in rows
]
         return jsonify({"mentor":data})
      except Exception as e:
          return jsonify({"error": str(e)}), 500

def apply_mentors_sql(data):
   #apply for mentor
   with engine.connect() as conn:
      try:
          #check forreuested at
          result=conn.execute(text("""INSERT INTO "MentorRequest" (project_id, admin_id, mentor_id, status, requested_at, remarks)
VALUES (:val1, :val2, :val3, :val4, :val5, :val6);
 """),{
    "val1":data['project_id'],
    "val2":data['admin_id'],
    "val3":data['mentor_id'],
    "val4":data['status'],
    "val5":data['requested_at'],
    "val6":data['remarks']
 })
          conn.commit()
          return jsonify({"mentor":"applied"})
      except Exception as e:

       return jsonify({"error": str(e)}), 500

def apply_mentors_takeback_sql(data):
    with engine.connect() as conn:
        try:
            result=conn.execute(text("""DELETE FROM "MentorRequest" WHERE mentor_id = :val1 AND project_id = :val2;"""),{
              "val1":data["mentor_id"],
              "val2":data["project_id"]

            })
            conn.commit()
            return jsonify({"request":"taken"})
        except Exception as e:
             return jsonify({"error": str(e)}), 500


def accept_mentor_sql(data):
 #update ,push to project member table ,delete other mentor request
  with engine.connect() as conn:
     try:

        ##cond if  metnor page is not updated and  mentor accepted then error wll come handle that
        #update
        result=conn.execute(text("""
    UPDATE "mentorrequest"
    SET status = :status
    WHERE mentor_id = :mentor_id AND project_id = :project_id;
"""),{

    "status": data["status"],  # "Accepted" or "Rejected"
    "mentor_id": data["mentor_id"],
    "project_id": data["project_id"]
})

        if data['status']=='Accepted':

            ### delete other mentor request
         result1=conn.execute(text("""
 DELETE FROM "mentorrequest"
    WHERE project_id = :project_id AND status IN ('Rejected', 'Pending');


"""
        ),{
                "project_id": data["project_id"]


                }
                )
        ### insert into project members table
        result2=conn.execute(text("""
INSERT INTO "projectmembers" (project_id, user_id, role)
VALUES (:val1, :val2, :val3);
"""),{
    "val1":data['project_id'],
    "val2":data['mentor_id'],
    "val3":"mentor"
})
        conn.commit()
        return jsonify({"mentor":"accepted"})


     except Exception as e:
            return jsonify({"error": str(e)}), 500


__all__ = [
    "list_of_mentors_sql",
    "apply_mentors_sql",
    "apply_mentors_takeback_sql",
    "accept_mentor_sql",
]
