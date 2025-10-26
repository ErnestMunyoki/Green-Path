from flask import Blueprint, jsonify
from models import Achievement

achievements_bp = Blueprint("achievements", __name__)

@achievements_bp.route("/api/achievements", methods=["GET"])
def get_achievements():
    data = Achievement.query.all()
    result = [
        {"title": a.title, "unlocked": a.unlocked}
        for a in data
    ]
    return jsonify(result)