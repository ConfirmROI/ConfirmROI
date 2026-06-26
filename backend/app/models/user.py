from datetime import datetime, date
from enum import Enum as PyEnum

from app.extensions import db


class UserRole(PyEnum):
    user = "user"
    admin = "admin"


class UserTier(PyEnum):
    free = "free"
    paid = "paid"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    tier = db.Column(db.Enum(UserTier), default=UserTier.free, nullable=False)
    default_labor_cost_per_week = db.Column(db.Numeric(12, 2), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    identities = db.relationship("UserIdentity", backref="user", lazy=True)
    teams = db.relationship("TeamMember", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value if self.role else "user",
            "tier": self.tier.value if self.tier else "free",
            "default_labor_cost_per_week": float(self.default_labor_cost_per_week) if self.default_labor_cost_per_week is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
