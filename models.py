from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


def generate_uuid():
    return str(uuid.uuid4())

# User Model
class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.Text, nullable=True)

    stories = db.relationship("Story", backref="creator", lazy=True)
    chapters = db.relationship("Chapter", backref="creator", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Story Model
class Story(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    image = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    chapters = db.relationship("Chapter", backref="story", cascade="all, delete", lazy=True)


# Chapter Model
class Chapter(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    story_id = db.Column(db.String, db.ForeignKey("story.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)


# Favorites
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    story_id = db.Column(db.String, db.ForeignKey("story.id"), nullable=False)


# Likes
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    chapter_id = db.Column(db.String, db.ForeignKey("chapter.id"), nullable=False)
