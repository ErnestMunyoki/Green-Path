from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models import Activity
from datetime import date, timedelta

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/api/stats")

@stats_bp.route("/weekly-emissions", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_weekly_emissions():
    """
    Returns total emissions grouped by each weekday for the current week.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = date.today()
        week_start = today - timedelta(days=today.weekday())  
        week_end = week_start + timedelta(days=6)

        query = Activity.query.filter(Activity.date >= week_start, Activity.date <= week_end)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()

        weekly_data = {
            (week_start + timedelta(days=i)).strftime("%A"): 0.0 for i in range(7)
        }

        for activity in activities:
            day_name = activity.date.strftime("%A")
            weekly_data[day_name] += activity.emission

        return jsonify(weekly_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stats_bp.route("/monthly-stats", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_monthly_stats():
    """
    Returns total emissions per day for the last 30 days.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = date.today()
        start = today - timedelta(days=30)

        query = Activity.query.filter(Activity.date >= start)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()

        result = {}
        for activity in activities:
            day = activity.date.strftime("%Y-%m-%d")
            result[day] = result.get(day, 0) + activity.emission

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@stats_bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_overall_stats():
    """
    Returns total activities, total emissions, and daily average.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        query = Activity.query
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()

        total_activities = len(activities)
        total_emission = sum(a.emission for a in activities)
        avg_emission = total_emission / total_activities if total_activities > 0 else 0

        return jsonify({
            "total_activities": total_activities,
            "total_emission": round(total_emission, 2),
            "average_emission": round(avg_emission, 2),
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
