from flask import Blueprint, jsonify
from flask_cors import cross_origin
from models import db, Activity  # import your model(s)

clear_data_bp = Blueprint("clear_data", __name__, url_prefix="/api")

@clear_data_bp.route("/clear", methods=["DELETE", "OPTIONS"])  # ✅ both DELETE + OPTIONS
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def clear_data():
    if flask.request.method == "OPTIONS":
        # ✅ respond to preflight CORS
        return jsonify({"status": "OK"}), 200

    try:
        # ✅ Example: clear Activity table (add more models if needed)
        db.session.query(Activity).delete()
        db.session.commit()
        return jsonify({"message": "All activity data cleared successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
