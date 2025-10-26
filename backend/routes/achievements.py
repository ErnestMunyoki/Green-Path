from flask import Blueprint, jsonify
from models import Achievement

achievements_bp = Blueprint("achievements", __name__)

@achievements_bp.route("/all", methods=["GET"])
def get_achievements():
    achievements = Achievement.query.all()
    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "date_earned": a.date_earned.isoformat(),
            "unlocked": True  # Replace with actual logic if needed
        }
        for a in achievements
    ])
