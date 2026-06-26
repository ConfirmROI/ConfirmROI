import pytest

from app.extensions import db
from app.models import User, UserRole, UserTier, Team, TeamMember, TeamMemberRole, Project, CostEntry, CostCategory


@pytest.fixture
def setup_project(app, auth_user):
    with app.app_context():
        team = Team(name="Test Team", manager_user_id=auth_user)
        db.session.add(team)
        db.session.flush()
        db.session.add(TeamMember(team_id=team.id, user_id=auth_user, role=TeamMemberRole.manager))
        db.session.commit()
        team_id = team.id

        project = Project(team_id=team_id, name="Test Project")
        db.session.add(project)
        db.session.flush()

        dev_cost = CostEntry(
            project_id=project.id,
            category=CostCategory.development,
            description="Development (labor)",
            person_weeks=0,
            amount=0,
        )
        db.session.add(dev_cost)
        db.session.commit()
        project_id = project.id
        return team_id, project_id


class TestCostsAPI:
    def test_list_costs(self, client, auth_headers, setup_project):
        _, project_id = setup_project
        resp = client.get(f"/api/projects/{project_id}/costs", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["category"] == "development"

    def test_create_development_cost(self, client, auth_headers, setup_project):
        _, project_id = setup_project
        resp = client.post(
            f"/api/projects/{project_id}/costs",
            json={"category": "development", "person_weeks": 10},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["category"] == "development"
        assert data["person_weeks"] == 10
        assert data["amount"] == 10 * 3500.0
        assert data["effective_rate"] == 3500.0

    def test_create_non_development_cost(self, client, auth_headers, setup_project):
        _, project_id = setup_project
        resp = client.post(
            f"/api/projects/{project_id}/costs",
            json={"category": "infrastructure", "amount": 5000, "description": "AWS hosting"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["category"] == "infrastructure"
        assert data["amount"] == 5000
        assert data["person_weeks"] is None

    def test_update_cost_person_weeks(self, client, auth_headers, setup_project):
        _, project_id = setup_project
        resp = client.get(f"/api/projects/{project_id}/costs", headers=auth_headers)
        cost_id = resp.get_json()[0]["id"]

        resp = client.put(
            f"/api/projects/{project_id}/costs/{cost_id}",
            json={"person_weeks": 8},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["person_weeks"] == 8
        assert data["amount"] == 8 * 3500.0

    def test_delete_cost(self, client, auth_headers, setup_project):
        _, project_id = setup_project
        resp = client.get(f"/api/projects/{project_id}/costs", headers=auth_headers)
        cost_id = resp.get_json()[0]["id"]

        resp = client.delete(
            f"/api/projects/{project_id}/costs/{cost_id}",
            headers=auth_headers,
        )
        assert resp.status_code == 204

        resp = client.get(f"/api/projects/{project_id}/costs", headers=auth_headers)
        assert len(resp.get_json()) == 0

    def test_team_labor_rate_overrides_default(self, client, auth_headers, setup_project):
        team_id, project_id = setup_project
        with client.application.app_context():
            team = db.session.get(Team, team_id)
            team.avg_labor_cost_per_week = 5000
            db.session.commit()

        resp = client.post(
            f"/api/projects/{project_id}/costs",
            json={"category": "development", "person_weeks": 4},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["effective_rate"] == 5000.0
        assert data["amount"] == 20000.0

    def test_project_creation_auto_creates_development_cost(self, client, auth_headers, setup_project):
        team_id, _ = setup_project
        resp = client.post(
            "/api/projects",
            json={"team_id": team_id, "name": "New Project"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        project_id = resp.get_json()["id"]

        resp = client.get(f"/api/projects/{project_id}/costs", headers=auth_headers)
        assert resp.status_code == 200
        costs = resp.get_json()
        assert len(costs) == 1
        assert costs[0]["category"] == "development"
