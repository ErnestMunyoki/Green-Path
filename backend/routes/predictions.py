# predictions.py
from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock user activity data
# Each activity could have an emission value in kg CO2
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
    """Generate predicted emissions for the next `days` days"""
    # Calculate average emission from past activities
    total = sum(a["emission"] for a in user_activities)
    avg = total / len(user_activities)

    predictions = []
    for i in range(days):
        date = (datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d")
        # Add some random variation to simulate prediction
        emission = round(avg * random.uniform(0.95, 1.05), 1)
        predictions.append({"date": date, "emission": emission})

    return predictions

@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    data = generate_predictions(7)  # 7-day forecast
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
