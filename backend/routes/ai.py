import openai
import os
from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai", __name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@ai_bp.route("/api/ai/insights", methods=["POST"])
def generate_insights():
    data = request.get_json()
    emissions = data.get("emissions", [])

    emission_summary = ", ".join([f"{d['day']}: {d['emission']}kg" for d in emissions])
    prompt = (
        f"Here is a user's weekly CO₂ emission data: {emission_summary}. "
        "Give 3 personalized suggestions to reduce emissions based on this pattern."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        message = response.choices[0].message.content
        return jsonify({"insights": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

