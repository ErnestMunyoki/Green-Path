import logging
from flask import Blueprint, jsonify

# Create and configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

prediction_bp = Blueprint("prediction_bp", __name__)

# Sample data that your API returns
sample_predictions = [
    {
        "activity": "Boiled water with charcoal",
        "emission": 0.3,
        "problem": "High carbon emissions from charcoal use.",
        "recommendation": "Use electric kettle with renewable energy.",
        "solution": "Electric kettles reduce emissions by 80%.",
        "date": "2025-10-24"
    },
    {
        "activity": "Car commute",
        "emission": 5.1,
        "problem": "Gasoline car emits high CO2.",
        "recommendation": "Switch to e-bike or public transit.",
        "solution": "Biking or transit reduces emissions significantly.",
        "date": "2025-10-23"
    },
    {
        "activity": "Air travel",
        "emission": 50,
        "problem": "Flights contribute large carbon footprint.",
        "recommendation": "Use virtual meetings when possible.",
        "solution": "Virtual meetings reduce travel emissions effectively.",
        "date": "2025-10-20"
    }
]

@prediction_bp.route("/predictions", methods=["GET"])
def get_predictions():
    try:
        logger.debug("Predictions endpoint called")
        logger.debug(f"Returning {len(sample_predictions)} predictions")
        return jsonify(sample_predictions)
    except Exception as e:
        logger.error("Error in /predictions endpoint", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500
