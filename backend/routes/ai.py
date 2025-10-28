from flask import Blueprint, request, jsonify
from services.ai_insights import AIInsightsService
import logging

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
def estimate_emission():
    if request.method == "OPTIONS":
        return jsonify({}), 200  # CORS preflight

    try:
        data = request.get_json() or {}
        logging.info(f"AI payload received: {data}")

        name = str(data.get("name", "")).strip() or "Unknown activity"
        try:
            distance_km = float(data.get("distance_km", 0))
        except (TypeError, ValueError):
            distance_km = 0.0
        vehicle_type = str(data.get("vehicle_type", "other")).strip() or "other"

        # Generate AI insight safely
        ai_result = {
            "emission": 0.0,
            "problem": "No problem generated.",
            "solution": "Try again later.",
            "recommendation": "No recommendation provided.",
            "activity": name,
            "distance_km": distance_km,
            "vehicle_type": vehicle_type
        }

        try:
            output = AIInsightsService.generate_insight(
                activity_name=name,
                distance_km=distance_km,
                vehicle_type=vehicle_type
            )
            if isinstance(output, dict):
                ai_result.update(output)
        except Exception as e:
            logging.warning(f"⚠️ AI generation failed: {e}")

        return jsonify(ai_result), 200

    except Exception as e:
        logging.error(f"❌ AI endpoint error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
