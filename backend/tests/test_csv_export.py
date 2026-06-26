import csv
import io
import pytest

from app.extensions import db
from app.models.project import Project, ProjectStatus, ExternalSource
from app.models.value_formula import ValueFormula, ValueAssumption, ProjectFormula, ProjectAssumptionValue
from app.models.roi import RoiCalculation


@pytest.fixture
def projects_with_roi(app, client, auth_headers, team_id):
    p1 = client.post("/api/projects", headers=auth_headers, json={
        "name": "Export Project 1", "description": "First", "team_id": team_id, "status": "planning"
    })
    p2 = client.post("/api/projects", headers=auth_headers, json={
        "name": "Export Project 2", "description": "Second", "team_id": team_id, "status": "in_progress"
    })
    p1_id = p1.get_json()["id"]
    p2_id = p2.get_json()["id"]

    formula = client.post("/api/formulas", headers=auth_headers, json={
        "name": "Export Formula",
        "description": "Test",
        "formula": "value1 * 2",
        "assumptions": [{"key": "value1", "label": "Value 1", "data_type": "number", "default_value": 100}],
    })
    formula_id = formula.get_json()["id"]

    pa1 = client.post(f"/api/projects/{p1_id}/formulas", headers=auth_headers, json={"formula_id": formula_id})
    pa2 = client.post(f"/api/projects/{p2_id}/formulas", headers=auth_headers, json={"formula_id": formula_id})

    client.post(f"/api/projects/{p1_id}/formulas/{pa1.get_json()['id']}/calculate", headers=auth_headers)
    client.post(f"/api/projects/{p2_id}/formulas/{pa2.get_json()['id']}/calculate", headers=auth_headers)

    return team_id


class TestCsvExport:
    def test_export_projects_csv(self, client, auth_headers, projects_with_roi):
        resp = client.get(f"/api/projects/export?team_id={projects_with_roi}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.mimetype == "text/csv"

        reader = csv.DictReader(io.StringIO(resp.data.decode()))
        rows = list(reader)
        assert len(rows) == 2
        assert "name" in rows[0]
        assert "status" in rows[0]
        assert rows[0]["name"] == "Export Project 1"
        assert rows[1]["name"] == "Export Project 2"

    def test_export_csv_includes_roi(self, client, auth_headers, projects_with_roi):
        resp = client.get(f"/api/projects/export?team_id={projects_with_roi}", headers=auth_headers)
        assert resp.status_code == 200

        reader = csv.DictReader(io.StringIO(resp.data.decode()))
        rows = list(reader)
        assert "roi_1yr" in rows[0]
        assert float(rows[0]["roi_1yr"]) > 0

    def test_export_csv_no_auth(self, client, projects_with_roi):
        resp = client.get(f"/api/projects/export?team_id={projects_with_roi}")
        assert resp.status_code == 401

    def test_export_csv_no_team_id(self, client, auth_headers):
        resp = client.get("/api/projects/export", headers=auth_headers)
        assert resp.status_code == 400

    def test_export_csv_empty_team(self, client, auth_headers, team_id):
        resp = client.get(f"/api/projects/export?team_id={team_id}", headers=auth_headers)
        assert resp.status_code == 200
        reader = csv.DictReader(io.StringIO(resp.data.decode()))
        rows = list(reader)
        assert len(rows) == 0

    def test_export_csv_wrong_team(self, client, auth_headers):
        resp = client.get("/api/projects/export?team_id=9999", headers=auth_headers)
        assert resp.status_code == 404
