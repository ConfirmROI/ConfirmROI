import csv
import io
from datetime import date
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.project import Project, ProjectStatus, ExternalSource
from app.models.value_formula import ProjectFormula
from app.models.cost import CostEntry, CostCategory
from app.models.roi import RoiCalculation
from app.models.team import Team, TeamMember
from app.models.user import User
from app.services.import_service import CsvImportService
from app.access import check_project_access, check_team_access, get_visible_team_ids

projects_bp = Blueprint("projects", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


@projects_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "Project name is required"}), 400

    team_id = data.get("team_id")
    if not team_id:
        member = TeamMember.query.filter_by(user_id=user.id).order_by(TeamMember.id).first()
        if member:
            team_id = member.team_id
        else:
            return jsonify({"error": "Team ID is required"}), 400

    team = db.session.get(Team, team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if not check_team_access(team, user):
        return jsonify({"error": "Access denied"}), 403

    project = Project(
        team_id=team_id,
        name=data["name"],
        description=data.get("description"),
        external_id=data.get("external_id"),
        external_source=ExternalSource(data.get("external_source", "manual")),
        status=ProjectStatus(data.get("status", "planning")),
        start_date=_parse_date(data.get("start_date")),
        end_date=_parse_date(data.get("end_date")),
    )
    db.session.add(project)
    db.session.flush()

    default_cost = CostEntry(
        project_id=project.id,
        category=CostCategory.development,
        description="Development (labor)",
        person_weeks=0,
        amount=0,
    )
    db.session.add(default_cost)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@projects_bp.route("/teams", methods=["GET"])
@jwt_required()
def list_user_teams():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    teams = Team.query.filter_by(manager_user_id=user.id).all()
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "manager_user_id": t.manager_user_id,
    } for t in teams]), 200


@projects_bp.route("", methods=["GET"])
@jwt_required()
def list_projects():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    team_id_filter = request.args.get("team_id")
    managed_only = request.args.get("managed_only", "").lower() in ("1", "true", "yes")
    if managed_only:
        team_ids = [t.id for t in Team.query.filter_by(manager_user_id=user.id).all()]
        query = Project.query.filter(Project.team_id.in_(team_ids))
        if team_id_filter:
            query = query.filter_by(team_id=int(team_id_filter))
    else:
        team_ids = get_visible_team_ids(user)
        query = Project.query.filter(Project.team_id.in_(team_ids))
        if team_id_filter:
            query = query.filter_by(team_id=int(team_id_filter))

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date:
        parsed_start = _parse_date(start_date)
        if parsed_start:
            query = query.filter(Project.start_date >= parsed_start)
    if end_date:
        parsed_end = _parse_date(end_date)
        if parsed_end:
            query = query.filter(Project.end_date <= parsed_end)

    projects = query.all()

    include_roi = request.args.get("include_roi", "").lower() in ("1", "true", "yes")
    if include_roi:
        from app.services.formula_service import FormulaService, RoiService
        result = []
        for p in projects:
            d = p.to_dict()
            pas = ProjectFormula.query.filter_by(project_id=p.id).all()
            gross_annual = 0.0
            found_any = False
            for pa in pas:
                formula = pa.formula
                if not formula or not formula.formula:
                    continue
                values = {}
                for assumption in formula.assumptions:
                    pav = next(
                        (v for v in pa.assumption_values if v.assumption_id == assumption.id),
                        None,
                    )
                    values[assumption.key] = float(pav.value) if pav else float(assumption.default_value)
                if "implementation_cost" in values:
                    values["implementation_cost"] = 0
                try:
                    result_val = FormulaService.evaluate(formula.formula, values)
                    gross_annual += float(result_val)
                    found_any = True
                except Exception:
                    pass
            if found_any:
                costs = RoiService._get_cost_breakdown(p.id)
                recurring_annual = costs["recurring_monthly"] * 12 + costs["recurring_annual"]
                first_year_investment = costs["one_time"] + recurring_annual
                d["roi_1yr"] = gross_annual - first_year_investment
                d["roi_3yr"] = gross_annual * 3 - (costs["one_time"] + recurring_annual * 3)
            else:
                d["roi_1yr"] = None
                d["roi_3yr"] = None
            result.append(d)
        return jsonify(result), 200

    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    user = _get_current_user()
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if not check_project_access(project, user):
        return jsonify({"error": "Access denied"}), 403

    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    user = _get_current_user()
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if not check_project_access(project, user):
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        project.name = data["name"]
    if "description" in data:
        project.description = data["description"]
    if "status" in data:
        project.status = ProjectStatus(data["status"])
    if "start_date" in data:
        project.start_date = _parse_date(data["start_date"])
    if "end_date" in data:
        project.end_date = _parse_date(data["end_date"])
    if "external_id" in data:
        project.external_id = data["external_id"]

    db.session.commit()
    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user = _get_current_user()
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if not check_project_access(project, user):
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(project)
    db.session.commit()
    return "", 204


@projects_bp.route("/import", methods=["POST"])
@jwt_required()
def import_projects():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    team_id = request.args.get("team_id")
    if not team_id:
        return jsonify({"error": "team_id query parameter is required"}), 400

    team = db.session.get(Team, int(team_id))
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    csv_data = request.get_data(as_text=True)
    if not csv_data.strip():
        return jsonify({"error": "No CSV data provided"}), 400

    buf = io.StringIO(csv_data)
    result = CsvImportService.import_projects(buf, int(team_id))
    return jsonify(result), 200


@projects_bp.route("/export", methods=["GET"])
@jwt_required()
def export_projects():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    team_id = request.args.get("team_id")
    if not team_id:
        return jsonify({"error": "team_id query parameter is required"}), 400

    team = db.session.get(Team, int(team_id))
    if not team:
        return jsonify({"error": "Team not found"}), 404
    if team.manager_user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    projects = Project.query.filter_by(team_id=int(team_id)).all()

    from app.services.formula_service import FormulaService, RoiService
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "description", "status", "external_id", "external_source", "start_date", "end_date", "roi_1yr", "roi_3yr"])

    for project in projects:
        pas = ProjectFormula.query.filter_by(project_id=project.id).all()
        gross_annual = 0.0
        found_any = False
        for pa in pas:
            formula = pa.formula
            if not formula or not formula.formula:
                continue
            values = {}
            for assumption in formula.assumptions:
                pav = next(
                    (v for v in pa.assumption_values if v.assumption_id == assumption.id),
                    None,
                )
                values[assumption.key] = float(pav.value) if pav else float(assumption.default_value)
            if "implementation_cost" in values:
                values["implementation_cost"] = 0
            try:
                result_val = FormulaService.evaluate(formula.formula, values)
                gross_annual += float(result_val)
                found_any = True
            except Exception:
                pass
        if found_any:
            costs = RoiService._get_cost_breakdown(project.id)
            recurring_annual = costs["recurring_monthly"] * 12 + costs["recurring_annual"]
            roi_1yr = gross_annual - (costs["one_time"] + recurring_annual)
            roi_3yr = gross_annual * 3 - (costs["one_time"] + recurring_annual * 3)
        else:
            roi_1yr = ""
            roi_3yr = ""
        writer.writerow([
            project.id,
            project.name,
            project.description or "",
            project.status.value if project.status else "",
            project.external_id or "",
            project.external_source.value if project.external_source else "",
            project.start_date.isoformat() if project.start_date else "",
            project.end_date.isoformat() if project.end_date else "",
            roi_1yr,
            roi_3yr,
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=projects_team_{team_id}.csv"},
    )
