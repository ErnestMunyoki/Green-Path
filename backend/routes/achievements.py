from flask import Blueprint, jsonify
from flask_cors import cross_origin
from models import Achievement

# Create the blueprint with a proper prefix
achievements_bp = Blueprint("achievements_bp", __name__, url_prefix="/api/achievements")

@achievements_bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_achievements():
    """
    Returns all achievements from the database in JSON format.
    """
    try:
        # Fetch all achievements from the database
        achievements = Achievement.query.order_by(Achievement.id).all()

        # Convert each achievement to a JSON-serializable dict
        result = [
            {
                "id": a.id,
                "title": a.title,
                "description": getattr(a, "description", ""),  # Default to empty string
                "unlocked": getattr(a, "unlocked", False)      # Default to False if not defined
            }
            for a in achievements
        ]

        return jsonify(result), 200

    except Exception as e:
        # Return a JSON error if something goes wrong
        return jsonify({"error": str(e)}), 500
