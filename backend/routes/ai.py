import openai
import os
from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai", __name__, url_prefix="/api")

@ai_bp.route("/estimate-emission", methods=["POST"])
def estimate_emission():
    try:
        data = request.get_json()
        description = data.get("description")

        if not description:
            return jsonify({"error": "Missing activity description"}), 400

        description = description.lower()
        emission = 0.0

        if "car" in description and "10km" in description:
            emission = 2.3
        elif "bus" in description and "15km" in description:
            emission = 1.1
        elif "train" in description and "20km" in description:
            emission = 0.8
        elif "walk" in description or "bike" in description:
            emission = 0.0
        elif "flight" in description:
            emission = 90.0
        else:
            emission = 5.0  

        return jsonify({"emission": emission}), 200

    except Exception as e:
        print("AI error:", e)
        return jsonify({"error": "Internal server error"}), 500

