import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.project import Project, ProjectStatus, ExternalSource
from app.models.roi import JiraConnection
from app.models.team import Team
from app.models.user import User


class JiraService:
    @staticmethod
    def create_connection(team_id: int, base_url: str, api_token: str, email: str) -> JiraConnection:
        conn = JiraConnection(
            team_id=team_id,
            base_url=base_url,
            api_token=api_token,
            email=email,
        )
        db.session.add(conn)
        db.session.commit()
        return conn

    @staticmethod
    def get_connection(connection_id: int) -> JiraConnection | None:
        return db.session.get(JiraConnection, connection_id)

    @staticmethod
    def get_connection_by_team(team_id: int) -> JiraConnection | None:
        return JiraConnection.query.filter_by(team_id=team_id).first()

    @staticmethod
    def delete_connection(connection_id: int) -> None:
        conn = db.session.get(JiraConnection, connection_id)
        if conn:
            db.session.delete(conn)
            db.session.commit()

    @staticmethod
    def fetch_projects(connection_id: int) -> list[dict]:
        conn = JiraService.get_connection(connection_id)
        if not conn:
            raise ValueError("Jira connection not found")

        url = f"{conn.base_url}/rest/api/3/project"
        headers = {"Accept": "application/json"}
        auth = (conn.email, conn.api_token)

        resp = requests.get(url, headers=headers, auth=auth, timeout=30)
        if resp.status_code != 200:
            raise Exception(f"Jira API error: {resp.status_code} - {resp.text}")

        return resp.json()

    @staticmethod
    def import_projects(connection_id: int, team_id: int) -> dict:
        result = {"imported": 0, "errors": []}
        try:
            projects = JiraService.fetch_projects(connection_id)
        except Exception as e:
            result["errors"].append(str(e))
            return result

        for proj in projects:
            key = proj.get("key")
            name = proj.get("name", key)
            if not key:
                result["errors"].append(f"Project missing key: {name}")
                continue

            existing = Project.query.filter_by(
                team_id=team_id, external_id=key, external_source=ExternalSource.jira
            ).first()
            if existing:
                continue

            project = Project(
                team_id=team_id,
                name=name,
                external_id=key,
                external_source=ExternalSource.jira,
                status=ProjectStatus.planning,
            )
            db.session.add(project)
            result["imported"] += 1

        db.session.commit()
        return result


jira_bp = Blueprint("jira", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


def _check_team_access(team_id, user):
    team = db.session.get(Team, team_id)
    if not team:
        return None, ("Team not found", 404)
    if team.manager_user_id != user.id:
        return None, ("Access denied", 403)
    return team, None


@jira_bp.route("/teams/<int:team_id>/jira", methods=["POST"])
@jwt_required()
def create_jira_connection(team_id):
    user = _get_current_user()
    team, error = _check_team_access(team_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    data = request.get_json(silent=True)
    if not data or not data.get("base_url") or not data.get("api_token") or not data.get("email"):
        return jsonify({"error": "base_url, api_token, and email are required"}), 400

    existing = JiraService.get_connection_by_team(team_id)
    if existing:
        return jsonify({"error": "Jira connection already exists for this team"}), 400

    conn = JiraService.create_connection(
        team_id=team_id,
        base_url=data["base_url"],
        api_token=data["api_token"],
        email=data["email"],
    )
    return jsonify(conn.to_dict()), 201


@jira_bp.route("/teams/<int:team_id>/jira", methods=["GET"])
@jwt_required()
def get_jira_connection(team_id):
    user = _get_current_user()
    team, error = _check_team_access(team_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    conn = JiraService.get_connection_by_team(team_id)
    if not conn:
        return jsonify({"error": "No Jira connection found"}), 404
    return jsonify(conn.to_dict()), 200


@jira_bp.route("/teams/<int:team_id>/jira", methods=["DELETE"])
@jwt_required()
def delete_jira_connection(team_id):
    user = _get_current_user()
    team, error = _check_team_access(team_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    conn = JiraService.get_connection_by_team(team_id)
    if not conn:
        return jsonify({"error": "No Jira connection found"}), 404

    JiraService.delete_connection(conn.id)
    return "", 204


@jira_bp.route("/teams/<int:team_id>/jira/import", methods=["POST"])
@jwt_required()
def import_jira_projects(team_id):
    user = _get_current_user()
    team, error = _check_team_access(team_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    conn = JiraService.get_connection_by_team(team_id)
    if not conn:
        return jsonify({"error": "No Jira connection found"}), 404

    result = JiraService.import_projects(conn.id, team_id)
    return jsonify(result), 200
