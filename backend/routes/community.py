from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from models import db, Post, Comment, User

community_bp = Blueprint("community_bp", __name__)

@community_bp.route("/api/posts", methods=["GET", "POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def posts():
    if request.method == "OPTIONS":
        return "", 200

    if request.method == "GET":
        posts = Post.query.order_by(Post.date_created.desc()).all()
        return jsonify([p.to_dict() for p in posts]), 200

    if request.method == "POST":
        data = request.get_json()
        if not data or not data.get("content"):
            return jsonify({"error": "Content cannot be empty"}), 400

        user_id = data.get("user_id", 1)  
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        post = Post(
            content=data.get("content"),
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_dict()), 201

@community_bp.route("/api/posts/<int:post_id>/comments", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def add_comment(post_id):
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "Comment cannot be empty"}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    user_id = data.get("user_id", 1)  
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    comment = Comment(
        content=data.get("content"),
        post_id=post_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@community_bp.route("/api/posts/<int:post_id>/like", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def like_post(post_id):
    if request.method == "OPTIONS":
        return "", 200

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if not hasattr(post, "likes"):
        setattr(post, "likes", 0)

    post.likes += 1
    db.session.commit()
    return jsonify({"message": "Post liked!", "likes": post.likes}), 200

@community_bp.route("/api/posts/<int:post_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def delete_post(post_id):
    if request.method == "OPTIONS":
        return "", 200

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"}), 200

@community_bp.route("/api/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=[
    "https://green-path-m5yh.vercel.app",  
    "http://localhost:5173",               
    "http://127.0.0.1:5173"
])
def delete_comment(post_id, comment_id):
    if request.method == "OPTIONS":
        return "", 200

    comment = Comment.query.get(comment_id)
    if not comment or comment.post_id != post_id:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully!"}), 200
