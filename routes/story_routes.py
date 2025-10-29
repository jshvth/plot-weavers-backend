import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Story, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

story_bp = Blueprint("stories", __name__)

# ✅ Alle Stories abrufen (sicher & robust)
@story_bp.route("/all", methods=["GET"])
def all_stories():
    try:
        stories = Story.query.all()
        return jsonify([
            {
                "id": s.id,
                "title": s.title,
                "description": s.description,
                "genre": s.genre,
                "cover_image": s.cover_image,
                "created_by": s.creator.username if s.creator else "Unknown",
            }
            for s in stories
        ]), 200
    except Exception as e:
        print("❌ Fehler beim Laden der Stories:", e)
        return jsonify({"error": str(e)}), 500


# 🟢 Story erstellen (mit optionalem Cover-Bild)
@story_bp.route("/create", methods=["POST"])
@jwt_required()
def create_story():
    data = request.json
    story = Story(
        title=data["title"],
        description=data.get("description"),
        genre=data.get("genre"),
        cover_image=data.get("cover_image"),
        user_id=get_jwt_identity()
    )

    db.session.add(story)
    db.session.commit()

    return jsonify({
        "message": "Story created successfully",
        "story": {
            "id": story.id,
            "title": story.title,
            "description": story.description,
            "genre": story.genre,
            "cover_image": story.cover_image,
            "created_by": story.creator.username
        }
    }), 201


# 🟢 Einzelne Story abrufen
@story_bp.route("/<id>", methods=["GET"])
def get_story(id):
    s = Story.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "genre": s.genre,
        "cover_image": s.cover_image,
        "created_by": s.creator.username
    })


# 🟢 Story löschen
@story_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_story(id):
    story = Story.query.get_or_404(id)
    if story.user_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(story)
    db.session.commit()
    return jsonify({"message": "Story deleted"})


# 🟢 Upload-Route für Titelbilder
@story_bp.route("/upload/story-cover", methods=["POST"])
@jwt_required()
def upload_story_cover():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.root_path, "uploads", "stories")

    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 🔗 URL generieren (z. B. /uploads/stories/filename.jpg)
    file_url = f"/uploads/stories/{filename}"

    return jsonify({"message": "File uploaded", "url": file_url}), 201
