# routes/favorites_routes.py
from flask import Blueprint, jsonify, request
from extensions import db
from models import Favorite, Story, User
from flask_jwt_extended import jwt_required, get_jwt_identity

favorite_bp = Blueprint("favorites", __name__)

# 🔹 Favoriten des eingeloggten Nutzers abrufen
@favorite_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_favorites():
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()

    data = []
    for fav in favorites:
        story = Story.query.get(fav.story_id)
        if story:
            data.append({
                "id": story.id,
                "title": story.title,
                "cover_image": story.cover_image,
                "genre": story.genre,
                "description": story.description
            })
    return jsonify(data), 200


# 🔹 Story favorisieren oder entfernen (toggle)
@favorite_bp.route("/toggle/<story_id>", methods=["POST"])
@jwt_required()
def toggle_favorite(story_id):
    user_id = get_jwt_identity()

    story = Story.query.get(story_id)
    if not story:
        return jsonify({"error": "Invalid story_id"}), 404

    existing = Favorite.query.filter_by(user_id=user_id, story_id=story_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"message": "Removed from favorites"}), 200
    else:
        fav = Favorite(user_id=user_id, story_id=story_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({"message": "Added to favorites"}), 201
