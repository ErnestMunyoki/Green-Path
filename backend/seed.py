from app import app, db
from models import Activity, Achievement
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    sample_activities = [
        Activity(category="Commuting", emission=3.2, date=date(2025, 10, 10)),
        Activity(category="Meals", emission=4.1, date=date(2025, 10, 10)),
        Activity(category="Home", emission=4.1, date=date(2025, 10, 11)),
        Activity(category="Transport", emission=0.6, date=date(2025, 10, 11)),
        Activity(category="Shopping", emission=2.3, date=date(2025, 10, 12)),
    ]

    sample_achievements = [
        Achievement(title="First Step", unlocked=True),
        Achievement(title="Week Warrior", unlocked=True),
        Achievement(title="Carbon Cutter", unlocked=True),
        Achievement(title="Public Transport Hero", unlocked=False),
        Achievement(title="Plant Based", unlocked=False),
        Achievement(title="Community Champion", unlocked=False),
    ]

    db.session.bulk_save_objects(sample_activities + sample_achievements)
    db.session.commit()

    print("✅ Seeded database with sample activities and achievements.")
