from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models import Activity

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def estimate_emission():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    description = data.get("description", "")
    emission = len(description) * 0.1
    return jsonify({"emission": emission}), 200

@activities_bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_activities():
    activities = Activity.query.order_by(Activity.date.desc()).all()

    results = [
        {
            "id": a.id,
            "category": a.category,
            "emission": a.emission,
            "date": a.date.strftime("%Y-%m-%d"),
        }
        for a in activities
    ]

    return jsonify(results), 200
