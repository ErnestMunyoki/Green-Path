from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Activity
from services.ai_insights import AIInsightsService

log_activity_bp = Blueprint("log_activity", __name__, url_prefix="/api")

@log_activity_bp.route("/log-activity", methods=["POST"])
def log_activity():
    try:
        data = request.get_json()
        category = data.get("category")
        emission = data.get("emission")
        date_str = data.get("date")

        if not all([category, emission, date_str]):
            return jsonify({"error": "category, emission, and date are required"}), 400

        # Convert emission to float
        try:
            emission = float(emission)
        except ValueError:
            return jsonify({"error": "Emission must be a number"}), 400

        # Convert date string to datetime.date
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Date must be YYYY-MM-DD format"}), 400

        # Save activity
        activity = Activity(category=category, emission=emission, date=date_obj)
        db.session.add(activity)
        db.session.commit()

        # AI analysis
        activities = Activity.query.all()  # filter by user if needed
        problem = AIInsightsService.generate_insight(activities)
        prediction = AIInsightsService.predict_emissions_next_week(activities)

        return jsonify({
            "message": "Activity logged successfully",
            "problem": problem,
            "predicted_emissions": prediction.get("predicted_emissions", 0),
            "solution": "Try reducing high-emission activities like driving and eating meat."
        }), 201

    except Exception as e:
        import logging
        logging.error(f"Log Activity Error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
