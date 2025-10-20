from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)      
    emission = db.Column(db.Float, nullable=False)            
    date = db.Column(db.Date, default=date.today)             

    def __repr__(self):
        return f"<Activity {self.category} on {self.date}: {self.emission} kg CO₂>"

class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)         
    unlocked = db.Column(db.Boolean, default=False)           

    def __repr__(self):
        return f"<Achievement {self.title}: {'Unlocked' if self.unlocked else 'Locked'}>"

