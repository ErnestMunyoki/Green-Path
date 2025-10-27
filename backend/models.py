from datetime import datetime
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
    category = db.Column(db.String(100), nullable=False, default="Uncategorized")  # ✅ Added category
    emission = db.Column(db.Float, nullable=True, default=0.0)
    problem = db.Column(db.Text, nullable=True, default="No problem provided.")  # ✅ AI problem
    solution = db.Column(db.Text, nullable=True, default="No solution provided.")  # ✅ AI solution
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.name}>"


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    badge_icon = db.Column(db.String(200), nullable=True)
    date_awarded = db.Column(db.DateTime, nullable=True)  # Only set when unlocked

    # Dynamic unlocking
    threshold_type = db.Column(db.String(50), nullable=True)  # "activity_count" or "emission_total"
    threshold_value = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", back_populates="achievements")

    def __repr__(self):
        return f"<Achievement {self.title}>"


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
