from flask import Blueprint, request, jsonify
from Backend.database import get_db
bp=Blueprint("messages",__name__)
@bp.get("/<int:uid>")
def inbox(uid):
    c=get_db(); r=c.execute("""SELECT m.*,u.name sender_name FROM messages m JOIN users u ON u.id=m.sender_id
    WHERE m.receiver_id=? ORDER BY m.created_at DESC""",(uid,)).fetchall(); c.close()
    return jsonify(messages=[dict(x) for x in r])
@bp.post("")
def send():
    x=request.get_json() or {}; c=get_db()
    c.execute("INSERT INTO messages(sender_id,receiver_id,content) VALUES(?,?,?)",(x["sender_id"],x["receiver_id"],x["content"]))
    c.commit(); c.close(); return jsonify(message="Message sent"),201
