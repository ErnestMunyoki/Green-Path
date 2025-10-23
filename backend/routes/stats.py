from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/api/stats", methods=["GET"])
def get_monthly_stats():
    today = datetime.today()
    start = today - timedelta(days=30)  # last 30 days
    activities = Activity.query.filter(Activity.date >= start).all()

    result = {}
    for activity in activities:
        day = activity.date.strftime("%Y-%m-%d")
        result[day] = result.get(day, 0) + activity.emission

    return jsonify(result)
