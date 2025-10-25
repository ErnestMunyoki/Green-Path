from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Activity
from services.ai_insights import AIInsightsService
import logging

log_activity_bp = Blueprint("log_activity", __name__, url_prefix="/api")

@log_activity_bp.route("/log-activity", methods=["POST", "OPTIONS"])
def log_activity():
    if request.method == "OPTIONS":
        # Preflight response
        return jsonify({}), 200

    try:
        data = request.get_json()

        # Required fields
        name = data.get("name")
        category = data.get("category")
        date_str = data.get("date")

        if not all([name, category, date_str]):
            return jsonify({"error": "name, category, and date are required"}), 400

        # Parse date safely
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Date must be in YYYY-MM-DD format"}), 400

        # Optional fields with defaults
        distance_km = float(data.get("distance_km", 0))
        vehicle_type = data.get("vehicle_type", "other")

        # Generate AI insight
        ai_result = AIInsightsService.generate_insight(
            activity_name=name,
            distance_km=distance_km,
            vehicle_type=vehicle_type
        )

        # Ensure emission is never None
        emission_value = ai_result.get("emission") or 0.0

        # Save activity in DB
        activity = Activity(
            name=name,
            category=category,
            emission=emission_value,
            problem=ai_result.get("problem", ""),
            solution=ai_result.get("solution", ""),
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
