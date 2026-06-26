import pytest


class TestProjectCreation:
    def test_create_project_success(self, client, auth_headers, team_id):
        resp = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id,
            "name": "Migration Project",
            "description": "Migrate to new infrastructure",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Migration Project"
        assert data["description"] == "Migrate to new infrastructure"
        assert data["status"] == "planning"
        assert data["external_source"] == "manual"

    def test_create_project_no_auth(self, client, team_id):
        resp = client.post("/api/projects", json={
            "team_id": team_id,
            "name": "Project",
        })
        assert resp.status_code == 401

    def test_create_project_missing_name(self, client, auth_headers, team_id):
        resp = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id,
        })
        assert resp.status_code == 400

    def test_create_project_with_dates(self, client, auth_headers, team_id):
        resp = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id,
            "name": "Dated Project",
            "start_date": "2024-01-15",
            "end_date": "2024-06-30",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["start_date"] == "2024-01-15"
        assert data["end_date"] == "2024-06-30"


class TestProjectRetrieval:
    def test_get_project(self, client, auth_headers, team_id):
        create = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Get Me",
        })
        pid = create.get_json()["id"]
        resp = client.get(f"/api/projects/{pid}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Get Me"

    def test_list_projects(self, client, auth_headers, team_id):
        client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Project A",
        })
        client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Project B",
        })
        resp = client.get("/api/projects", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 2

    def test_list_projects_by_team(self, client, auth_headers, team_id):
        client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Project A",
        })
        resp = client.get(f"/api/projects?team_id={team_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.get_json()) == 1

    def test_list_projects_with_include_roi(self, client, auth_headers, team_id):
        client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Roi Project",
        })
        resp = client.get(f"/api/projects?team_id={team_id}&include_roi=true", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 1
        assert "roi_1yr" in data[0]
        assert "roi_3yr" in data[0]
        assert data[0]["roi_1yr"] is None
        assert data[0]["roi_3yr"] is None

    def test_list_projects_with_include_roi_after_calculation(self, client, auth_headers, team_id, app):
        create = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Roi Calc Project",
        })
        pid = create.get_json()["id"]
        # Assign first system formula
        archs = client.get("/api/formulas", headers=auth_headers).get_json()
        pa = client.post(f"/api/projects/{pid}/formulas", headers=auth_headers, json={
            "formula_id": archs[0]["id"],
        }).get_json()
        # Calculate ROI
        client.post(f"/api/projects/{pid}/formulas/{pa['id']}/calculate", headers=auth_headers)
        # List with include_roi
        resp = client.get(f"/api/projects?team_id={team_id}&include_roi=true", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["roi_1yr"] is not None
        assert data[0]["roi_3yr"] is not None
        assert isinstance(data[0]["roi_1yr"], (int, float))
        assert isinstance(data[0]["roi_3yr"], (int, float))

    def test_get_nonexistent_project(self, client, auth_headers):
        resp = client.get("/api/projects/9999", headers=auth_headers)
        assert resp.status_code == 404


class TestProjectUpdate:
    def test_update_project_status(self, client, auth_headers, team_id):
        create = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Status Project",
        })
        pid = create.get_json()["id"]
        resp = client.put(f"/api/projects/{pid}", headers=auth_headers, json={
            "status": "in_progress",
        })
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "in_progress"

    def test_update_project_name(self, client, auth_headers, team_id):
        create = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Old Name",
        })
        pid = create.get_json()["id"]
        resp = client.put(f"/api/projects/{pid}", headers=auth_headers, json={
            "name": "New Name",
        })
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "New Name"


class TestProjectDelete:
    def test_delete_project(self, client, auth_headers, team_id):
        create = client.post("/api/projects", headers=auth_headers, json={
            "team_id": team_id, "name": "Delete Me",
        })
        pid = create.get_json()["id"]
        resp = client.delete(f"/api/projects/{pid}", headers=auth_headers)
        assert resp.status_code == 204
        resp2 = client.get(f"/api/projects/{pid}", headers=auth_headers)
        assert resp2.status_code == 404
