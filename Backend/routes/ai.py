from flask import Blueprint, request, jsonify
from Backend.services.ml_service import recommend
from Backend.services.genai_service import generate_content
bp=Blueprint("ai",__name__)
@bp.get("/recommend/<int:uid>")
def rec(uid): return jsonify(recommendations=recommend(uid))
@bp.post("/generate")
def gen():
    return jsonify(result=generate_content(request.get_json() or {}))
