import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Story, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

story_bp = Blueprint("stories", __name__)

# ============================================================
# 🟢 Alle Stories abrufen
# ============================================================
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
                # 🔗 Stelle sicher, dass URL absolut ist
                "cover_image": (
                    s.cover_image if s.cover_image.startswith("http")
                    else f"https://plot-weavers-backend.onrender.com{s.cover_image}"
                    if s.cover_image else None
                ),
                "created_by": s.creator.username if s.creator else "Unknown",
            }
            for s in stories
        ]), 200
    except Exception as e:
        print("❌ Fehler beim Laden der Stories:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# 🟢 Story erstellen
# ============================================================
@story_bp.route("/create", methods=["POST"])
@jwt_required()
def create_story():
    data = request.json
    user_id = get_jwt_identity()

    story = Story(
        title=data["title"],
        description=data.get("description"),
        genre=data.get("genre"),
        cover_image=data.get("cover_image"),
        user_id=user_id
    )

    db.session.add(story)
    db.session.commit()

    # Creator-Objekt manuell abrufen (sonst bleibt es None)
    from models import User
    creator = User.query.get(user_id)

    return jsonify({
        "message": "Story created successfully",
        "story": {
            "id": story.id,
            "title": story.title,
            "description": story.description,
            "genre": story.genre,
            "cover_image": (
                story.cover_image if story.cover_image.startswith("http")
                else f"https://plot-weavers-backend.onrender.com{story.cover_image}"
                if story.cover_image else None
            ),
            "created_by": creator.username if creator else "Unknown"
        }
    }), 201


# ============================================================
# 🟢 Einzelne Story abrufen
# ============================================================
@story_bp.route("/<id>", methods=["GET"])
def get_story(id):
    s = Story.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "title": s.title,
        "description": s.description,
        "genre": s.genre,
        "cover_image": (
            s.cover_image if s.cover_image.startswith("http")
            else f"https://plot-weavers-backend.onrender.com{s.cover_image}"
            if s.cover_image else None
        ),
        "created_by": s.creator.username if s.creator else "Unknown",
        "author": s.creator.username if s.creator else "Unknown"
    })


# ============================================================
# 🟢 Story löschen (Admin darf alles)
# ============================================================
@story_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_story(id):
    story = Story.query.get_or_404(id)
    current_user_id = get_jwt_identity()

    # 🔹 Hole den aktuellen User aus der Datenbank
    from models import User
    user = User.query.get(current_user_id)

    # 🟡 Admin darf alles löschen
    if user and user.username == "admin":
        db.session.delete(story)
        db.session.commit()
        return jsonify({"message": "Story deleted by admin"})

    # 🟢 Normale Berechtigungsprüfung
    if story.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(story)
    db.session.commit()
    return jsonify({"message": "Story deleted"})

# ============================================================
# 🟢 Upload-Route für Titelbilder
# ============================================================
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

    file_url = f"/uploads/stories/{filename}"

    return jsonify({"message": "File uploaded", "url": file_url}), 201


# ============================================================
# 🟣 Favoriten-Funktionen
# ============================================================
@story_bp.route("/favorites", methods=["GET"])
@jwt_required()
def get_favorites():
    """Alle Favoriten-Stories des eingeloggten Users"""
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorite_stories = [f.story for f in favorites]
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "genre": s.genre,
            "cover_image": (
                s.cover_image if s.cover_image.startswith("http")
                else f"https://plot-weavers-backend.onrender.com{s.cover_image}"
                if s.cover_image else None
            ),
            "created_by": s.creator.username if s.creator else "Unknown"
        }
        for s in favorite_stories
    ])


@story_bp.route("/favorites/<story_id>", methods=["POST"])
@jwt_required()
def add_favorite(story_id):
    """Story zu Favoriten hinzufügen"""
    user_id = get_jwt_identity()
    if Favorite.query.filter_by(user_id=user_id, story_id=story_id).first():
        return jsonify({"message": "Already in favorites"}), 200

    favorite = Favorite(user_id=user_id, story_id=story_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Story added to favorites"}), 201


@story_bp.route("/favorites/<story_id>", methods=["DELETE"])
@jwt_required()
def remove_favorite(story_id):
    """Story aus Favoriten entfernen"""
    user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(user_id=user_id, story_id=story_id).first()
    if not favorite:
        return jsonify({"message": "Not in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Story removed from favorites"}), 200


# ============================================================
# 🟣 Eigene Stories des Users abrufen
# ============================================================
@story_bp.route("/my-stories", methods=["GET"])
@jwt_required()
def my_stories():
    user_id = get_jwt_identity()
    stories = Story.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "genre": s.genre,
            "description": s.description,
            "cover_image": (
                s.cover_image if s.cover_image.startswith("http")
                else f"https://plot-weavers-backend.onrender.com{s.cover_image}"
                if s.cover_image else None
            ),
            "created_by": s.creator.username if s.creator else "Unknown"
        }
        for s in stories
    ])
