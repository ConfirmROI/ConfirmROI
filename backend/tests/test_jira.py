import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from app.extensions import db
from app.models.project import Project, ExternalSource
from tests.conftest import enterpriseskip

try:
    from confirmroi_enterprise.models.jira_connection import JiraConnection
    from confirmroi_enterprise.api.jira import JiraService
except ImportError:
    JiraConnection = None
    JiraService = None


@pytest.fixture
def team_id(client, auth_headers):
    team = client.post("/api/teams", headers=auth_headers, json={"name": "Jira Team"})
    return team.get_json()["id"]


@pytest.fixture
def jira_connection(app, team_id):
    with app.app_context():
        conn = JiraConnection(
            team_id=team_id,
            base_url="https://test.atlassian.net",
            api_token="test-token",
            email="test@example.com",
        )
        db.session.add(conn)
        db.session.commit()
        return conn.id


@enterpriseskip
class TestJiraService:
    def test_create_connection(self, app, team_id):
        with app.app_context():
            conn = JiraService.create_connection(
                team_id=team_id,
                base_url="https://company.atlassian.net",
                api_token="my-token",
                email="user@company.com",
            )
            assert conn.id is not None
            assert conn.base_url == "https://company.atlassian.net"
            assert conn.email == "user@company.com"

    def test_get_connection(self, app, jira_connection):
        with app.app_context():
            conn = JiraService.get_connection(jira_connection)
            assert conn is not None
            assert conn.base_url == "https://test.atlassian.net"

    def test_get_connection_not_found(self, app):
        with app.app_context():
            conn = JiraService.get_connection(9999)
            assert conn is None

    def test_delete_connection(self, app, jira_connection):
        with app.app_context():
            JiraService.delete_connection(jira_connection)
            conn = JiraService.get_connection(jira_connection)
            assert conn is None

    @patch("confirmroi_enterprise.api.jira.requests.get")
    def test_fetch_projects_from_jira(self, mock_get, app, jira_connection, team_id):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"key": "PROJ1", "name": "Project One"},
            {"key": "PROJ2", "name": "Project Two"},
        ]
        mock_get.return_value = mock_response

        with app.app_context():
            projects = JiraService.fetch_projects(jira_connection)
            assert len(projects) == 2
            assert projects[0]["key"] == "PROJ1"
            assert projects[1]["name"] == "Project Two"

    @patch("confirmroi_enterprise.api.jira.requests.get")
    def test_fetch_projects_api_error(self, mock_get, app, jira_connection):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        with app.app_context():
            with pytest.raises(Exception):
                JiraService.fetch_projects(jira_connection)

    @patch("confirmroi_enterprise.api.jira.requests.get")
    def test_import_jira_projects(self, mock_get, app, jira_connection, team_id):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"key": "JIRA1", "name": "Jira Project 1"},
            {"key": "JIRA2", "name": "Jira Project 2"},
        ]
        mock_get.return_value = mock_response

        with app.app_context():
            result = JiraService.import_projects(jira_connection, team_id)
            assert result["imported"] == 2
            assert result["errors"] == []

            projects = Project.query.filter_by(team_id=team_id).all()
            assert len(projects) == 2
            assert projects[0].external_source == ExternalSource.jira
            assert projects[0].external_id == "JIRA1"
            assert projects[1].external_id == "JIRA2"


@enterpriseskip
class TestJiraConnectionAPI:
    def test_create_jira_connection_endpoint(self, client, auth_headers, team_id):
        resp = client.post(
            f"/api/teams/{team_id}/jira",
            headers=auth_headers,
            json={
                "base_url": "https://company.atlassian.net",
                "api_token": "my-token",
                "email": "user@company.com",
            },
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["base_url"] == "https://company.atlassian.net"

    def test_create_jira_connection_no_auth(self, client, team_id):
        resp = client.post(
            f"/api/teams/{team_id}/jira",
            json={"base_url": "https://test.atlassian.net", "api_token": "t", "email": "e@e.com"},
        )
        assert resp.status_code == 401

    def test_get_jira_connection_endpoint(self, client, auth_headers, team_id, jira_connection):
        resp = client.get(f"/api/teams/{team_id}/jira", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["base_url"] == "https://test.atlassian.net"

    def test_delete_jira_connection_endpoint(self, client, auth_headers, team_id, jira_connection):
        resp = client.delete(f"/api/teams/{team_id}/jira", headers=auth_headers)
        assert resp.status_code == 204

    @patch("confirmroi_enterprise.api.jira.requests.get")
    def test_import_jira_projects_endpoint(self, mock_get, client, auth_headers, team_id, jira_connection):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"key": "API1", "name": "API Project"},
        ]
        mock_get.return_value = mock_response

        resp = client.post(f"/api/teams/{team_id}/jira/import", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["imported"] == 1
