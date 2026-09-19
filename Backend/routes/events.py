from flask import Blueprint, request, jsonify
from Backend.database import get_db
bp=Blueprint("events",__name__)
@bp.get("")
def events():
    c=get_db(); r=c.execute("SELECT * FROM events ORDER BY event_date").fetchall(); c.close()
    return jsonify(events=[dict(x) for x in r])
@bp.post("")
def add():
    x=request.get_json() or {}
    c=get_db(); cur=c.execute("INSERT INTO events(title,description,event_date,location) VALUES(?,?,?,?)",
      (x.get("title"),x.get("description"),x.get("event_date"),x.get("location",""))); c.commit()
    r=c.execute("SELECT * FROM events WHERE id=?",(cur.lastrowid,)).fetchone(); c.close()
    return jsonify(event=dict(r)),201
