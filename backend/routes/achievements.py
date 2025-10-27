from flask import Blueprint, jsonify
from flask_cors import cross_origin
from models import Achievement

achievements_bp = Blueprint("achievements_bp", __name__)

@achievements_bp.route("/", methods=["GET"])
@cross_origin()  # Allow CORS
def get_achievements():
    achievements = Achievement.query.order_by(Achievement.id).all()
    result = []

    for a in achievements:
        result.append({
            "title": a.title,
            "description": a.description,
            "unlocked": True  # Static, since thresholds don't exist yet
        })

    return jsonify(result), 200
