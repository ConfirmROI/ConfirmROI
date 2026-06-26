import os
import sys

from app import create_app
from app.extensions import db
from app.models.user import User, UserRole, UserTier
from app.models.user_identity import UserIdentity
from app.models.team import Team, TeamMember, TeamMemberRole
from app.models.project import Project, ProjectStatus, ExternalSource
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    AssumptionDataType,
    FormulaAssumption,
    ProjectFormula,
    ProjectAssumptionValue,
)
from app.models.cost import CostEntry, CostCategory, CostType
from app.services.auth_service import LocalAuthProvider
from app.services.formula_service import RoiService
from app.services.seed import seed_formulas

from app.services.demo_data import (
    DEMO_DATA_VERSION,
    DEMO_PASSWORD,
    DEMO_USERS,
    DEMO_TEAMS_FREE,
    DEMO_TEAMS_PAID,
    DEMO_TEAM_MEMBERS_FREE,
    DEMO_TEAM_MEMBERS_PAID,
    DEMO_PROJECTS_FREE,
    DEMO_PROJECTS_PAID,
    DEMO_CUSTOM_ASSUMPTIONS_FREE,
    DEMO_CUSTOM_ASSUMPTIONS_PAID,
    DEMO_CUSTOM_FORMULAS_FREE,
    DEMO_CUSTOM_FORMULAS_PAID,
)

MERIDIAN_DOMAIN = "@meridian.dev"


def _demo_data_exists():
    return User.query.filter(User.email.like(f"%{MERIDIAN_DOMAIN}")).first() is not None


def _reset_demo_data():
    print("Resetting existing demo data...")
    conn = db.session.connection()

    user_ids = conn.execute(
        db.text(f"SELECT id FROM users WHERE email LIKE :domain"),
        {"domain": f"%{MERIDIAN_DOMAIN}"},
    ).fetchall()
    user_ids = [r[0] for r in user_ids]
    if not user_ids:
        print("No demo data found to reset.")
        return

    user_id_params = ",".join(str(i) for i in user_ids)

    team_ids = conn.execute(
        db.text(f"SELECT id FROM teams WHERE manager_user_id IN ({user_id_params})")
    ).fetchall()
    team_ids = [r[0] for r in team_ids]

    if team_ids:
        team_id_params = ",".join(str(i) for i in team_ids)

        proj_ids = conn.execute(
            db.text(f"SELECT id FROM projects WHERE team_id IN ({team_id_params})")
        ).fetchall()
        proj_ids = [r[0] for r in proj_ids]

        if proj_ids:
            proj_id_params = ",".join(str(i) for i in proj_ids)

            pa_ids = conn.execute(
                db.text(f"SELECT id FROM project_formulas WHERE project_id IN ({proj_id_params})")
            ).fetchall()
            pa_ids = [r[0] for r in pa_ids]

            if pa_ids:
                pa_id_params = ",".join(str(i) for i in pa_ids)
                conn.execute(db.text(f"DELETE FROM roi_calculations WHERE project_formula_id IN ({pa_id_params})"))
                conn.execute(db.text(f"DELETE FROM project_assumption_values WHERE project_formula_id IN ({pa_id_params})"))
                conn.execute(db.text(f"DELETE FROM project_formulas WHERE id IN ({pa_id_params})"))

            conn.execute(db.text(f"DELETE FROM cost_entries WHERE project_id IN ({proj_id_params})"))
            conn.execute(db.text(f"DELETE FROM projects WHERE id IN ({proj_id_params})"))

        conn.execute(db.text(f"DELETE FROM team_members WHERE team_id IN ({team_id_params})"))
        conn.execute(db.text(f"DELETE FROM teams WHERE id IN ({team_id_params})"))

    conn.execute(db.text(f"DELETE FROM user_identities WHERE user_id IN ({user_id_params})"))
    conn.execute(db.text(f"DELETE FROM value_formulas WHERE is_system = FALSE AND user_id IN ({user_id_params})"))
    conn.execute(db.text(f"DELETE FROM value_assumptions WHERE is_system = FALSE AND user_id IN ({user_id_params})"))
    conn.execute(db.text(f"DELETE FROM users WHERE id IN ({user_id_params})"))

    db.session.commit()
    db.session.expire_all()
    print(f"Deleted {len(user_ids)} demo user(s), {len(team_ids)} team(s), and all related data.")


def _seed_users(tier: str) -> dict:
    user_map = {}
    for u in DEMO_USERS:
        role_str = u[f"{tier}_role"]
        tier_str = u[f"{tier}_tier"]
        if role_str is None:
            continue

        existing = User.query.filter_by(email=u["email"]).first()
        if existing:
            user_map[u["email"]] = existing
            continue

        user = User(
            email=u["email"],
            name=u["name"],
            password_hash=LocalAuthProvider.hash_password(DEMO_PASSWORD),
            role=UserRole(role_str),
            tier=UserTier(tier_str),
        )
        db.session.add(user)
        db.session.flush()

        identity = UserIdentity(
            user_id=user.id,
            provider="local",
            provider_user_id=u["email"],
        )
        db.session.add(identity)
        db.session.flush()

        user_map[u["email"]] = user

    db.session.flush()
    return user_map


