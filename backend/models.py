from datetime import date, datetime
from extensions import db  


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

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous")
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General")  # e.g. 'Question', 'Tip'
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "category": self.category,
            "likes": self.likes,
            "created_at": self.created_at.strftime("%b %d, %Y %H:%M"),
            "comments": [c.to_dict() for c in self.comments],
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous")
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.strftime("%b %d, %Y %H:%M"),
        }
