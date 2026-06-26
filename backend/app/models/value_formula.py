from enum import Enum as PyEnum

from app.extensions import db


class AssumptionDataType(PyEnum):
    number = "number"
    currency = "currency"
    percentage = "percentage"


class FormulaAssumption(db.Model):
    __tablename__ = "formula_assumptions"

    id = db.Column(db.Integer, primary_key=True)
    formula_id = db.Column(db.Integer, db.ForeignKey("value_formulas.id"), nullable=False)
    assumption_id = db.Column(db.Integer, db.ForeignKey("value_assumptions.id"), nullable=False)
    sort_order = db.Column(db.Integer, default=0)


class ValueFormula(db.Model):
    __tablename__ = "value_formulas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    formula = db.Column(db.Text, nullable=False)
    is_system = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    assumptions = db.relationship(
        "ValueAssumption",
        secondary="formula_assumptions",
        lazy=True,
        order_by="FormulaAssumption.sort_order",
    )
    project_formulas = db.relationship("ProjectFormula", backref="formula", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "formula": self.formula,
            "is_system": self.is_system,
            "user_id": self.user_id,
            "assumptions": [a.to_dict() for a in self.assumptions] if self.assumptions else [],
        }


class ValueAssumption(db.Model):
    __tablename__ = "value_assumptions"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    data_type = db.Column(db.Enum(AssumptionDataType), default=AssumptionDataType.number, nullable=False)
    default_value = db.Column(db.Numeric(20, 4), nullable=False, default=0)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_system = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    formulas = db.relationship(
        "ValueFormula",
        secondary="formula_assumptions",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "label": self.label,
            "data_type": self.data_type.value if self.data_type else "number",
            "default_value": float(self.default_value) if self.default_value is not None else 0,
            "description": self.description,
            "sort_order": self.sort_order,
            "is_system": self.is_system,
            "user_id": self.user_id,
        }


class ProjectFormula(db.Model):
    __tablename__ = "project_formulas"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    formula_id = db.Column(db.Integer, db.ForeignKey("value_formulas.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    assumption_values = db.relationship(
        "ProjectAssumptionValue", backref="project_formula", lazy=True, cascade="all, delete-orphan"
    )
    roi_calculations = db.relationship(
        "RoiCalculation", backref="project_formula", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "formula_id": self.formula_id,
            "formula": self.formula.to_dict() if self.formula else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "assumption_values": [av.to_dict() for av in self.assumption_values] if self.assumption_values else [],
        }


class ProjectAssumptionValue(db.Model):
    __tablename__ = "project_assumption_values"

    id = db.Column(db.Integer, primary_key=True)
    project_formula_id = db.Column(db.Integer, db.ForeignKey("project_formulas.id"), nullable=False)
    assumption_id = db.Column(db.Integer, db.ForeignKey("value_assumptions.id"), nullable=False)
    value = db.Column(db.Numeric(20, 4), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    assumption = db.relationship("ValueAssumption", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "project_formula_id": self.project_formula_id,
            "assumption_id": self.assumption_id,
            "value": float(self.value) if self.value is not None else 0,
            "assumption": self.assumption.to_dict() if self.assumption else None,
        }
