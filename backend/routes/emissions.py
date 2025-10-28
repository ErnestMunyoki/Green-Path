from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models import Activity
from datetime import datetime, timedelta
from sqlalchemy import cast, Date
import calendar

emissions_bp = Blueprint("emissions_bp", __name__, url_prefix="/api/emissions")

# --- Weekly Emissions ---
@emissions_bp.route("/weekly", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_weekly_emissions():
    """
    Returns total CO₂ emissions for each day of the current week (Monday–Sunday).
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = datetime.utcnow().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        week_days = [(start_of_week + timedelta(days=i)) for i in range(7)]
        result = {day.strftime("%A"): 0.0 for day in week_days}

        query = Activity.query.filter(cast(Activity.date, Date) >= start_of_week)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()
        for activity in activities:
            activity_date = activity.date.date() if isinstance(activity.date, datetime) else activity.date
            day_name = activity_date.strftime("%A")
            if day_name in result:
                result[day_name] += float(activity.emission or 0.0)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Monthly Emissions ---
@emissions_bp.route("/monthly", methods=["GET"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_monthly_emissions():
    """
    Returns total CO₂ emissions for each day of the current month.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = datetime.utcnow().date()
        start_of_month = today.replace(day=1)
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        result = {str(i + 1): 0.0 for i in range(days_in_month)}

        query = Activity.query.filter(cast(Activity.date, Date) >= start_of_month)
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()
        for activity in activities:
            activity_date = activity.date.date() if isinstance(activity.date, datetime) else activity.date
            day_str = str(activity_date.day)
            if day_str in result:
                result[day_str] += float(activity.emission or 0.0)

        # Sort results by day number
        sorted_result = dict(sorted(result.items(), key=lambda x: int(x[0])))
        return jsonify(sorted_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
