from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Story, Chapter, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("users", __name__)

@user_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_me():
    user = User.query.get(get_jwt_identity())
    data = request.json
    if "username" in data:
        user.username = data["username"]
    if "profile_image" in data:
        user.profile_image = data["profile_image"]
    db.session.commit()
    return jsonify({"message": "Profile updated"})


@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_me():
    user = User.query.get(get_jwt_identity())
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"})


@user_bp.route("/me/stories", methods=["GET"])
@jwt_required()
def my_stories():
    user = User.query.get(get_jwt_identity())
    return jsonify([{"id": s.id, "title": s.title} for s in user.stories])


@user_bp.route("/me/chapters", methods=["GET"])
@jwt_required()
def my_chapters():
    user = User.query.get(get_jwt_identity())
    return jsonify([{"id": c.id, "title": c.title} for c in user.chapters])
