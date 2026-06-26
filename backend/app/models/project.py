from enum import Enum as PyEnum

from app.extensions import db


class ExternalSource(PyEnum):
    manual = "manual"
    csv = "csv"
    jira = "jira"


class ProjectStatus(PyEnum):
    planning = "planning"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    external_id = db.Column(db.String(255))
    external_source = db.Column(db.Enum(ExternalSource), default=ExternalSource.manual, nullable=False)
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.planning, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    formulas = db.relationship("ProjectFormula", backref="project", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "external_id": self.external_id,
            "external_source": self.external_source.value if self.external_source else "manual",
            "status": self.status.value if self.status else "planning",
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
