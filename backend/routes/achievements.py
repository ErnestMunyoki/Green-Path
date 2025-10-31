from flask import Blueprint, jsonify
from flask_cors import cross_origin
from models import Achievement

achievements_bp = Blueprint("achievements_bp", __name__, url_prefix="/api/achievements")

@achievements_bp.route("/", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app", 
    "http://localhost:5173",              
    "http://127.0.0.1:5173"
])

def get_achievements():
    """
    Returns all achievements from the database in JSON format.
    """
    try:
        achievements = Achievement.query.order_by(Achievement.id).all()

        result = [
            {
                "id": a.id,
                "title": a.title,
                "description": getattr(a, "description", ""),  
                "unlocked": getattr(a, "unlocked", False)    
            }
            for a in achievements
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
