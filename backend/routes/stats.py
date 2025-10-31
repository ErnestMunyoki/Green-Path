from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models import Activity
from datetime import date, timedelta, datetime

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/api/stats")

# --- Overall Stats ---
@stats_bp.route("/", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def get_overall_stats():
    """
    Returns total activities, total emissions, and average emission per activity.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        query = Activity.query
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()
        total_activities = len(activities)
        total_emission = sum(a.emission or 0 for a in activities)
        avg_emission = total_emission / total_activities if total_activities else 0

        return jsonify({
            "total_activities": total_activities,
            "total_emission": round(total_emission, 2),
            "average_emission": round(avg_emission, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Weekly Emissions ---
@stats_bp.route("/weekly-emissions", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def get_weekly_emissions():
    """
    Returns total CO₂ emissions for each day of the current week (Monday–Sunday).
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = date.today()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_days = [(week_start + timedelta(days=i)) for i in range(7)]
        weekly_data = {day.strftime("%A"): 0.0 for day in week_days}

        query = Activity.query.filter(Activity.date >= week_start)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()
        for activity in activities:
            # Ensure date is a date object
            activity_date = activity.date
            if isinstance(activity_date, datetime):
                activity_date = activity_date.date()
            day_name = activity_date.strftime("%A")
            if day_name in weekly_data:
                weekly_data[day_name] += float(activity.emission or 0.0)

        return jsonify(weekly_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Monthly Stats ---
@stats_bp.route("/monthly-stats", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def get_monthly_stats():
    """
    Returns total CO₂ emissions per day for the last 30 days.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = date.today()
        start_date = today - timedelta(days=30)

        query = Activity.query.filter(Activity.date >= start_date)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()
        result = {}
        for activity in activities:
            activity_date = activity.date
            if isinstance(activity_date, datetime):
                activity_date = activity_date.date()
            day_str = activity_date.strftime("%Y-%m-%d")
            result[day_str] = result.get(day_str, 0) + float(activity.emission or 0.0)

        # Sort results by date
        sorted_result = dict(sorted(result.items()))
        return jsonify(sorted_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