def _seed_teams(tier: str, user_map: dict) -> dict:
    team_defs = DEMO_TEAMS_FREE if tier == "free" else DEMO_TEAMS_PAID
    team_map = {}

    for t in team_defs:
        manager = user_map.get(t["manager_email"])
        if not manager:
            continue

        existing = Team.query.filter_by(name=t["name"], manager_user_id=manager.id).first()
        if existing:
            team_map[t["name"]] = existing
            continue

        team = Team(
            name=t["name"],
            manager_user_id=manager.id,
            parent_team_id=None,
        )
        db.session.add(team)
        db.session.flush()
        team_map[t["name"]] = team

    db.session.flush()

    for t in team_defs:
        if t["parent_name"] and t["name"] in team_map and t["parent_name"] in team_map:
            child = team_map[t["name"]]
            if child.parent_team_id is None:
                child.parent_team_id = team_map[t["parent_name"]].id

    db.session.flush()

    for team_name, team in team_map.items():
        manager_email = next(
            (t["manager_email"] for t in (DEMO_TEAMS_FREE if tier == "free" else DEMO_TEAMS_PAID)
             if t["name"] == team_name),
            None,
        )
        if not manager_email:
            continue
        manager = user_map.get(manager_email)
        if not manager:
            continue

        existing_mgr = TeamMember.query.filter_by(
            team_id=team.id, user_id=manager.id
        ).first()
        if not existing_mgr:
            db.session.add(TeamMember(
                team_id=team.id,
                user_id=manager.id,
                role=TeamMemberRole.manager,
            ))

    db.session.flush()
    return team_map


def _seed_team_members(tier: str, user_map: dict, team_map: dict):
    member_defs = DEMO_TEAM_MEMBERS_FREE if tier == "free" else DEMO_TEAM_MEMBERS_PAID
    for m in member_defs:
        team = team_map.get(m["team_name"])
        user = user_map.get(m["member_email"])
        if not team or not user:
            continue

        existing = TeamMember.query.filter_by(team_id=team.id, user_id=user.id).first()
        if not existing:
            db.session.add(TeamMember(
                team_id=team.id,
                user_id=user.id,
                role=TeamMemberRole.member,
            ))

    db.session.flush()


def _seed_custom_assumptions(tier: str, user_map: dict) -> dict:
    assumption_defs = DEMO_CUSTOM_ASSUMPTIONS_FREE if tier == "free" else DEMO_CUSTOM_ASSUMPTIONS_PAID
    custom_assumption_map = {}

    for a in assumption_defs:
        owner = user_map.get(a["owner_email"])
        if not owner:
            continue

        existing = ValueAssumption.query.filter_by(
            key=a["key"], is_system=False, user_id=owner.id
        ).first()
        if existing:
            custom_assumption_map[a["key"]] = existing
            continue

        assumption = ValueAssumption(
            key=a["key"],
            label=a["label"],
            data_type=AssumptionDataType(a["data_type"]),
            default_value=a["default_value"],
            description=a["description"],
            is_system=False,
            user_id=owner.id,
        )
        db.session.add(assumption)
        db.session.flush()
        custom_assumption_map[a["key"]] = assumption

    db.session.flush()
    return custom_assumption_map


def _seed_custom_formulas(tier: str, user_map: dict):
    formula_defs = DEMO_CUSTOM_FORMULAS_FREE if tier == "free" else DEMO_CUSTOM_FORMULAS_PAID

    for arch_data in formula_defs:
        owner = user_map.get(arch_data["owner_email"])
        if not owner:
            continue

        existing = ValueFormula.query.filter_by(
            name=arch_data["name"], is_system=False, user_id=owner.id
        ).first()
        if existing:
            continue

        arch = ValueFormula(
            name=arch_data["name"],
            description=arch_data["description"],
            formula=arch_data["formula"],
            is_system=False,
            user_id=owner.id,
        )
        db.session.add(arch)
        db.session.flush()

        for i, key in enumerate(arch_data["assumption_keys"]):
            assumption = ValueAssumption.query.filter_by(key=key, is_system=True).first()
            if not assumption:
                assumption = ValueAssumption.query.filter_by(key=key, user_id=owner.id).first()
            if assumption:
                db.session.add(FormulaAssumption(
                    formula_id=arch.id,
                    assumption_id=assumption.id,
                    sort_order=i,
                ))

    db.session.flush()


