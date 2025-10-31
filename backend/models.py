from datetime import datetime, date
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    activities = db.relationship(
        "Activity", back_populates="user", cascade="all, delete-orphan"
    )
    achievements = db.relationship(
        "Achievement", back_populates="user", cascade="all, delete-orphan"
    )
    posts = db.relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, default="Uncategorized")
    emission = db.Column(db.Float, nullable=True, default=0.0)
    problem = db.Column(db.Text, nullable=True, default="No problem provided.")
    solution = db.Column(db.Text, nullable=True, default="No solution provided.")
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.name}>"

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

class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    badge_icon = db.Column(db.String(200), nullable=True)
    date_awarded = db.Column(db.DateTime, nullable=True)

    threshold_type = db.Column(db.String(50), nullable=True)
    threshold_value = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", back_populates="achievements")

    def __repr__(self):
        return f"<Achievement {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "badge_icon": self.badge_icon,
            "date_awarded": self.date_awarded.isoformat() if self.date_awarded else None,
        }

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "date_created": self.date_created.isoformat(),
            "comments": [comment.to_dict() for comment in self.comments],
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    user = db.relationship("User")
    post = db.relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_created": self.date_created.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id,
        }
