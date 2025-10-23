from flask import Blueprint, request, jsonify
from models import Activity, db
from services.ai_insights import AIInsightsService
from datetime import datetime

# Define Blueprint
ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
def estimate_emission():
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()

    # ✅ Extract data from request
    name = data.get("name", "").strip() or "Unknown activity"
    user_id = data.get("user_id", 1)
    distance_km = float(data.get("distance_km", 0))
    vehicle_type = data.get("vehicle_type", "other")

    # ✅ Generate AI-based insight
    result = AIInsightsService.generate_insight(
        activity_name=name,
        distance_km=distance_km,
        vehicle_type=vehicle_type
    )

    # ✅ Save activity in database
    new_activity = Activity(
        user_id=user_id,
        name=result["activity"],
        category="custom",
        emission=result["emission"],
        problem=result["problem"],
        solution=result["solution"],
        date=datetime.utcnow().date()
    )
    db.session.add(new_activity)
    db.session.commit()

    # ✅ Return AI insight response to frontend
    return jsonify(result), 201
