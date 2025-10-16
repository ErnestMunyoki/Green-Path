from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta

emissions_bp = Blueprint("emissions", __name__)

@emissions_bp.route("/api/emissions/weekly", methods=["GET"])
def get_weekly_emissions():
    today = datetime.today().date()
    start = today - timedelta(days=6)
    data = Activity.query.filter(Activity.date >= start).all()

    result = {}
    for activity in data:
        day = activity.date.strftime("%a")
        result[day] = result.get(day, 0) + activity.emission

    return jsonify(result)
