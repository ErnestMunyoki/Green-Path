# backend/routes/stats.py
from flask import Blueprint, jsonify
from models import Activity
from extensions import db

stats_bp = Blueprint("stats_bp", __name__)

@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        # Fetch all activities from DB
        activities = Activity.query.all()

        total_emissions = sum(a.emission for a in activities)
        total_activities = len(activities)

        # Example monthly breakdown
        monthly_data = [
            {"month": "Jan", "emissions": 20},
            {"month": "Feb", "emissions": 35},
            {"month": "Mar", "emissions": 25},
        ]

        return jsonify({
            "total_emissions": total_emissions,
            "total_activities": total_activities,
            "monthly_data": monthly_data,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
