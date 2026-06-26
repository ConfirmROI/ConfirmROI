from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.services.audit_service import AuditService

audit_bp = Blueprint("audit", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


@audit_bp.route("", methods=["GET"])
@jwt_required()
def get_audit_history():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    entity_type = request.args.get("entity_type")
    entity_id = request.args.get("entity_id")

    if not entity_type or not entity_id:
        return jsonify({"error": "entity_type and entity_id are required"}), 400

    try:
        entity_id = int(entity_id)
    except (ValueError, TypeError):
        return jsonify({"error": "entity_id must be an integer"}), 400

    entries = AuditService.get_entity_history(entity_type, entity_id)
    return jsonify([e.to_dict() for e in entries]), 200
