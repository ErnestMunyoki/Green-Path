from datetime import date, datetime
from extensions import db


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="custom", nullable=False)
    emission = db.Column(db.Float, nullable=False)
    problem = db.Column(db.String(200))
    solution = db.Column(db.String(200))
    date = db.Column(db.Date, default=lambda: date.today(), nullable=False)

    def __repr__(self):
        return f"<Activity {self.name} ({self.category}) on {self.date}: {self.emission} kg CO₂>"


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    unlocked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Achievement {self.title}: {'Unlocked' if self.unlocked else 'Locked'}>"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous", nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General", nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship(
        "Comment", backref="post", cascade="all, delete-orphan", lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "category": self.category,
            "likes": self.likes,
            "created_at": self.created_at.isoformat(),
            "comments": [c.to_dict() for c in self.comments],
        }

    def __repr__(self):
        return f"<Post {self.id} by {self.author}>"

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous", nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Comment {self.id} by {self.author} on Post {self.post_id}>"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    activities = db.relationship("Activity", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
