from flask import Blueprint, request, jsonify
from models import Activity, db
from services.ai_insights import AIInsightsService
from flask_cors import CORS
from datetime import datetime

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")
CORS(ai_bp, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

@ai_bp.route("/estimate-emission", methods=["POST"])
def estimate_emission():
    data = request.get_json()

    name = data.get("name", "").strip() or "Unknown activity"
    user_id = data.get("user_id", 1)
    distance_km = float(data.get("distance_km", 0))
    vehicle_type = data.get("vehicle_type", "other")

    result = AIInsightsService.generate_insight(
        activity_name=name,
        distance_km=distance_km,
        vehicle_type=vehicle_type
    )

    new_activity = Activity(
        user_id=user_id,
        name=result["activity"],
        category="custom",
        emission=result.get("emission") or 0.0,
        problem=result.get("problem", ""),
        solution=result.get("solution", ""),
        date=datetime.utcnow().date()
    )
    db.session.add(new_activity)
    db.session.commit()

    return jsonify(result), 201
