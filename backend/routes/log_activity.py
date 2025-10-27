from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Activity
from services.ai_insights import AIInsightsService
import logging

log_activity_bp = Blueprint("log_activity", __name__, url_prefix="/api")

@log_activity_bp.route("/log-activity", methods=["POST", "OPTIONS"])
def log_activity():
    if request.method == "OPTIONS":
        return jsonify({}), 200  # CORS preflight

    try:
        data = request.get_json() or {}
        logging.info(f"📩 Payload received for logging: {data}")

        # Required fields with safe defaults
        name = str(data.get("name", "")).strip() or "Unnamed activity"
        category = str(data.get("category", "")).strip() or "Uncategorized"

        # Safe user_id
        try:
            user_id = int(data.get("user_id", 1))
        except (TypeError, ValueError):
            user_id = 1

        # Safe date parsing
        date_str = str(data.get("date", "")).strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            date_obj = datetime.utcnow()

        # Safe emission, problem, solution
        try:
            emission = float(data.get("emission", 0))
        except (TypeError, ValueError):
            emission = 0.0

        problem = str(data.get("problem", "No problem provided."))
        solution = str(data.get("solution", "No solution provided."))

        # ✅ AI insight fallback
        try:
            ai_output = AIInsightsService.generate_insight(
                activity_name=name,
                distance_km=float(data.get("distance_km", 0)),
                vehicle_type=str(data.get("vehicle_type", "other"))
            )
            if isinstance(ai_output, dict):
                emission = float(ai_output.get("emission", emission))
                problem = str(ai_output.get("problem", problem))
                solution = str(ai_output.get("solution", solution))
        except Exception as ai_err:
            logging.warning(f"⚠️ AI insight generation failed: {ai_err}")

        # Create and commit activity
        activity = Activity(
            user_id=user_id,
            name=name,
            category=category,
            emission=emission,
            problem=problem,
            solution=solution,
            date=date_obj
        )

        db.session.add(activity)
        db.session.commit()

        logging.info(f"✅ Activity '{name}' logged successfully for user_id {user_id}.")

        return jsonify({
            "message": "Activity logged successfully",
            "ai_insight": {
                "emission": emission,
                "problem": problem,
                "solution": solution
            }
        }), 201

    except Exception as e:
        logging.error(f"❌ Log Activity Error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
