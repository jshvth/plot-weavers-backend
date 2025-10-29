import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename


upload_bp = Blueprint("upload", __name__)

# Erlaubte Dateiendungen
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# 🔹 Allgemeiner Upload-Endpunkt für Story-Cover etc.
@upload_bp.route("", methods=["POST"])
def upload_generic_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"

        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_STORIES"], unique_name)
        os.makedirs(current_app.config["UPLOAD_FOLDER_STORIES"], exist_ok=True)
        file.save(save_path)

        # ✅ Baue vollständige URL zurück zum Bild
        image_url = f"{request.host_url}upload/stories/{unique_name}"
        return jsonify({"message": "File uploaded", "url": image_url}), 201

    return jsonify({"error": "Invalid file type"}), 400


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Profilbild hochladen
@upload_bp.route("/profile", methods=["POST"])
def upload_profile():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_PROFILES"], filename)
        os.makedirs(current_app.config["UPLOAD_FOLDER_PROFILES"], exist_ok=True)
        file.save(save_path)
        return jsonify({"message": "Profile image uploaded", "filename": filename}), 201

    return jsonify({"error": "Invalid file type"}), 400


# Story-Bild hochladen
@upload_bp.route("/story/<string:story_id>", methods=["POST"])
def upload_story(story_id):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(f"story_{story_id}_" + file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_STORIES"], filename)
        os.makedirs(current_app.config["UPLOAD_FOLDER_STORIES"], exist_ok=True)
        file.save(save_path)
        return jsonify({"message": "Story image uploaded", "filename": filename}), 201

    return jsonify({"error": "Invalid file type"}), 400


# Route um Bilder auszuliefern (Frontend kann sie direkt laden)
@upload_bp.route("/profiles/<filename>")
def get_profile_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_PROFILES"], filename)


@upload_bp.route("/stories/<filename>")
def get_story_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_STORIES"], filename)
