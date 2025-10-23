from flask import Blueprint, request, jsonify, abort
from services.ecotrack_ai_service import EcotrackAIService

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/insights", methods=["POST"])
def ai_insights():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    emissions_data = request.json.get("emissions")
    if not emissions_data:
        abort(400, description="No emissions data provided")

    advice, error = EcotrackAIService.get_insights(emissions_data)
    if error:
        abort(500, description=error)

    return jsonify({"insights": advice})

@ai_bp.route("/predictions/next_7_days", methods=["POST"])
def ai_predictions():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    emissions_data = request.json.get("emissions")
    if not emissions_data:
        abort(400, description="No emissions data provided")

    predictions = EcotrackAIService.predict_next_7_days(emissions_data)
    if "error" in predictions:
        abort(500, description=predictions["error"])

    return jsonify(predictions)

@ai_bp.errorhandler(400)
@ai_bp.errorhandler(404)
@ai_bp.errorhandler(500)
def handle_api_errors(error):
    response = jsonify({
        "error": error.name,
        "message": error.description or str(error),
        "status": error.code if hasattr(error, "code") else 500
    })
    response.status_code = error.code if hasattr(error, "code") else 500
    return response
