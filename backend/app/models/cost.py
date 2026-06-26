from enum import Enum as PyEnum

from app.extensions import db


class CostCategory(PyEnum):
    development = "development"
    infrastructure = "infrastructure"
    vendor = "vendor"
    other = "other"


class CostType(PyEnum):
    one_time = "one_time"
    recurring_monthly = "recurring_monthly"
    recurring_annual = "recurring_annual"


SYSTEM_DEFAULT_LABOR_RATE = 3500.00


class CostEntry(db.Model):
    __tablename__ = "cost_entries"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    category = db.Column(db.Enum(CostCategory), default=CostCategory.development, nullable=False)
    description = db.Column(db.String(255))
    person_weeks = db.Column(db.Numeric(10, 2), nullable=True)
    amount = db.Column(db.Numeric(20, 4), nullable=False, default=0)
    cost_type = db.Column(db.Enum(CostType), default=CostType.one_time, nullable=False)
    incurred_date = db.Column(db.Date, nullable=True)
    is_estimate = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    project = db.relationship("Project", backref=db.backref("cost_entries", cascade="all, delete-orphan"), lazy=True)

    def resolve_labor_rate(self):
        if self.category != CostCategory.development:
            return None
        team = self.project.team if self.project else None
        if team and team.avg_labor_cost_per_week is not None:
            return float(team.avg_labor_cost_per_week)
        if team and team.manager:
            manager = team.manager
            if manager.default_labor_cost_per_week is not None:
                return float(manager.default_labor_cost_per_week)
        return SYSTEM_DEFAULT_LABOR_RATE

    def recompute_amount(self):
        if self.category == CostCategory.development and self.person_weeks is not None:
            rate = self.resolve_labor_rate()
            self.amount = float(self.person_weeks) * rate

    def to_dict(self):
        rate = self.resolve_labor_rate() if self.category == CostCategory.development else None
        return {
            "id": self.id,
            "project_id": self.project_id,
            "category": self.category.value if self.category else "development",
            "description": self.description,
            "person_weeks": float(self.person_weeks) if self.person_weeks is not None else None,
            "amount": float(self.amount) if self.amount is not None else 0,
            "cost_type": self.cost_type.value if self.cost_type else "one_time",
            "incurred_date": self.incurred_date.isoformat() if self.incurred_date else None,
            "is_estimate": self.is_estimate,
            "effective_rate": rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
