from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models import Activity
from datetime import datetime, timedelta
from sqlalchemy import cast, Date
import calendar

emissions_bp = Blueprint("emissions_bp", __name__, url_prefix="/api/emissions")

def parse_activity_date(activity_date):
    """
    Safely convert activity.date to a datetime.date.
    Handles datetime objects, date objects, and string dates (YYYY-MM-DD).
    """
    if isinstance(activity_date, datetime):
        return activity_date.date()
    elif isinstance(activity_date, str):
        try:
            return datetime.strptime(activity_date, "%Y-%m-%d").date()
        except ValueError:
            return None
    return activity_date 


@emissions_bp.route("/weekly", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",             
    "http://127.0.0.1:5173"
])
def get_weekly_emissions():
    """
    Returns total CO₂ emissions for each day of the current week (Monday–Sunday).
    Includes future dates in the week.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = datetime.now().date()  
        start_of_week = today - timedelta(days=today.weekday())  
        end_of_week = start_of_week + timedelta(days=6) 

        week_days = [(start_of_week + timedelta(days=i)) for i in range(7)]
        result = {day.strftime("%A"): 0.0 for day in week_days}

        query = Activity.query.filter(
            cast(Activity.date, Date) >= start_of_week,
            cast(Activity.date, Date) <= end_of_week
        )
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()

        for activity in activities:
            activity_date = parse_activity_date(activity.date)
            if not activity_date:
                continue
            day_name = activity_date.strftime("%A")
            if day_name in result:
                result[day_name] += float(activity.emission or 0.0)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@emissions_bp.route("/monthly", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def get_monthly_emissions():
    """
    Returns total CO₂ emissions for each day of the current month.
    Includes future dates in the month.
    """
    try:
        user_id = request.args.get("user_id", type=int)
        today = datetime.now().date()  
        start_of_month = today.replace(day=1)
        days_in_month = calendar.monthrange(today.year, today.month)[1]

        result = {str(day): 0.0 for day in range(1, days_in_month + 1)}

        query = Activity.query.filter(
            cast(Activity.date, Date) >= start_of_month
        )
        if user_id:
            query = query.filter(Activity.user_id == user_id)

        activities = query.all()

        for activity in activities:
            activity_date = parse_activity_date(activity.date)
            if not activity_date:
                continue
            day_str = str(activity_date.day)
            if day_str in result:
                result[day_str] += float(activity.emission or 0.0)

        sorted_result = dict(sorted(result.items(), key=lambda x: int(x[0])))

        return jsonify(sorted_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
