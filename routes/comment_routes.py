# routes/comment_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Comment, db
from datetime import datetime

comment_bp = Blueprint("comment_bp", __name__)

@comment_bp.route("/<string:story_id>", methods=["GET"])
def get_comments(story_id):
    comments = Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.desc()).all()
    return jsonify([
        {
            "id": c.id,
            "user_id": c.user_id,
            "username": c.username,
            "content": c.content,
            "created_at": c.created_at.isoformat()
        } for c in comments
    ]), 200


@comment_bp.route("/<string:story_id>", methods=["POST"])
@jwt_required()
def add_comment(story_id):
    data = request.get_json()
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    current_user_id = get_jwt_identity()
    username = data.get("username")  # Wird aus dem Frontend mitgeschickt

    comment = Comment(
        story_id=story_id,
        user_id=current_user_id,
        username=username,
        content=content,
        created_at=datetime.utcnow()
    )

    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added"}), 201


@comment_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    current_user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    if comment.user_id != current_user_id:
        return jsonify({"error": "Not authorized"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200
