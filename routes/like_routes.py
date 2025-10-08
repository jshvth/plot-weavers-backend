# routes/like_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Like, db, Story

like_bp = Blueprint("like_bp", __name__)

@like_bp.route("/<string:story_id>", methods=["POST"])
@jwt_required()
def toggle_like(story_id):
    current_user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=current_user_id, story_id=story_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 200
    else:
        new_like = Like(user_id=current_user_id, story_id=story_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message": "Story liked"}), 201


@like_bp.route("/count/<string:story_id>", methods=["GET"])
def count_likes(story_id):
    count = Like.query.filter_by(story_id=story_id).count()
    return jsonify({"likes": count}), 200


@like_bp.route("/check/<string:story_id>", methods=["GET"])
@jwt_required()
def check_like(story_id):
    current_user_id = get_jwt_identity()
    liked = Like.query.filter_by(user_id=current_user_id, story_id=story_id).first() is not None
    return jsonify({"liked": liked}), 200
