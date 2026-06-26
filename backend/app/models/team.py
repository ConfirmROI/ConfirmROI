from enum import Enum as PyEnum

from app.extensions import db


class TeamMemberRole(PyEnum):
    member = "member"
    manager = "manager"


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    manager_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    avg_labor_cost_per_week = db.Column(db.Numeric(12, 2), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    manager = db.relationship("User", backref="managed_teams", foreign_keys=[manager_user_id])
    parent_team = db.relationship("Team", remote_side="Team.id", backref="sub_teams")
    members = db.relationship("TeamMember", backref="team", lazy=True, cascade="all, delete-orphan")
    projects = db.relationship("Project", backref="team", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manager_user_id": self.manager_user_id,
            "manager_name": self.manager.name if self.manager else None,
            "parent_team_id": self.parent_team_id,
            "avg_labor_cost_per_week": float(self.avg_labor_cost_per_week) if self.avg_labor_cost_per_week is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.Enum(TeamMemberRole), default=TeamMemberRole.member, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "role": self.role.value if self.role else "member",
        }
