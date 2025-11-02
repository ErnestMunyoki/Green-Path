from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models import Activity, db
from datetime import datetime

activities_bp = Blueprint("activities_bp", __name__, url_prefix="/api/activities")

@activities_bp.route("/estimate-emission", methods=["POST", "OPTIONS"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"])
def estimate_emission():
    if request.method == "OPTIONS":
        return '', 200

    data = request.get_json()
    description = data.get("description", "")
    emission = round(len(description) * 0.1, 2)  
    return jsonify({"emission": emission, "problem": "No problem generated.", "solution": "No solution provided."}), 200

@activities_bp.route("/", methods=["GET"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",              
    "http://127.0.0.1:5173"
])
def get_activities():
    activities = Activity.query.order_by(Activity.id.desc()).all()
    results = [a.to_dict() for a in activities]
    return jsonify(results), 200


@activities_bp.route("/latest", methods=["GET", "OPTIONS"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app", 
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def get_latest_activity():
    if request.method == "OPTIONS":
        return '', 200

    latest_activity = Activity.query.order_by(Activity.id.desc()).first()
    if latest_activity:
        return jsonify(latest_activity.to_dict()), 200
    else:
        return jsonify({"message": "No activities found"}), 404


@activities_bp.route("/log-activity", methods=["POST"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def log_activity():
    data = request.get_json()
    try:
        new_activity = Activity(
            name=data.get("name", ""),
            category=data.get("category", "Uncategorized"),
            emission=data.get("emission", 0),
            date=datetime.strptime(data.get("date"), "%Y-%m-%d") if data.get("date") else datetime.utcnow(),
            problem=data.get("problem", "No problem provided."),
            solution=data.get("solution", "No solution provided."),
            user_id=data.get("user_id")
        )
        db.session.add(new_activity)
        db.session.commit()
        return jsonify(new_activity.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@activities_bp.route("/<int:activity_id>", methods=["PATCH"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def edit_activity(activity_id):
    data = request.get_json()
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    try:
        for key in ["name", "category", "description", "emission", "problem", "solution", "date"]:
            if key in data:
                if key == "date" and data[key]:
                    setattr(activity, key, datetime.strptime(data[key], "%Y-%m-%d"))
                else:
                    setattr(activity, key, data[key])
        db.session.commit()
        return jsonify(activity.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@activities_bp.route("/<int:activity_id>", methods=["DELETE"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",              
    "http://127.0.0.1:5173"
])
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    try:
        db.session.delete(activity)
        db.session.commit()
        return jsonify({"message": "Activity deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@activities_bp.route("/clear", methods=["POST", "OPTIONS"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",             
    "http://127.0.0.1:5173"
])
def clear_all_activities():
    if request.method == "OPTIONS":
        return '', 200

    try:
        num_deleted = db.session.query(Activity).delete()
        db.session.commit()
        return jsonify({"success": True, "message": f"Cleared {num_deleted} activities"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
