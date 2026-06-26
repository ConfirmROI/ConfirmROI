import io
import csv
import pytest

from app.extensions import db
from app.models.project import Project, ExternalSource
from app.services.import_service import CsvImportService


@pytest.fixture
def team_and_project(team_id):
    return team_id


class TestCsvImportService:
    def test_import_valid_csv(self, app, team_and_project):
        csv_content = "name,description,status,start_date,end_date\n"
        csv_content += "Project Alpha,First project,planning,2025-01-01,2025-06-30\n"
        csv_content += "Project Beta,Second project,in_progress,2025-02-01,\n"

        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 2
        assert result["errors"] == []

        with app.app_context():
            projects = Project.query.filter_by(team_id=team_and_project).all()
            assert len(projects) == 2
            assert projects[0].external_source == ExternalSource.csv
            assert projects[0].name == "Project Alpha"
            assert projects[1].name == "Project Beta"

    def test_import_csv_with_external_id(self, app, team_and_project):
        csv_content = "name,description,external_id,status\n"
        csv_content += "Jira Project,Jira import,PROJ1,planning\n"

        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 1
        with app.app_context():
            project = Project.query.filter_by(team_id=team_and_project).first()
            assert project.external_id == "PROJ1"
            assert project.external_source == ExternalSource.csv

    def test_import_csv_missing_name_column(self, app, team_and_project):
        csv_content = "description,status\nProject without name,planning\n"
        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 0
        assert len(result["errors"]) == 1
        assert "name" in result["errors"][0].lower()

    def test_import_csv_empty_file(self, app, team_and_project):
        buf = io.StringIO("")
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 0
        assert len(result["errors"]) >= 1

    def test_import_csv_row_missing_name(self, app, team_and_project):
        csv_content = "name,description,status\n"
        csv_content += ",Missing name,planning\n"
        csv_content += "Valid Project,Has name,planning\n"

        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 1
        assert len(result["errors"]) == 1
        with app.app_context():
            projects = Project.query.filter_by(team_id=team_and_project).all()
            assert len(projects) == 1
            assert projects[0].name == "Valid Project"

    def test_import_csv_invalid_date_skipped_or_nulled(self, app, team_and_project):
        csv_content = "name,start_date\nProject X,not-a-date\n"
        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 1
        with app.app_context():
            project = Project.query.filter_by(team_id=team_and_project).first()
            assert project.start_date is None

    def test_import_csv_duplicate_names_allowed(self, app, team_and_project):
        csv_content = "name\nDup Project\nDup Project\n"
        buf = io.StringIO(csv_content)
        result = CsvImportService.import_projects(buf, team_and_project)

        assert result["imported"] == 2

    def test_import_csv_via_api(self, client, auth_headers, team_and_project):
        csv_content = "name,description,status\nAPI Import,Test,planning\n"
        resp = client.post(
            f"/api/projects/import?team_id={team_and_project}",
            headers=auth_headers,
            data=csv_content,
            content_type="text/csv",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["imported"] == 1

    def test_import_csv_via_api_no_auth(self, client, team_and_project):
        csv_content = "name\nTest\n"
        resp = client.post(
            f"/api/projects/import?team_id={team_and_project}",
            data=csv_content,
            content_type="text/csv",
        )
        assert resp.status_code == 401

    def test_import_csv_via_api_no_team_id(self, client, auth_headers):
        csv_content = "name\nTest\n"
        resp = client.post(
            "/api/projects/import",
            headers=auth_headers,
            data=csv_content,
            content_type="text/csv",
        )
        assert resp.status_code == 400
