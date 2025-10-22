from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous")  # ✅ new
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General")    # ✅ can be 'Question', 'Tip', etc.
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
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), default="Anonymous")   # ✅ new
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.strftime("%b %d, %Y %H:%M"),
        }
