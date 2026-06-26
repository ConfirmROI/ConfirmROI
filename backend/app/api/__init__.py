from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.api.auth import auth_bp
from app.api.projects import projects_bp
from app.api.value_formulas import formulas_bp
from app.api.assumptions import assumptions_bp
from app.api.dashboard import dashboard_bp
from app.api.costs import costs_bp

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(projects_bp, url_prefix="/projects")
api_bp.register_blueprint(formulas_bp, url_prefix="/formulas")
api_bp.register_blueprint(assumptions_bp)
api_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
api_bp.register_blueprint(costs_bp)
