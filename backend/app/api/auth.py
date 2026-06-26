from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    from app.services.auth_service import AuthService

    data = request.get_json(silent=True)
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    result, error = AuthService.register(data["email"], data["password"], data.get("name"))
    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    from app.services.auth_service import AuthService

    data = request.get_json(silent=True)
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    result, error = AuthService.login(data["email"], data["password"])
    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200


@auth_bp.route("/auto-login", methods=["POST"])
def auto_login():
    from app.services.auth_service import AuthService

    result, error = AuthService.auto_login()
    if error:
        return jsonify({"error": error}), 404

    return jsonify(result), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    from app.services.auth_service import AuthService

    user = AuthService.get_user_by_id(current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    from app.extensions import db
    from app.models.user import User

    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid identity"}), 400

    user = db.session.get(User, uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "default_labor_cost_per_week" in data:
        val = data["default_labor_cost_per_week"]
        user.default_labor_cost_per_week = val if val is not None else None

    if "name" in data:
        user.name = data["name"]

    db.session.commit()
    return jsonify(user.to_dict()), 200
