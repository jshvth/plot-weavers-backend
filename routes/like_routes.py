# routes/like_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Like, Chapter, User

like_bp = Blueprint("like_bp", __name__)

# 🔹 GET: Likes eines Kapitels abrufen
@like_bp.route("/chapters/<chapter_id>/likes", methods=["GET"])
def get_likes(chapter_id):
    likes = Like.query.filter_by(chapter_id=chapter_id).all()
    return jsonify({
        "chapter_id": chapter_id,
        "like_count": len(likes),
        "likes": [{"user_id": l.user_id} for l in likes]
    }), 200


# 🔹 POST: Kapitel liken oder like entfernen (toggle)
@like_bp.route("/chapters/<chapter_id>/like", methods=["POST"])
def toggle_like(chapter_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(user_id)
    chapter = Chapter.query.get(chapter_id)
    if not user or not chapter:
        return jsonify({"error": "Invalid user_id or chapter_id"}), 404

    existing_like = Like.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 200
    else:
        new_like = Like(user_id=user_id, chapter_id=chapter_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message": "Like added"}), 201
