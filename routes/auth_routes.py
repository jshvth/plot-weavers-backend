from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "username": user.username,
        "id": user.id
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "profile_image": user.profile_image
    })

@auth_bp.before_app_request
def create_default_admin():
    # Nur einmal pro App-Start
    if getattr(current_app, "_admin_created", False):
        return

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin")
        admin.set_password("admin")  # 👉 korrekter Weg, Passwort wird gehasht
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created: username='admin', password='admin'")

    test_user = User.query.filter_by(username="testuser").first()
    if not test_user:
        test_user = User(username="testuser")
        test_user.set_password("testuser")
        db.session.add(test_user)
        db.session.commit()
        print("✅ Default testuser created: username='testuser', password='testuser'")

    current_app._admin_created = True