def _seed_projects(tier: str, team_map: dict):
    project_defs = DEMO_PROJECTS_FREE if tier == "free" else DEMO_PROJECTS_PAID
    project_map = {}

    for p in project_defs:
        team = team_map.get(p["team_name"])
        if not team:
            continue

        existing = Project.query.filter_by(name=p["name"], team_id=team.id).first()
        if existing:
            project_map[p["name"]] = existing
            continue

        project = Project(
            team_id=team.id,
            name=p["name"],
            description=p["description"],
            external_id=p.get("external_id"),
            external_source=ExternalSource(p["external_source"]),
            status=ProjectStatus(p["status"]),
            start_date=p.get("start_date"),
            end_date=p.get("end_date"),
        )
        db.session.add(project)
        db.session.flush()
        project_map[p["name"]] = project

    db.session.flush()
    return project_map


def _seed_project_formulas(tier: str, project_map: dict):
    project_defs = DEMO_PROJECTS_FREE if tier == "free" else DEMO_PROJECTS_PAID

    for p in project_defs:
        project = project_map.get(p["name"])
        if not project:
            continue

        for arch_def in p["formulas"]:
            formula = ValueFormula.query.filter_by(
                name=arch_def["formula_name"], is_system=True
            ).first()
            if not formula:
                continue

            existing_pa = ProjectFormula.query.filter_by(
                project_id=project.id, formula_id=formula.id
            ).first()
            if existing_pa:
                continue

            pa = ProjectFormula(
                project_id=project.id,
                formula_id=formula.id,
            )
            db.session.add(pa)
            db.session.flush()

            for key, value in arch_def["assumption_overrides"].items():
                assumption = ValueAssumption.query.filter_by(key=key, is_system=True).first()
                if not assumption:
                    continue

                db.session.add(ProjectAssumptionValue(
                    project_formula_id=pa.id,
                    assumption_id=assumption.id,
                    value=value,
                ))

            db.session.flush()
            RoiService.calculate_roi(pa.id)


def _seed_project_costs(tier: str, project_map: dict):
    project_defs = DEMO_PROJECTS_FREE if tier == "free" else DEMO_PROJECTS_PAID

    for p in project_defs:
        project = project_map.get(p["name"])
        if not project:
            continue

        existing = CostEntry.query.filter_by(project_id=project.id).first()
        if existing:
            continue

        impl_cost = 0
        for arch_def in p["formulas"]:
            impl_cost += arch_def["assumption_overrides"].get("implementation_cost", 0)

        person_weeks = max(1, round(impl_cost / 3500)) if impl_cost > 0 else 4

        dev_cost = CostEntry(
            project_id=project.id,
            category=CostCategory.development,
            description="Development (labor)",
            person_weeks=person_weeks,
        )
        dev_cost.recompute_amount()
        db.session.add(dev_cost)

        for c in p.get("costs", []):
            extra_cost = CostEntry(
                project_id=project.id,
                category=CostCategory(c["category"]),
                description=c["description"],
                amount=c["amount"],
                cost_type=CostType(c["cost_type"]),
                is_estimate=True,
            )
            db.session.add(extra_cost)

    db.session.flush()


def seed_demo(tier: str, reset: bool = False):
    if _demo_data_exists():
        if reset:
            _reset_demo_data()
        else:
            print(f"Demo data (v{DEMO_DATA_VERSION}) already exists. Use --reset to recreate.")
            _print_summary(tier)
            return

    print(f"Seeding demo data for tier='{tier}' (v{DEMO_DATA_VERSION})...")

    seed_formulas()

    user_map = _seed_users(tier)
    print(f"  Users:       {len(user_map)}")

    team_map = _seed_teams(tier, user_map)
    print(f"  Teams:       {len(team_map)}")

    _seed_team_members(tier, user_map, team_map)

    _seed_custom_assumptions(tier, user_map)
    _seed_custom_formulas(tier, user_map)

    project_map = _seed_projects(tier, team_map)
    print(f"  Projects:    {len(project_map)}")

    _seed_project_formulas(tier, project_map)
    _seed_project_costs(tier, project_map)

    db.session.commit()
    print("Demo data seeded successfully.")
    _print_summary(tier)


def _print_summary(tier: str):
    url = "http://localhost:5174" if tier == "free" else "http://localhost:5175"
    print("")
    print("=" * 55)
    print(f" Demo Environment: {tier.upper()}-TIER")
    print(f" URL: {url}")
    print("-" * 55)
    print(f" Email:    sarah.chen@meridian.dev")
    print(f" Password: {DEMO_PASSWORD}")
    print(" (All 6-8 demo users share the same password)")
    print("=" * 55)


if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    tier = os.environ.get("DEMO_TIER", "free")
    app = create_app()
    with app.app_context():
        seed_demo(tier, reset=reset_flag)
