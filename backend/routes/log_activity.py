from flask import Blueprint, request, jsonify
from models import db, Activity
from datetime import datetime

log_activity_bp = Blueprint("log_activity", __name__)

@log_activity_bp.route("/api/activities", methods=["POST"])
def log_activity():
    data = request.get_json()
    category = data.get("category")
    emission = data.get("emission")
    date_str = data.get("date")

    if not category or emission is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        activity_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        new_activity = Activity(category=category, emission=emission, date=activity_date)
        db.session.add(new_activity)
        db.session.commit()

        return jsonify({"message": "✅ Activity logged successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
