# routes/predictions.py
from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import random

predictions_bp = Blueprint("predictions_bp", __name__, url_prefix="/api/predictions")

# Mock user activity data
user_activities = [
    {"date": "2025-10-21", "emission": 12.5},
    {"date": "2025-10-22", "emission": 13.2},
    {"date": "2025-10-23", "emission": 11.8},
    {"date": "2025-10-24", "emission": 12.0},
    {"date": "2025-10-25", "emission": 13.5},
    {"date": "2025-10-26", "emission": 12.9},
    {"date": "2025-10-27", "emission": 13.1},
]

def generate_predictions(days=7):
    total = sum(a["emission"] for a in user_activities)
    avg = total / len(user_activities)
    predictions = []
    for i in range(days):
        date = (datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d")
        emission = round(avg * random.uniform(0.95, 1.05), 1)
        predictions.append({"date": date, "emission": emission})
    return predictions

@predictions_bp.route("/", methods=["GET"])
def get_predictions():
    data = generate_predictions(7)
    return jsonify(data)
