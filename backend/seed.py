from app import create_app
from models import db, Activity, Achievement, User
from datetime import date
import os

# ✅ Create app context
app = create_app()

with app.app_context():
    # Print database being used
    print(f"📘 Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # ✅ Reset database
    db.drop_all()
    db.create_all()

    # ✅ Create sample user
    sample_user = User(
        username="testuser",
        email="test@example.com"
    )
    db.session.add(sample_user)
    db.session.commit()

    # ✅ Create sample activities
    sample_activities = [
        Activity(name="Commute to work", category="Commuting", emission=3.2, date=date(2025, 10, 10), user_id=sample_user.id),
        Activity(name="Lunch", category="Meals", emission=4.1, date=date(2025, 10, 10), user_id=sample_user.id),
        Activity(name="Home electricity", category="Home", emission=4.1, date=date(2025, 10, 11), user_id=sample_user.id),
        Activity(name="Bus ride", category="Transport", emission=0.6, date=date(2025, 10, 11), user_id=sample_user.id),
        Activity(name="Grocery shopping", category="Shopping", emission=2.3, date=date(2025, 10, 12), user_id=sample_user.id),
    ]

    # ✅ Create sample achievements (simplified for your model)
    sample_achievements = [
        Achievement(title="First Step", description="Logged your first activity", user_id=sample_user.id),
        Achievement(title="Week Warrior", description="Logged activities for 7 days", user_id=sample_user.id),
        Achievement(title="Carbon Cutter", description="Saved 50kg of CO₂", user_id=sample_user.id),
        Achievement(title="Public Transport Hero", description="Used public transport 5 times", user_id=sample_user.id),
        Achievement(title="Plant Based", description="Logged 3 plant-based meals", user_id=sample_user.id),
        Achievement(title="Community Champion", description="Joined the community challenge", user_id=sample_user.id),
    ]

    # ✅ Commit to database
    db.session.bulk_save_objects(sample_activities + sample_achievements)
    db.session.commit()

    print("✅ Seeded database with sample user, activities, and achievements.")
