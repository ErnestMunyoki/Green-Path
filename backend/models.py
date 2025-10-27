from datetime import date, datetime
from extensions import db


# -------------------------
# ACTIVITY MODEL
# -------------------------
class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="custom", nullable=False)
    emission = db.Column(db.Float, nullable=False)
    problem = db.Column(db.String(200))
    solution = db.Column(db.String(200))
    date = db.Column(db.Date, default=date.today, nullable=False)

    def __repr__(self):
        return f"<Activity {self.name} ({self.category}) on {self.date}: {self.emission} kg CO₂>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category,
            "emission": self.emission,
            "problem": self.problem,
            "solution": self.solution,
            "date": self.date.isoformat(),
        }


# -------------------------
# ACHIEVEMENT MODEL
# -------------------------
class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    unlocked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Achievement {self.title}: {'Unlocked' if self.unlocked else 'Locked'}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "unlocked": self.unlocked,
        }


# -------------------------
# POST MODEL
# -------------------------
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous", nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General", nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship(
        "Comment",
        backref="post",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Post {self.id} by {self.author}>"

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "category": self.category,
            "likes": self.likes,
            "created_at": self.created_at.isoformat(),
            "comments": [comment.to_dict() for comment in self.comments],
        }


# -------------------------
# COMMENT MODEL
# -------------------------
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous", nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.id} by {self.author} on Post {self.post_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


# -------------------------
# USER MODEL
# -------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    activities = db.relationship(
        "Activity",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }
