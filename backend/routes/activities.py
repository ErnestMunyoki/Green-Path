from flask import Blueprint, request, jsonify
from models import db, Activity
from datetime import datetime, timedelta

activities_bp = Blueprint("activities", __name__, url_prefix="/api")

@activities_bp.route("/activities", methods=["POST"])
def log_activity():
    try:
        data = request.get_json()
        category = data.get("category")
        emission = data.get("emission")
        date_str = data.get("date")

        if not category or emission is None or not date_str:
            return jsonify({"error": "Missing required fields"}), 400

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        activity = Activity(category=category, emission=emission, date=date_obj)
        db.session.add(activity)
        db.session.commit()

        return jsonify({"message": "Activity logged successfully"}), 200

    except Exception as e:
        print("Error logging activity:", e)
        return jsonify({"error": "Internal server error"}), 500

@activities_bp.route("/activities", methods=["GET"])
def get_activities():
    try:
        activities = Activity.query.order_by(Activity.date.desc()).all()
        return jsonify([
            {
                "id": a.id,
                "category": a.category,
                "emission": a.emission,
                "date": a.date.strftime("%Y-%m-%d")
            }
            for a in activities
        ]), 200
    except Exception as e:
        print("Error fetching activities:", e)
        return jsonify({"error": "Failed to fetch activities"}), 500

@activities_bp.route("/activities/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    try:
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        db.session.delete(activity)
        db.session.commit()
        return jsonify({"message": "Activity deleted"}), 200

    except Exception as e:
        print("Error deleting activity:", e)
        return jsonify({"error": "Internal server error"}), 500

@activities_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        today = datetime.today().date()
        start_week = today - timedelta(days=today.weekday())
        start_month = today.replace(day=1)

        week_activities = Activity.query.filter(Activity.date >= start_week).all()
        month_activities = Activity.query.filter(Activity.date >= start_month).all()

        week_emissions = sum(a.emission for a in week_activities)
        month_emissions = sum(a.emission for a in month_activities)
        unique_days = len(set(a.date for a in month_activities))
        daily_average = month_emissions / max(unique_days, 1)
        activity_count = len(month_activities)

        return jsonify({
            "week_emissions": round(week_emissions, 2),
            "month_emissions": round(month_emissions, 2),
            "daily_average": round(daily_average, 2),
            "activity_count": activity_count
        }), 200

    except Exception as e:
        print("Error calculating stats:", e)
        return jsonify({"error": "Failed to calculate stats"}), 500

@activities_bp.route("/clear", methods=["POST"])
def clear_all_data():
    try:
        num_deleted = Activity.query.delete()
        db.session.commit()
        return jsonify({"message": f"Cleared {num_deleted} activities."}), 200
    except Exception as e:
        print("Error clearing data:", e)
        return jsonify({"error": "Failed to clear data"}), 500

@activities_bp.route("/activities/by-date", methods=["POST"])
def get_activities_by_date():
    try:
        data = request.get_json()
        date_str = data.get("date")
        if not date_str:
            return jsonify({"error": "Missing date"}), 400

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        activities = Activity.query.filter(Activity.date == date_obj).all()

        return jsonify([
            {
                "category": a.category,
                "emission": a.emission
            }
            for a in activities
        ]), 200
    except Exception as e:
        print("Error fetching activities by date:", e)
        return jsonify({"error": "Failed to fetch activities"}), 500






