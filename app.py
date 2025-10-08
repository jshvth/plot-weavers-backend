from flask import Flask
from config import Config
from extensions import db, jwt, cors
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.story_routes import story_bp
from routes.chapter_routes import chapter_bp
from routes.upload_routes import upload_bp
from routes.like_routes import like_bp
from routes.favorites_routes import favorite_bp
from routes.comment_routes import comment_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Sicherstellen, dass Upload-Ordner existieren
    os.makedirs(app.config["UPLOAD_FOLDER_PROFILES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_STORIES"], exist_ok=True)

    # Blueprints registrieren
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(story_bp, url_prefix="/stories")
    app.register_blueprint(chapter_bp, url_prefix="/chapters")
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(like_bp, url_prefix="/likes")
    app.register_blueprint(favorite_bp, url_prefix="/favorites")
    app.register_blueprint(comment_bp, url_prefix="/comments")

    # Datenbanktabellen erstellen
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
