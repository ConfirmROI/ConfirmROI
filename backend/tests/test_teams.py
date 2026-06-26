import pytest
from tests.conftest import enterpriseskip


@enterpriseskip
class TestTeamCreation:
    def test_create_team_success(self, client, auth_headers, auth_user):
        resp = client.post("/api/teams", headers=auth_headers, json={
            "name": "Engineering Team",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Engineering Team"
        assert data["manager_user_id"] == auth_user
        assert data["parent_team_id"] is None

    def test_create_team_no_auth(self, client):
        resp = client.post("/api/teams", json={"name": "Team"})
        assert resp.status_code == 401

    def test_create_team_missing_name(self, client, auth_headers):
        resp = client.post("/api/teams", headers=auth_headers, json={})
        assert resp.status_code == 400

    def test_create_second_team_free_tier(self, client, auth_headers):
        client.post("/api/teams", headers=auth_headers, json={"name": "First Team"})
        resp = client.post("/api/teams", headers=auth_headers, json={"name": "Second Team"})
        assert resp.status_code == 403
        assert "free tier" in resp.get_json()["error"].lower()


@enterpriseskip
class TestTeamRetrieval:
    def test_get_team(self, client, auth_headers, auth_user):
        create = client.post("/api/teams", headers=auth_headers, json={"name": "My Team"})
        team_id = create.get_json()["id"]
        resp = client.get(f"/api/teams/{team_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "My Team"

    def test_list_teams(self, client, auth_headers):
        client.post("/api/teams", headers=auth_headers, json={"name": "Team A"})
        resp = client.get("/api/teams", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "Team A"

    def test_get_nonexistent_team(self, client, auth_headers):
        resp = client.get("/api/teams/9999", headers=auth_headers)
        assert resp.status_code == 404


@enterpriseskip
class TestTeamUpdate:
    def test_update_team_name(self, client, auth_headers):
        create = client.post("/api/teams", headers=auth_headers, json={"name": "Old Name"})
        team_id = create.get_json()["id"]
        resp = client.put(f"/api/teams/{team_id}", headers=auth_headers, json={"name": "New Name"})
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "New Name"


@enterpriseskip
class TestTeamDelete:
    def test_delete_team(self, client, auth_headers):
        create = client.post("/api/teams", headers=auth_headers, json={"name": "Delete Me"})
        team_id = create.get_json()["id"]
        resp = client.delete(f"/api/teams/{team_id}", headers=auth_headers)
        assert resp.status_code == 204
        resp2 = client.get(f"/api/teams/{team_id}", headers=auth_headers)
        assert resp2.status_code == 404
