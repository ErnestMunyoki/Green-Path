from flask import Blueprint, request, jsonify
from models import db, Activity
from datetime import date

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/api/activities", methods=["POST"])
def log_activity():
    data = request.get_json()
    activity = Activity(
        category=data["category"],
        emission=data["emission"],
        date=date.fromisoformat(data["date"])
    )
    db.session.add(activity)
    db.session.commit()
    return jsonify({"message": "Activity logged successfully"}), 201
