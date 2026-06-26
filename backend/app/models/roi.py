from app.extensions import db


class RoiCalculation(db.Model):
    __tablename__ = "roi_calculations"

    id = db.Column(db.Integer, primary_key=True)
    project_formula_id = db.Column(db.Integer, db.ForeignKey("project_formulas.id"), nullable=False)
    roi_value = db.Column(db.Numeric(20, 4), nullable=False)
    roi_value_3yr = db.Column(db.Numeric(20, 4), nullable=True)
    calculated_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "project_formula_id": self.project_formula_id,
            "roi_value": float(self.roi_value) if self.roi_value is not None else 0,
            "roi_value_3yr": float(self.roi_value_3yr) if self.roi_value_3yr is not None else 0,
            "calculated_at": self.calculated_at.isoformat() if self.calculated_at else None,
        }
