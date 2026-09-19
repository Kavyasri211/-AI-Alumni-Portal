from flask import Blueprint, request, jsonify
from Backend.database import get_db
bp=Blueprint("alumni",__name__)

@bp.get("")
def all_alumni():
    q=request.args.get("q","").strip()
    c=get_db()
    if q:
        like=f"%{q}%"
        rs=c.execute("""SELECT id,name,department,skills,experience,job_role,interests,location,previous_role,bio
        FROM users WHERE role='alumni' AND (name LIKE ? OR department LIKE ? OR skills LIKE ? OR job_role LIKE ? OR location LIKE ?)""",
        (like,like,like,like,like)).fetchall()
    else:
        rs=c.execute("""SELECT id,name,department,skills,experience,job_role,interests,location,previous_role,bio
        FROM users WHERE role='alumni'""").fetchall()
    c.close(); return jsonify(alumni=[dict(r) for r in rs])

@bp.get("/<int:uid>")
def one(uid):
    c=get_db(); r=c.execute("""SELECT id,name,email,department,skills,experience,job_role,interests,location,previous_role,bio
    FROM users WHERE id=?""",(uid,)).fetchone(); c.close()
    return (jsonify(alumni=dict(r)),200) if r else (jsonify(error="Not found"),404)

@bp.put("/<int:uid>")
def update(uid):
    x=request.get_json() or {}; fields=["name","department","skills","experience","job_role","interests","location","previous_role","bio"]
    c=get_db(); c.execute("""UPDATE users SET name=?,department=?,skills=?,experience=?,job_role=?,interests=?,location=?,previous_role=?,bio=? WHERE id=?""",
      tuple(x.get(f,"") for f in fields)+(uid,)); c.commit()
    r=c.execute("SELECT id,name,email,department,skills,experience,job_role,interests,location,previous_role,bio FROM users WHERE id=?",(uid,)).fetchone(); c.close()
    return jsonify(alumni=dict(r))
