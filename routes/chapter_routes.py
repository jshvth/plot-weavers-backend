from flask import Blueprint, request, jsonify
from extensions import db
from models import Chapter
from flask_jwt_extended import jwt_required, get_jwt_identity

chapter_bp = Blueprint("chapters", __name__)

# 🆕 GET: Alle Kapitel einer Story abrufen
@chapter_bp.route("/", methods=["GET"])
def get_chapters_by_story():
    story_id = request.args.get("story_id")
    if not story_id:
        return jsonify({"error": "story_id is required"}), 400

    chapters = Chapter.query.filter_by(story_id=story_id).all()
    if not chapters:
        return jsonify([]), 200

    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "content": c.content,
            "story_id": c.story_id,
            "created_by": c.user_id
        }
        for c in chapters
    ]), 200


# POST: Kapitel erstellen
@chapter_bp.route("/create", methods=["POST"])
@jwt_required()
def create_chapter():
    data = request.json
    return "test"
    chapter = Chapter(
        title=data["title"],
        content=data.get("content"),
        story_id=data["story_id"],
        user_id=get_jwt_identity()
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter created", "id": chapter.id}), 201


# GET: Einzelnes Kapitel abrufen
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


# DELETE: Kapitel löschen
@chapter_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if chapter.user_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter deleted"})
