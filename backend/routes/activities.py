from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models import Activity, db
from datetime import datetime

activities_bp = Blueprint("activities_bp", __name__, url_prefix="/api/activities")

# --- Estimate Emission (fake AI) ---
@activities_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def estimate_emission():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    description = data.get("description", "")
    emission = round(len(description) * 0.1, 2)  # Simple placeholder calculation
    return jsonify({"emission": emission}), 200

# --- Get all activities ---
@activities_bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_activities():
    activities = Activity.query.order_by(Activity.date.desc()).all()
    results = [
        {
            "id": a.id,
            "name": getattr(a, "name", ""),
            "category": getattr(a, "category", ""),
            "emission": getattr(a, "emission", 0),
            "date": a.date.strftime("%Y-%m-%d") if a.date else None,
            "distance_km": getattr(a, "distance_km", 0),
            "vehicle_type": getattr(a, "vehicle_type", "other"),
            "problem": getattr(a, "problem", ""),
            "solution": getattr(a, "solution", "")
        }
        for a in activities
    ]
    return jsonify(results), 200

# --- Log a new activity ---
@activities_bp.route("/log-activity", methods=["POST"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def log_activity():
    data = request.get_json()
    try:
        new_activity = Activity(
            name=data.get("name", ""),
            category=data.get("category", "Uncategorized"),
            emission=data.get("emission", 0),
            date=datetime.strptime(data.get("date"), "%Y-%m-%d") if data.get("date") else datetime.today(),
            distance_km=data.get("distance_km", 0),
            vehicle_type=data.get("vehicle_type", "other"),
            problem=data.get("problem", ""),
            solution=data.get("solution", "")
        )
        db.session.add(new_activity)
        db.session.commit()
        return jsonify({"message": "Activity logged successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
