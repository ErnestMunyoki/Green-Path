from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

activities_bp = Blueprint("activities_bp", __name__)

@activities_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def estimate_emission():
    if request.method == "OPTIONS":
        # Preflight request
        return '', 200

    data = request.get_json()
    description = data.get("description", "")

    # Placeholder emission calculation (replace with real logic later)
    emission = len(description) * 0.1
    return jsonify({"emission": emission}), 200
