from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta
from sqlalchemy import cast, Date
import calendar

emissions_bp = Blueprint("emissions", __name__)

@emissions_bp.route("/weekly", methods=["GET"])
def get_weekly_emissions():
    today = datetime.utcnow().date()
    start = today - timedelta(days=6)
    week_days = [(start + timedelta(days=i)) for i in range(7)]
    result = {day.strftime("%A"): 0.0 for day in week_days}

    activities = Activity.query.filter(cast(Activity.date, Date) >= start).all()
    for activity in activities:
        activity_date = activity.date.date() if isinstance(activity.date, datetime) else activity.date
        day_name = activity_date.strftime("%A")
        result[day_name] += float(activity.emission or 0.0)

    return jsonify(result)

@emissions_bp.route("/monthly", methods=["GET"])
def get_monthly_emissions():
    today = datetime.utcnow().date()
    start = today.replace(day=1)
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    result = {str(i + 1): 0.0 for i in range(days_in_month)}

    activities = Activity.query.filter(cast(Activity.date, Date) >= start).all()
    for activity in activities:
        activity_date = activity.date.date() if isinstance(activity.date, datetime) else activity.date
        day_str = str(activity_date.day)
        result[day_str] += float(activity.emission or 0.0)

    return jsonify(dict(sorted(result.items(), key=lambda x: int(x[0]))))
