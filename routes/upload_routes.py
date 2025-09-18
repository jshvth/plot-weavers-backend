import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

# Erlaubte Dateiendungen
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Profilbild hochladen
@upload_bp.route("/upload/profile", methods=["POST"])
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
@upload_bp.route("/upload/story/<int:story_id>", methods=["POST"])
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
@upload_bp.route("/uploads/profiles/<filename>")
def get_profile_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_PROFILES"], filename)


@upload_bp.route("/uploads/stories/<filename>")
def get_story_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER_STORIES"], filename)
