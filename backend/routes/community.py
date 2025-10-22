from flask import Blueprint, jsonify, request
from models import db, Post, Comment

community_bp = Blueprint("community_bp", __name__, url_prefix="/api")

@community_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@community_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    post = Post(
        author=data.get("author", "Anonymous"),
        content=data.get("content", ""),
        category=data.get("category", "General")
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@community_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    data = request.get_json()
    comment = Comment(
        author=data.get("author", "Anonymous"),
        content=data.get("content", ""),
        post_id=post_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@community_bp.route("/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    post.likes += 1
    db.session.commit()
    return jsonify({"message": "Post liked!", "likes": post.likes}), 200

@community_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"}), 200
