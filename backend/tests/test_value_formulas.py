import pytest


@pytest.fixture
def team_and_project(client, auth_headers, team_id):
    project = client.post("/api/projects", headers=auth_headers, json={
        "team_id": team_id, "name": "Test Project",
    })
    project_id = project.get_json()["id"]
    return team_id, project_id


class TestFormulaList:
    def test_list_system_formulas(self, client, auth_headers, app):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        resp = client.get("/api/formulas", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) >= 4
        names = [d["name"] for d in data]
        assert "Cost Savings" in names
        assert "Revenue Generation" in names

    def test_list_formulas_no_auth(self, client):
        resp = client.get("/api/formulas")
        assert resp.status_code == 401


class TestFormulaDetail:
    def test_get_formula_detail(self, client, auth_headers, app):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        formulas = client.get("/api/formulas", headers=auth_headers).get_json()
        formula_id = formulas[0]["id"]

        resp = client.get(f"/api/formulas/{formula_id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "formula" in data
        assert "assumptions" in data
        assert len(data["assumptions"]) > 0


class TestFormulaCreate:
    def test_create_custom_formula(self, client, auth_headers):
        resp = client.post("/api/formulas", headers=auth_headers, json={
            "name": "Custom ROI",
            "description": "My custom formula",
            "formula": "revenue - cost",
            "assumptions": [
                {"key": "revenue", "label": "Revenue", "data_type": "currency", "default_value": 50000},
                {"key": "cost", "label": "Cost", "data_type": "currency", "default_value": 10000},
            ],
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Custom ROI"
        assert data["is_system"] is False
        assert len(data["assumptions"]) == 2

    def test_create_formula_no_auth(self, client):
        resp = client.post("/api/formulas", json={"name": "Test", "formula": "1"})
        assert resp.status_code == 401

    def test_create_formula_missing_name(self, client, auth_headers):
        resp = client.post("/api/formulas", headers=auth_headers, json={
            "formula": "1 + 2",
        })
        assert resp.status_code == 400

    def test_create_formula_missing_formula(self, client, auth_headers):
        resp = client.post("/api/formulas", headers=auth_headers, json={
            "name": "No Formula",
        })
        assert resp.status_code == 400


class TestProjectFormula:
    def test_assign_formula_to_project(self, client, auth_headers, app, team_and_project):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        _, project_id = team_and_project
        formulas = client.get("/api/formulas", headers=auth_headers).get_json()
        formula_id = formulas[0]["id"]

        resp = client.post(f"/api/projects/{project_id}/formulas", headers=auth_headers, json={
            "formula_id": formula_id,
        })
        assert resp.status_code == 201
        assert "id" in resp.get_json()

    def test_list_project_formulas(self, client, auth_headers, app, team_and_project):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        _, project_id = team_and_project
        formulas = client.get("/api/formulas", headers=auth_headers).get_json()
        formula_id = formulas[0]["id"]
        client.post(f"/api/projects/{project_id}/formulas", headers=auth_headers, json={
            "formula_id": formula_id,
        })

        resp = client.get(f"/api/projects/{project_id}/formulas", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.get_json()) == 1


class TestAssumptionValues:
    def test_update_assumption_value(self, client, auth_headers, app, team_and_project):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        _, project_id = team_and_project
        formulas = client.get("/api/formulas", headers=auth_headers).get_json()
        formula_id = formulas[0]["id"]

        pa = client.post(f"/api/projects/{project_id}/formulas", headers=auth_headers, json={
            "formula_id": formula_id,
        }).get_json()

        assumption_id = formulas[0]["assumptions"][0]["id"]
        resp = client.put(
            f"/api/projects/{project_id}/formulas/{pa['id']}/assumptions/{assumption_id}",
            headers=auth_headers,
            json={"value": 15000},
        )
        assert resp.status_code == 200
        assert resp.get_json()["value"] == 15000


class TestRoiCalculation:
    def test_calculate_roi_endpoint(self, client, auth_headers, app, team_and_project):
        from app.services.seed import seed_formulas
        with app.app_context():
            seed_formulas()

        _, project_id = team_and_project
        formulas = client.get("/api/formulas", headers=auth_headers).get_json()
        formula_id = formulas[0]["id"]

        pa = client.post(f"/api/projects/{project_id}/formulas", headers=auth_headers, json={
            "formula_id": formula_id,
        }).get_json()

        resp = client.post(
            f"/api/projects/{project_id}/formulas/{pa['id']}/calculate",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "roi_value" in data
        assert data["roi_value"] > 0
