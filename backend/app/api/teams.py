from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.team import Team, TeamMember, TeamMemberRole
from app.models.user import User, UserTier

teams_bp = Blueprint("teams", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


@teams_bp.route("", methods=["POST"])
@jwt_required()
def create_team():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "Team name is required"}), 400

    existing = Team.query.filter_by(manager_user_id=user.id).count()
    if user.tier == UserTier.free and existing >= 1:
        return jsonify({"error": "Free tier allows only one team"}), 403

    team = Team(
        name=data["name"],
        manager_user_id=user.id,
        parent_team_id=data.get("parent_team_id"),
    )
    db.session.add(team)
    db.session.flush()

    member = TeamMember(
        team_id=team.id,
        user_id=user.id,
        role=TeamMemberRole.manager,
    )
    db.session.add(member)
    db.session.commit()

    return jsonify(team.to_dict()), 201


@teams_bp.route("", methods=["GET"])
@jwt_required()
def list_teams():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.tier == UserTier.paid:
        teams = Team.query.all()
    else:
        teams = Team.query.filter_by(manager_user_id=user.id).all()
    teams.sort(key=lambda t: (0 if t.manager_user_id == user.id else 1, t.name))
    return jsonify([t.to_dict() for t in teams]), 200


@teams_bp.route("/<int:team_id>/members", methods=["GET"])
@jwt_required()
def list_team_members(team_id):
    user = _get_current_user()
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id and user.tier != UserTier.paid:
        return jsonify({"error": "Access denied"}), 403
    return jsonify([m.to_dict() for m in team.members]), 200


@teams_bp.route("/<int:team_id>", methods=["GET"])
@jwt_required()
def get_team(team_id):
    user = _get_current_user()
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    return jsonify(team.to_dict()), 200


@teams_bp.route("/<int:team_id>", methods=["PUT"])
@jwt_required()
def update_team(team_id):
    user = _get_current_user()
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        team.name = data["name"]
    if "avg_labor_cost_per_week" in data:
        val = data["avg_labor_cost_per_week"]
        team.avg_labor_cost_per_week = val if val is not None else None
    db.session.commit()
    return jsonify(team.to_dict()), 200


@teams_bp.route("/<int:team_id>", methods=["DELETE"])
@jwt_required()
def delete_team(team_id):
    user = _get_current_user()
    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(team)
    db.session.commit()
    return "", 204
