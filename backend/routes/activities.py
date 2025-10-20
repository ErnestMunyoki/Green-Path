from flask import Blueprint, request, jsonify
from models import db, Activity
from datetime import datetime

activities_bp = Blueprint("activities", __name__, url_prefix="/api")

@activities_bp.route("/activities", methods=["POST"])
def log_activity():
    try:
        data = request.get_json()
        category = data.get("category")
        emission = data.get("emission")
        date_str = data.get("date")

        if not category or emission is None or not date_str:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        activity = Activity(category=category, emission=emission, date=date_obj)
        db.session.add(activity)
        db.session.commit()

        return jsonify({"message": "Activity logged successfully"}), 200

    except Exception as e:
        print("Error logging activity:", e)
        return jsonify({"error": "Internal server error"}), 500



