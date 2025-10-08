# routes/favorite_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Favorite, Story, User

favorite_bp = Blueprint("favorite_bp", __name__)

# 🔹 GET: Favoriten eines Nutzers abrufen
@favorite_bp.route("/users/<user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": f.id,
            "story_id": f.story_id,
            "user_id": f.user_id
        } for f in favorites
    ]), 200


# 🔹 POST: Story favorisieren oder entfernen (toggle)
@favorite_bp.route("/stories/<story_id>/favorite", methods=["POST"])
def toggle_favorite(story_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(user_id)
    story = Story.query.get(story_id)
    if not user or not story:
        return jsonify({"error": "Invalid user_id or story_id"}), 404

    existing_fav = Favorite.query.filter_by(user_id=user_id, story_id=story_id).first()

    if existing_fav:
        db.session.delete(existing_fav)
        db.session.commit()
        return jsonify({"message": "Story removed from favorites"}), 200
    else:
        new_fav = Favorite(user_id=user_id, story_id=story_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Story added to favorites"}), 201
