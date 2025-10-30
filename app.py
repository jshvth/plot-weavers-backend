from flask import Flask, request, make_response
from config import Config
from extensions import db, jwt
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.story_routes import story_bp
from routes.chapter_routes import chapter_bp
from routes.upload_routes import upload_bp
from routes.like_routes import like_bp
from routes.favorites_routes import favorite_bp
from routes.comment_routes import comment_bp
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    local_ports = [f"http://localhost:{port}" for port in range(5173, 5180)]

    #  CORS vollständig aktivieren
    CORS(
        app,
        resources={r"/*": {"origins": local_ports + [
            "https://plot-weavers-frontend.onrender.com"
        ]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ✅ Preflight-Handler für alle OPTIONS-Anfragen
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            origin = request.headers.get("Origin", "")
            if origin in ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177", "https://plot-weavers-frontend.onrender.com"]:
                response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.status_code = 204
            return response

    # Init Extensions
    db.init_app(app)
    jwt.init_app(app)

    # Upload-Ordner sicherstellen
    os.makedirs(app.config["UPLOAD_FOLDER_PROFILES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_STORIES"], exist_ok=True)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(story_bp, url_prefix="/stories")
    app.register_blueprint(chapter_bp, url_prefix="/chapters")
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(like_bp, url_prefix="/likes")
    app.register_blueprint(favorite_bp, url_prefix="/favorites")
    app.register_blueprint(comment_bp, url_prefix="/comments")

    # 🖼️ STATIC ROUTE: für Story-Bilder
    @app.route("/uploads/stories/<path:filename>")
    def serve_story_image(filename):
        folder = os.path.join(app.root_path, "uploads", "stories")
        return send_from_directory(folder, filename)

    @app.route("/")
    def index():
        return {"message": "✅ PlotWeavers Backend is running!"}

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
