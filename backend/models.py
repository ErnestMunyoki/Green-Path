from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    emission = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    unlocked = db.Column(db.Boolean, default=False)
