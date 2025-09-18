from flask import Blueprint, request, jsonify
from extensions import db
from models import Chapter
from flask_jwt_extended import jwt_required, get_jwt_identity

chapter_bp = Blueprint("chapters", __name__)

@chapter_bp.route("/create", methods=["POST"])
@jwt_required()
def create_chapter():
    data = request.json
    chapter = Chapter(
        title=data["title"],
        content=data.get("content"),
        story_id=data["story_id"],
        user_id=get_jwt_identity()
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter created", "id": chapter.id}), 201


@chapter_bp.route("/<id>", methods=["GET"])
def get_chapter(id):
    c = Chapter.query.get_or_404(id)
    return jsonify({
        "id": c.id,
        "title": c.title,
        "content": c.content,
        "story_id": c.story_id,
        "created_by": c.creator.username
    })


@chapter_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if chapter.user_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter deleted"})
