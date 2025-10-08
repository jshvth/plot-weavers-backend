# routes/favorite_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Favorite, db, Story

favorite_bp = Blueprint("favorite_bp", __name__)

@favorite_bp.route("/<string:story_id>", methods=["POST"])
@jwt_required()
def toggle_favorite(story_id):
    current_user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(user_id=current_user_id, story_id=story_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Removed from favorites"}), 200
    else:
        new_fav = Favorite(user_id=current_user_id, story_id=story_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Added to favorites"}), 201


@favorite_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    result = [{"story_id": f.story_id} for f in favorites]
    return jsonify(result), 200
