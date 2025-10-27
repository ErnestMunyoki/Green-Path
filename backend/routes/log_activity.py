from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Activity
from services.ai_insights import AIInsightsService
import logging

log_activity_bp = Blueprint("log_activity", __name__, url_prefix="/api")

@log_activity_bp.route("/log-activity", methods=["POST", "OPTIONS"])
def log_activity():
    if request.method == "OPTIONS":
        return jsonify({}), 200  

    try:
        data = request.get_json()
        logging.info(f"Received payload: {data}")

        if not data:
            return jsonify({"error": "Missing JSON payload"}), 400

        name = data.get("name", "").strip()
        category = data.get("category", "").strip()
        date_str = data.get("date", "").strip()

        if not name or not category or not date_str:
            return jsonify({"error": "name, category, and date are required"}), 400

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Date must be in YYYY-MM-DD format"}), 400

        try:
            distance_km = float(data.get("distance_km", 0))
        except (TypeError, ValueError):
            distance_km = 0.0

        vehicle_type = data.get("vehicle_type", "other")

        try:
            ai_result = AIInsightsService.generate_insight(
                activity_name=name,
                distance_km=distance_km,
                vehicle_type=vehicle_type
            )
        except Exception as ai_error:
            logging.warning(f"AI insight generation failed: {ai_error}")
            ai_result = {
                "emission": 0.0,
                "problem": "AI service unavailable.",
                "solution": "Try again later."
            }

        emission_value = ai_result.get("emission") or 0.0
        problem_text = ai_result.get("problem", "")
        solution_text = ai_result.get("solution", "")

        activity = Activity(
            name=name,
            category=category,
            emission=emission_value,
            problem=problem_text,
            solution=solution_text,
            date=date_obj
        )
        db.session.add(activity)
        db.session.commit()

        return jsonify({
            "message": "Activity logged successfully",
            "ai_insight": ai_result
        }), 201

    except Exception as e:
        logging.error(f"Log Activity Error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
