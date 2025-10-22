from flask import request, jsonify
from app import app, db
from models import Post, Comment

@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "author": p.author,  
            "content": p.content,
            "category": p.category,
            "likes": p.likes,
            "created_at": p.created_at.strftime("%b %d, %Y %H:%M"),
            "comments": [
                {
                    "id": c.id,
                    "author": c.author,  
                    "content": c.content,
                    "created_at": c.created_at.strftime("%b %d, %Y %H:%M"),
                }
                for c in p.comments
            ],
        }
        for p in posts
    ]), 200

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "Content is required"}), 400

    post = Post(
        author=data.get("author", "Anonymous"),  
        content=data["content"],
        category=data.get("category", "General")   
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

@app.route("/api/posts/<int:id>/like", methods=["POST"])
def like_post(id):
    post = Post.query.get_or_404(id)
    post.likes += 1
    db.session.commit()
    return jsonify({"likes": post.likes}), 200


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200

@app.route("/api/posts/<int:id>/comments", methods=["POST", "OPTIONS"])
def add_comment(id):
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "Comment content is required"}), 400

    comment = Comment(post_id=id, content=data["content"])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added", "comment_id": comment.id}), 201


@app.route("/api/comments/<int:id>", methods=["DELETE"])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200
