from datetime import date
from decimal import Decimal

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.cost import CostEntry, CostCategory, CostType
from app.models.project import Project
from app.models.team import Team
from app.models.user import User
from app.access import check_project_access

costs_bp = Blueprint("costs", __name__)


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


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


@costs_bp.route("/projects/<int:project_id>/costs", methods=["GET"])
@jwt_required()
def list_costs(project_id):
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    costs = CostEntry.query.filter_by(project_id=project_id).order_by(CostEntry.created_at).all()
    return jsonify([c.to_dict() for c in costs]), 200


@costs_bp.route("/projects/<int:project_id>/costs", methods=["POST"])
@jwt_required()
def create_cost(project_id):
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    category_str = data.get("category", "development")
    try:
        category = CostCategory(category_str)
    except ValueError:
        return jsonify({"error": f"Invalid category '{category_str}'"}), 400

    cost_type_str = data.get("cost_type", "one_time")
    try:
        cost_type = CostType(cost_type_str)
    except ValueError:
        return jsonify({"error": f"Invalid cost_type '{cost_type_str}'"}), 400

    person_weeks = data.get("person_weeks")
    if person_weeks is not None:
        person_weeks = Decimal(str(person_weeks))

    amount = Decimal(str(data.get("amount", 0)))

    cost = CostEntry(
        project_id=project_id,
        category=category,
        description=data.get("description"),
        person_weeks=person_weeks,
        amount=amount,
        cost_type=cost_type,
        incurred_date=_parse_date(data.get("incurred_date")),
        is_estimate=data.get("is_estimate", True),
    )

    if category == CostCategory.development:
        db.session.add(cost)
        db.session.flush()
        cost.recompute_amount()

    db.session.add(cost)
    db.session.commit()
    return jsonify(cost.to_dict()), 201


@costs_bp.route("/projects/<int:project_id>/costs/<int:cost_id>", methods=["PUT"])
@jwt_required()
def update_cost(project_id, cost_id):
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    cost = db.session.get(CostEntry, cost_id)
    if not cost or cost.project_id != project_id:
        return jsonify({"error": "Cost not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "category" in data:
        try:
            cost.category = CostCategory(data["category"])
        except ValueError:
            return jsonify({"error": "Invalid category"}), 400

    if "description" in data:
        cost.description = data["description"]

    if "person_weeks" in data:
        pw = data["person_weeks"]
        cost.person_weeks = Decimal(str(pw)) if pw is not None else None

    if "amount" in data:
        cost.amount = Decimal(str(data["amount"]))

    if "cost_type" in data:
        try:
            cost.cost_type = CostType(data["cost_type"])
        except ValueError:
            return jsonify({"error": "Invalid cost_type"}), 400

    if "incurred_date" in data:
        cost.incurred_date = _parse_date(data["incurred_date"])

    if "is_estimate" in data:
        cost.is_estimate = bool(data["is_estimate"])

    if cost.category == CostCategory.development:
        cost.recompute_amount()

    db.session.commit()
    return jsonify(cost.to_dict()), 200


@costs_bp.route("/projects/<int:project_id>/costs/<int:cost_id>", methods=["DELETE"])
@jwt_required()
def delete_cost(project_id, cost_id):
    user = _get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    project, error = _check_project_access(project_id, user)
    if error:
        return jsonify({"error": error[0]}), error[1]

    cost = db.session.get(CostEntry, cost_id)
    if not cost or cost.project_id != project_id:
        return jsonify({"error": "Cost not found"}), 404

    db.session.delete(cost)
    db.session.commit()
    return "", 204
