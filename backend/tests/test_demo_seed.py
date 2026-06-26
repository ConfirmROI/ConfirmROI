import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models.user import User
from app.models.team import Team, TeamMember
from app.models.project import Project
from app.models.value_formula import ProjectFormula, ValueFormula, ValueAssumption
from app.models.roi import RoiCalculation
from app.services.demo_seed import seed_demo, _demo_data_exists, _reset_demo_data, MERIDIAN_DOMAIN


@pytest.fixture
def demo_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestDemoSeedFree:
    def test_seed_free_creates_users(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            users = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).all()
            assert len(users) >= 6

    def test_seed_free_user_tiers(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            users = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).all()
            for u in users:
                assert u.tier.value == "free"

    def test_seed_free_creates_teams(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            teams = (
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            )
            assert len(teams) >= 6

    def test_seed_free_team_hierarchy_flat(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            teams = (
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            )
            for team in teams:
                assert team.parent_team_id is None

    def test_seed_free_creates_projects(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            meridian_team_ids = [
                t.id for t in
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            ]
            projects = Project.query.filter(Project.team_id.in_(meridian_team_ids)).all()
            assert len(projects) >= 8

    def test_seed_free_roi_calculations_exist(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            meridian_team_ids = [
                t.id for t in
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            ]
            project_ids = [
                p.id for p in
                Project.query.filter(Project.team_id.in_(meridian_team_ids)).all()
            ]
            pa_ids = [
                pa.id for pa in
                ProjectFormula.query.filter(ProjectFormula.project_id.in_(project_ids)).all()
            ]
            roi_calcs = RoiCalculation.query.filter(
                RoiCalculation.project_formula_id.in_(pa_ids)
            ).all()
            assert len(roi_calcs) >= 8

    def test_seed_free_team_members_populated(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            meridian_user_ids = [
                u.id for u in
                User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).all()
            ]
            memberships = TeamMember.query.filter(
                TeamMember.user_id.in_(meridian_user_ids)
            ).all()
            assert len(memberships) >= 6


class TestDemoSeedPaid:
    def test_seed_paid_creates_users(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            users = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).all()
            assert len(users) >= 8

    def test_seed_paid_user_tiers(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            users = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).all()
            for u in users:
                assert u.tier.value == "paid"

    def test_seed_paid_creates_teams(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            teams = (
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            )
            assert len(teams) >= 8

    def test_seed_paid_team_hierarchy_exists(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            teams_with_parent = (
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(
                    User.email.like(f"%{MERIDIAN_DOMAIN}"),
                    Team.parent_team_id.isnot(None),
                )
                .all()
            )
            assert len(teams_with_parent) >= 5

    def test_seed_paid_creates_projects(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            meridian_team_ids = [
                t.id for t in
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            ]
            projects = Project.query.filter(Project.team_id.in_(meridian_team_ids)).all()
            assert len(projects) >= 8

    def test_seed_paid_roi_calculations_exist(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            meridian_team_ids = [
                t.id for t in
                Team.query
                .join(User, Team.manager_user_id == User.id)
                .filter(User.email.like(f"%{MERIDIAN_DOMAIN}"))
                .all()
            ]
            project_ids = [
                p.id for p in
                Project.query.filter(Project.team_id.in_(meridian_team_ids)).all()
            ]
            pa_ids = [
                pa.id for pa in
                ProjectFormula.query.filter(ProjectFormula.project_id.in_(project_ids)).all()
            ]
            roi_calcs = RoiCalculation.query.filter(
                RoiCalculation.project_formula_id.in_(pa_ids)
            ).all()
            assert len(roi_calcs) >= 8

    def test_seed_paid_admin_user_exists(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            from app.models.user import UserRole
            admins = User.query.filter(
                User.email.like(f"%{MERIDIAN_DOMAIN}"),
                User.role == UserRole.admin,
            ).all()
            assert len(admins) >= 1


class TestDemoSeedIdempotent:
    def test_seed_is_idempotent(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            user_count_1 = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).count()

            seed_demo("free")
            user_count_2 = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).count()

            assert user_count_1 == user_count_2

    def test_reset_clears_demo_data(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            assert _demo_data_exists()

            _reset_demo_data()
            assert not _demo_data_exists()

    def test_reset_flag_recreates_data(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            count_before = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).count()

            seed_demo("free", reset=True)
            count_after = User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).count()

            assert count_after == count_before


class TestDemoCustomData:
    def test_custom_formulas_created_free(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            custom_formulas = ValueFormula.query.filter_by(is_system=False).all()
            assert len(custom_formulas) >= 2
            names = [a.name for a in custom_formulas]
            assert "Developer Productivity" in names

    def test_custom_assumptions_created_free(self, demo_app):
        with demo_app.app_context():
            seed_demo("free")
            custom_assumptions = ValueAssumption.query.filter_by(is_system=False).all()
            assert len(custom_assumptions) >= 3
            keys = [a.key for a in custom_assumptions]
            assert "onboarding_time_saved_days" in keys

    def test_custom_formulas_created_paid(self, demo_app):
        with demo_app.app_context():
            seed_demo("paid")
            custom_formulas = ValueFormula.query.filter_by(is_system=False).all()
            assert len(custom_formulas) >= 2
            names = [a.name for a in custom_formulas]
            assert "Compliance Fine Avoidance" in names
