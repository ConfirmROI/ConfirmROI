from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    ProjectFormula,
    ProjectAssumptionValue,
)
from app.models.project import Project
from app.models.team import Team
from app.models.user import User
from app.services.formula_service import RoiService
from app.access import check_project_access

assumptions_bp = Blueprint("assumptions", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


def _check_project_access(project_id, user):
    project = db.session.get(Project, project_id)
    if not project:
        return None, ("Project not found", 404)
    if not check_project_access(project, user):
        return None, ("Access denied", 403)
    return project, None


@assumptions_bp.route("/projects/<int:project_id>/formulas", methods=["POST"])
@jwt_required()
def assign_formula(project_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    data = request.get_json(silent=True)
    if not data or not data.get("formula_id"):
        return jsonify({"error": "formula_id is required"}), 400

    arch = db.session.get(ValueFormula, data["formula_id"])
    if not arch:
        return jsonify({"error": "Formula not found"}), 404

    existing = ProjectFormula.query.filter_by(
        project_id=project_id, formula_id=data["formula_id"]
    ).first()
    if existing:
        return jsonify({"error": "Formula already assigned to project"}), 400

    pa = ProjectFormula(
        project_id=project_id,
        formula_id=data["formula_id"],
    )
    db.session.add(pa)
    db.session.flush()

    for assumption in arch.assumptions:
        pav = ProjectAssumptionValue(
            project_formula_id=pa.id,
            assumption_id=assumption.id,
            value=assumption.default_value,
        )
        db.session.add(pav)

    db.session.commit()
    return jsonify(pa.to_dict()), 201


@assumptions_bp.route("/projects/<int:project_id>/formulas/<int:pa_id>", methods=["DELETE"])
@jwt_required()
def unassign_formula(project_id, pa_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    pa = db.session.get(ProjectFormula, pa_id)
    if not pa or pa.project_id != project_id:
        return jsonify({"error": "Project formula not found"}), 404

    db.session.delete(pa)
    db.session.commit()
    return jsonify({"message": "Formula unassigned"}), 200


@assumptions_bp.route("/projects/<int:project_id>/formulas", methods=["GET"])
@jwt_required()
def list_project_formulas(project_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    pas = ProjectFormula.query.filter_by(project_id=project_id).all()
    return jsonify([pa.to_dict() for pa in pas]), 200


@assumptions_bp.route(
    "/projects/<int:project_id>/formulas/<int:pa_id>/assumptions/<int:assumption_id>",
    methods=["PUT"],
)
@jwt_required()
def update_assumption_value(project_id, pa_id, assumption_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    pa = db.session.get(ProjectFormula, pa_id)
    if not pa or pa.project_id != project_id:
        return jsonify({"error": "Project formula not found"}), 404

    pav = ProjectAssumptionValue.query.filter_by(
        project_formula_id=pa_id, assumption_id=assumption_id
    ).first()
    if not pav:
        return jsonify({"error": "Assumption value not found"}), 404

    data = request.get_json(silent=True)
    if not data or "value" not in data:
        return jsonify({"error": "value is required"}), 400

    pav.value = data["value"]
    db.session.commit()
    return jsonify(pav.to_dict()), 200


@assumptions_bp.route(
    "/projects/<int:project_id>/formulas/<int:pa_id>/calculate",
    methods=["POST"],
)
@jwt_required()
def calculate_roi(project_id, pa_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    pa = db.session.get(ProjectFormula, pa_id)
    if not pa or pa.project_id != project_id:
        return jsonify({"error": "Project formula not found"}), 404

    result = RoiService.calculate_roi(pa_id)
    if result is None:
        return jsonify({"error": "Failed to calculate ROI"}), 500

    return jsonify(result), 200


@assumptions_bp.route(
    "/projects/<int:project_id>/formulas/<int:pa_id>/roi",
    methods=["GET"],
)
@jwt_required()
def get_latest_roi(project_id, pa_id):
    user = _get_current_user()
    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    pa = db.session.get(ProjectFormula, pa_id)
    if not pa or pa.project_id != project_id:
        return jsonify({"error": "Project formula not found"}), 404

    result = RoiService.get_latest_roi(pa_id)
    if result is None:
        return jsonify({"error": "No ROI calculation found"}), 404

    return jsonify(result), 200
