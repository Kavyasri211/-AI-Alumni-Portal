from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from Backend.database import get_db
bp = Blueprint("auth", __name__)

def clean(r):
    d=dict(r); d.pop("password",None); return d

@bp.post("/login")
def login():
    x=request.get_json() or {}
    c=get_db(); r=c.execute("SELECT * FROM users WHERE email=?",(x.get("email","").lower(),)).fetchone(); c.close()
    if not r or not check_password_hash(r["password"],x.get("password","")):
        return jsonify(error="Invalid email or password"),401
    return jsonify(user=clean(r))

@bp.post("/register")
def register():
    x=request.get_json() or {}
    required=["name","email","password","department","skills","experience","job_role","interests","location"]
    if any(not str(x.get(k,"")).strip() for k in required):
        return jsonify(error="Please fill all required fields"),400
    c=get_db()
    try:
        cur=c.execute("""INSERT INTO users
        (name,email,password,role,department,skills,experience,job_role,interests,location,previous_role,bio)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (x["name"],x["email"].lower(),generate_password_hash(x["password"]),"alumni",
         x["department"],x["skills"],float(x["experience"]),x["job_role"],x["interests"],
         x["location"],x.get("previous_role",""),x.get("bio","")))
        c.commit(); r=c.execute("SELECT * FROM users WHERE id=?",(cur.lastrowid,)).fetchone()
        return jsonify(user=clean(r)),201
    except Exception:
        return jsonify(error="Email already exists"),409
    finally: c.close()
