from flask import Blueprint, jsonify
from extensions import db
from models import User, Story, Chapter, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)

# 🔹 Eigene Stories abrufen
@user_bp.route("/me/stories", methods=["GET"])
@jwt_required()
def get_my_stories():
    user_id = get_jwt_identity()
    stories = Story.query.filter_by(created_by=user_id).all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "cover_image": s.cover_image,
            "genre": s.genre,
            "description": s.description,
        }
        for s in stories
    ]), 200


# 🔹 Eigene Kapitel abrufen
@user_bp.route("/me/chapters", methods=["GET"])
@jwt_required()
def get_my_chapters():
    user_id = get_jwt_identity()
    chapters = Chapter.query.filter_by(created_by=user_id).all()
    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "story_id": c.story_id,
            "created_at": c.created_at.isoformat() if c.created_at else None
        }
        for c in chapters
    ]), 200


# 🔹 Optional: Benutzerprofil löschen (bleibt gleich)
@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_me():
    user = User.query.get(get_jwt_identity())
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200
