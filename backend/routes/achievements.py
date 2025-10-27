from flask import Blueprint, jsonify
from flask_cors import cross_origin
from models import Achievement, db

achievements_bp = Blueprint("achievements_bp", __name__, url_prefix="/api/achievements")

@achievements_bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_achievements():
    """
    Returns all achievements from the database in JSON format.
    """
    try:
        achievements = Achievement.query.all()
        result = [
            {
                "id": a.id,
                "title": a.title,
                "description": a.description if hasattr(a, "description") else "",
                "unlocked": a.unlocked
            }
            for a in achievements
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
