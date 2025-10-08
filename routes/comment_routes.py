# routes/comment_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Comment, Story, User
from datetime import datetime

comment_bp = Blueprint("comment_bp", __name__)

# 🔹 GET: Alle Kommentare zu einer Story
@comment_bp.route("/stories/<story_id>/comments", methods=["GET"])
def get_comments(story_id):
    comments = Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.desc()).all()
    return jsonify([
        {
            "id": c.id,
            "story_id": c.story_id,
            "user_id": c.user_id,
            "username": c.username,
            "content": c.content,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ]), 200


# 🔹 POST: Kommentar hinzufügen
@comment_bp.route("/stories/<story_id>/comments", methods=["POST"])
def add_comment(story_id):
    data = request.get_json()
    user_id = data.get("user_id")
    content = data.get("content")

    if not user_id or not content:
        return jsonify({"error": "user_id and content are required"}), 400

    # Nutzer und Story prüfen
    user = User.query.get(user_id)
    story = Story.query.get(story_id)
    if not user or not story:
        return jsonify({"error": "Invalid user_id or story_id"}), 404

    new_comment = Comment(
        story_id=story_id,
        user_id=user_id,
        username=user.username,
        content=content,
        created_at=datetime.utcnow()
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "message": "Comment added successfully",
        "comment": {
            "id": new_comment.id,
            "story_id": new_comment.story_id,
            "user_id": new_comment.user_id,
            "username": new_comment.username,
            "content": new_comment.content,
            "created_at": new_comment.created_at.isoformat()
        }
    }), 201


# 🔹 DELETE: Kommentar löschen
@comment_bp.route("/comments/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200
