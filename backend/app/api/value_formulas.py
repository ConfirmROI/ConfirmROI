from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    AssumptionDataType,
    FormulaAssumption,
    ProjectFormula,
    ProjectAssumptionValue,
)
from app.models.project import Project
from app.models.team import Team
from app.models.user import User
from app.services.formula_service import FormulaService, RoiService
from app.services.audit_service import AuditService
from app.access import get_visible_team_ids

formulas_bp = Blueprint("formulas", __name__)


def _get_current_user():
    identity = get_jwt_identity()
    try:
        uid = int(identity)
    except (ValueError, TypeError):
        return None
    return db.session.get(User, uid)


@formulas_bp.route("", methods=["GET"])
@jwt_required()
def list_formulas():
    user = _get_current_user()
    formulas = ValueFormula.query.filter(
        (ValueFormula.is_system == True) | (ValueFormula.user_id == user.id)
    ).all()
    return jsonify([a.to_dict() for a in formulas]), 200


@formulas_bp.route("/<int:formula_id>", methods=["GET"])
@jwt_required()
def get_formula(formula_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if not arch.is_system and arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    return jsonify(arch.to_dict()), 200


@formulas_bp.route("", methods=["POST"])
@jwt_required()
def create_formula():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("name"):
        return jsonify({"error": "Formula name is required"}), 400
    if not data.get("formula"):
        return jsonify({"error": "Formula is required"}), 400

    arch = ValueFormula(
        name=data["name"],
        description=data.get("description"),
        formula=data["formula"],
        is_system=False,
        user_id=user.id,
    )
    db.session.add(arch)
    db.session.flush()

    sort_idx = 0

    for assumption_id in data.get("assumption_ids", []):
        assumption = db.session.get(ValueAssumption, assumption_id)
        if not assumption:
            continue
        if not assumption.is_system and assumption.user_id != user.id:
            continue
        link = FormulaAssumption(
            formula_id=arch.id,
            assumption_id=assumption_id,
            sort_order=sort_idx,
        )
        db.session.add(link)
        sort_idx += 1

    for a_data in data.get("assumptions", []):
        if not a_data.get("key") or not a_data.get("label"):
            continue
        assumption = ValueAssumption(
            key=a_data["key"],
            label=a_data["label"],
            data_type=AssumptionDataType(a_data.get("data_type", "number")),
            default_value=a_data.get("default_value", 0),
            description=a_data.get("description"),
            is_system=False,
            user_id=user.id,
        )
        db.session.add(assumption)
        db.session.flush()
        link = FormulaAssumption(
            formula_id=arch.id,
            assumption_id=assumption.id,
            sort_order=sort_idx,
        )
        db.session.add(link)
        sort_idx += 1

    AuditService.log_change(user.id, "formula", arch.id, "create", change_reason=data.get("change_reason"))
    db.session.commit()
    return jsonify(arch.to_dict()), 201


@formulas_bp.route("/<int:formula_id>/assumptions", methods=["GET"])
@jwt_required()
def list_assumptions(formula_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if not arch.is_system and arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403
    return jsonify([a.to_dict() for a in arch.assumptions]), 200


@formulas_bp.route("/<int:formula_id>/assumptions/<int:assumption_id>", methods=["POST"])
@jwt_required()
def link_assumption(formula_id, assumption_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if arch.is_system:
        return jsonify({"error": "Cannot modify system formula"}), 403
    if arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    assumption = db.session.get(ValueAssumption, assumption_id)
    if not assumption:
        return jsonify({"error": "Assumption not found"}), 404
    if not assumption.is_system and assumption.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    existing = FormulaAssumption.query.filter_by(
        formula_id=formula_id, assumption_id=assumption_id
    ).first()
    if existing:
        return jsonify({"error": "Assumption already linked to formula"}), 400

    max_sort = db.session.query(db.func.max(FormulaAssumption.sort_order)).filter_by(
        formula_id=formula_id
    ).scalar() or -1
    link = FormulaAssumption(
        formula_id=formula_id,
        assumption_id=assumption_id,
        sort_order=max_sort + 1,
    )
    db.session.add(link)
    data = request.get_json(silent=True) or {}
    AuditService.log_change(
        user.id, "formula", formula_id, "update",
        changes={"linked_assumption": {"old": None, "new": assumption_id}},
        change_reason=data.get("change_reason"),
    )
    db.session.commit()
    return jsonify(assumption.to_dict()), 201


@formulas_bp.route("/<int:formula_id>/assumptions/<int:assumption_id>", methods=["DELETE"])
@jwt_required()
def unlink_assumption(formula_id, assumption_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if arch.is_system:
        return jsonify({"error": "Cannot modify system formula"}), 403
    if arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    link = FormulaAssumption.query.filter_by(
        formula_id=formula_id, assumption_id=assumption_id
    ).first()
    if not link:
        return jsonify({"error": "Assumption not linked to formula"}), 404

    db.session.delete(link)
    AuditService.log_change(
        user.id, "formula", formula_id, "update",
        changes={"unlinked_assumption": {"old": assumption_id, "new": None}},
    )
    db.session.commit()
    return "", 204


@formulas_bp.route("/assumptions", methods=["GET"])
@jwt_required()
def list_all_assumptions():
    user = _get_current_user()
    assumptions = ValueAssumption.query.filter(
        (ValueAssumption.is_system == True) | (ValueAssumption.user_id == user.id)
    ).all()
    return jsonify([a.to_dict() for a in assumptions]), 200


@formulas_bp.route("/assumptions", methods=["POST"])
@jwt_required()
def create_assumption():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("key") or not data.get("label"):
        return jsonify({"error": "key and label are required"}), 400

    assumption = ValueAssumption(
        key=data["key"],
        label=data["label"],
        data_type=AssumptionDataType(data.get("data_type", "number")),
        default_value=data.get("default_value", 0),
        description=data.get("description"),
        is_system=False,
        user_id=user.id,
    )
    db.session.add(assumption)
    db.session.flush()
    AuditService.log_change(user.id, "assumption", assumption.id, "create", change_reason=data.get("change_reason"))
    db.session.commit()
    return jsonify(assumption.to_dict()), 201


@formulas_bp.route("/assumptions/<int:assumption_id>", methods=["PUT"])
@jwt_required()
def update_assumption(assumption_id):
    user = _get_current_user()
    assumption = db.session.get(ValueAssumption, assumption_id)
    if not assumption:
        return jsonify({"error": "Assumption not found"}), 404
    if not assumption.is_system and assumption.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    old_dict = assumption.to_dict()

    if "key" in data:
        assumption.key = data["key"]
    if "label" in data:
        assumption.label = data["label"]
    if "data_type" in data:
        assumption.data_type = AssumptionDataType(data["data_type"])
    if "default_value" in data:
        assumption.default_value = data["default_value"]
    if "description" in data:
        assumption.description = data["description"]

    new_dict = assumption.to_dict()
    changes = AuditService.diff_fields(old_dict, new_dict)
    AuditService.log_change(
        user.id, "assumption", assumption_id, "update",
        changes=changes, change_reason=data.get("change_reason"),
    )
    db.session.commit()
    return jsonify(assumption.to_dict()), 200


@formulas_bp.route("/assumptions/<int:assumption_id>", methods=["DELETE"])
@jwt_required()
def delete_assumption(assumption_id):
    user = _get_current_user()
    assumption = db.session.get(ValueAssumption, assumption_id)
    if not assumption:
        return jsonify({"error": "Assumption not found"}), 404
    if assumption.is_system:
        return jsonify({"error": "Cannot delete system assumption"}), 403
    if assumption.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True) or {}
    AuditService.log_change(
        user.id, "assumption", assumption_id, "delete",
        change_reason=data.get("change_reason"),
    )
    db.session.delete(assumption)
    db.session.commit()
    return "", 204


@formulas_bp.route("/<int:formula_id>", methods=["PUT"])
@jwt_required()
def update_formula(formula_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if arch.is_system:
        return jsonify({"error": "Cannot modify system formula"}), 403
    if arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    old_dict = arch.to_dict()

    if "name" in data:
        arch.name = data["name"]
    if "description" in data:
        arch.description = data["description"]
    if "formula" in data:
        arch.formula = data["formula"]

    if "assumption_ids" in data:
        old_assumption_ids = [a["id"] for a in old_dict.get("assumptions", [])]
        FormulaAssumption.query.filter_by(formula_id=formula_id).delete()
        for i, assumption_id in enumerate(data["assumption_ids"]):
            assumption = db.session.get(ValueAssumption, assumption_id)
            if not assumption:
                continue
            if not assumption.is_system and assumption.user_id != user.id:
                continue
            link = FormulaAssumption(
                formula_id=formula_id,
                assumption_id=assumption_id,
                sort_order=i,
            )
            db.session.add(link)
        changes_extra = {"assumption_ids": {"old": old_assumption_ids, "new": data["assumption_ids"]}}
    else:
        changes_extra = None

    new_dict = arch.to_dict()
    changes = AuditService.diff_fields(old_dict, new_dict)
    if changes_extra:
        changes = changes or {}
        changes.update(changes_extra)
    AuditService.log_change(
        user.id, "formula", formula_id, "update",
        changes=changes, change_reason=data.get("change_reason"),
    )
    db.session.commit()
    return jsonify(arch.to_dict()), 200


@formulas_bp.route("/usage", methods=["GET"])
@jwt_required()
def usage_stats():
    user = _get_current_user()

    team_ids = get_visible_team_ids(user)

    assumption_usage = {}
    for a in ValueAssumption.query.filter(
        (ValueAssumption.is_system == True) | (ValueAssumption.user_id == user.id)
    ).all():
        formula_ids = set()
        project_ids = set()
        for arch in a.formulas:
            formula_ids.add(arch.id)
            for pa in ProjectFormula.query.filter_by(formula_id=arch.id).all():
                proj = db.session.get(Project, pa.project_id)
                if proj and proj.team_id in team_ids:
                    project_ids.add(proj.id)
        assumption_usage[a.id] = {
            "formula_count": len(formula_ids),
            "project_count": len(project_ids),
            "formula_ids": list(formula_ids),
            "project_ids": list(project_ids),
        }

    formula_usage = {}
    for arch in ValueFormula.query.filter(
        (ValueFormula.is_system == True) | (ValueFormula.user_id == user.id)
    ).all():
        project_ids = set()
        for pa in ProjectFormula.query.filter_by(formula_id=arch.id).all():
            proj = db.session.get(Project, pa.project_id)
            if proj and proj.team_id in team_ids:
                project_ids.add(proj.id)
        formula_usage[arch.id] = {
            "project_count": len(project_ids),
            "project_ids": list(project_ids),
        }

    return jsonify({"assumptions": assumption_usage, "formulas": formula_usage}), 200


@formulas_bp.route("/<int:formula_id>", methods=["DELETE"])
@jwt_required()
def delete_formula(formula_id):
    user = _get_current_user()
    arch = db.session.get(ValueFormula, formula_id)
    if not arch:
        return jsonify({"error": "Formula not found"}), 404
    if arch.is_system:
        return jsonify({"error": "Cannot delete system formula"}), 403
    if arch.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(silent=True) or {}
    AuditService.log_change(
        user.id, "formula", formula_id, "delete",
        change_reason=data.get("change_reason"),
    )
    db.session.delete(arch)
    db.session.commit()
    return "", 204
