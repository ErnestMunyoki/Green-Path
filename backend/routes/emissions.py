from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta
from sqlalchemy import cast, Date
import calendar

emissions_bp = Blueprint("emissions", __name__)

# ------------------------
# Weekly emissions
# ------------------------
@emissions_bp.route("/weekly", methods=["GET"])
def get_weekly_emissions():
    today = datetime.utcnow().date()
    start = today - timedelta(days=6)  # Last 7 days including today

    # Initialize dictionary with day names
    week_days = [(start + timedelta(days=i)) for i in range(7)]
    result = {day.strftime("%A"): 0.0 for day in week_days}

    # Query activities in the last 7 days (compare only dates)
    activities = Activity.query.filter(cast(Activity.date, Date) >= start).all()

    for activity in activities:
        activity_date = activity.date
        if isinstance(activity_date, datetime):
            activity_date = activity_date.date()
        day_name = activity_date.strftime("%A")
        result[day_name] += float(activity.emission or 0.0)

    return jsonify(result)

# ------------------------
# Monthly emissions
# ------------------------
@emissions_bp.route("/monthly", methods=["GET"])
def get_monthly_emissions():
    today = datetime.utcnow().date()
    start = today.replace(day=1)  # First day of the current month

    # Get total days in month
    days_in_month = calendar.monthrange(today.year, today.month)[1]

    # Initialize dictionary for each day
    result = {str(i + 1): 0.0 for i in range(days_in_month)}

    # Query activities since start of month (compare only dates)
    activities = Activity.query.filter(cast(Activity.date, Date) >= start).all()

    for activity in activities:
        activity_date = activity.date
        if isinstance(activity_date, datetime):
            activity_date = activity_date.date()
        day_str = str(activity_date.day)
        result[day_str] += float(activity.emission or 0.0)

    # Sort dictionary by day number
    sorted_result = dict(sorted(result.items(), key=lambda x: int(x[0])))

    return jsonify(sorted_result)
