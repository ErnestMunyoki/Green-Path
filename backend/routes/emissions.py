from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta

emissions_bp = Blueprint("emissions", __name__)

# Weekly stats
@emissions_bp.route("/weekly", methods=["GET"])
def get_weekly_emissions():
    today = datetime.utcnow().date()
    start = today - timedelta(days=6)

    result = { (start + timedelta(days=i)).strftime("%A"): 0.0 for i in range(7) }

    data = Activity.query.filter(Activity.date >= start).all()
    for activity in data:
        day = activity.date.strftime("%A")
        result[day] += activity.emission

    return jsonify(result)

# Monthly stats
@emissions_bp.route("/monthly", methods=["GET"])
def get_monthly_emissions():
    today = datetime.utcnow().date()
    start = today.replace(day=1)

    result = {str(i+1): 0.0 for i in range(today.day)}  # Day of month: emission

    data = Activity.query.filter(Activity.date >= start).all()
    for activity in data:
        day = str(activity.date.day)
        result[day] += activity.emission

    return jsonify(result)
