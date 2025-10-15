from flask import Blueprint, request, jsonify
from extensions import db
from models import Story, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

story_bp = Blueprint("stories", __name__)

@story_bp.route("/all", methods=["GET"])
def all_stories():
    stories = Story.query.all()
    return jsonify([{
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "genre": s.genre,
        "image": s.image,
        "created_by": s.creator.username
    } for s in stories])


@story_bp.route("/create", methods=["POST"])
@jwt_required()
def create_story():
    data = request.json

    # ✅ Neue Story anlegen
    story = Story(
        title=data["title"],
        description=data.get("description"),
        genre=data.get("genre"),
        image=data.get("image"),
        user_id=get_jwt_identity()
    )

    db.session.add(story)
    db.session.commit()

    # ✅ Vollständiges Story-Objekt zurückgeben
    return jsonify({
        "message": "Story created successfully",
        "story": {
            "id": story.id,
            "title": story.title,
            "description": story.description,
            "genre": story.genre,
            "image": story.image,
            "created_by": story.creator.username
        }
    }), 201



@story_bp.route("/<id>", methods=["GET"])
def get_story(id):
    s = Story.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "genre": s.genre,
        "image": s.image,
        "created_by": s.creator.username
    })


@story_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_story(id):
    story = Story.query.get_or_404(id)
    if story.user_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(story)
    db.session.commit()
    return jsonify({"message": "Story deleted"})
