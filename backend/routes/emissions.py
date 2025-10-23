from flask import Blueprint, jsonify
from models import Activity
from datetime import datetime, timedelta

emissions_bp = Blueprint("emissions", __name__)

@emissions_bp.route("/api/emissions/weekly", methods=["GET"])
def get_weekly_emissions():
    today = datetime.today().date()
    start = today - timedelta(days=6)

    result = {}
    for i in range(7):
        day = (start + timedelta(days=i)).strftime("%A")  
        result[day] = 0.0

    data = Activity.query.filter(Activity.date >= start).all()

    for activity in data:
        day = activity.date.strftime("%A")
        result[day] += activity.emission

    return jsonify(result)

