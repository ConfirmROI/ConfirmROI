import csv
import io
from datetime import date

from app.extensions import db
from app.models.project import Project, ProjectStatus, ExternalSource
from app.models.cost import CostEntry, CostCategory
from app.models.team import Team
from app.models.user import User


class CsvImportService:
    REQUIRED_COLUMNS = {"name"}

    @staticmethod
    def import_projects(file_obj, team_id: int) -> dict:
        result = {"imported": 0, "errors": []}

        try:
            reader = csv.DictReader(file_obj)
        except Exception:
            result["errors"].append("Failed to read CSV file")
            return result

        if not reader.fieldnames:
            result["errors"].append("CSV file is empty or has no header row")
            return result

        missing_cols = CsvImportService.REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_cols:
            result["errors"].append(f"Missing required columns: {', '.join(missing_cols)}")
            return result

        for row_num, row in enumerate(reader, start=2):
            name = (row.get("name") or "").strip()
            if not name:
                result["errors"].append(f"Row {row_num}: missing project name")
                continue

            status_str = (row.get("status") or "").strip() or "planning"
            try:
                status = ProjectStatus(status_str)
            except ValueError:
                result["errors"].append(f"Row {row_num}: invalid status '{status_str}', defaulting to planning")
                status = ProjectStatus.planning

            project = Project(
                team_id=team_id,
                name=name,
                description=(row.get("description") or "").strip() or None,
                external_id=(row.get("external_id") or "").strip() or None,
                external_source=ExternalSource.csv,
                status=status,
                start_date=CsvImportService._parse_date(row.get("start_date")),
                end_date=CsvImportService._parse_date(row.get("end_date")),
            )
            db.session.add(project)
            db.session.flush()

            default_cost = CostEntry(
                project_id=project.id,
                category=CostCategory.development,
                description="Development (labor)",
                person_weeks=0,
                amount=0,
            )
            db.session.add(default_cost)
            result["imported"] += 1

        db.session.commit()
        return result

    @staticmethod
    def _parse_date(date_str):
        if not date_str or not date_str.strip():
            return None
        try:
            return date.fromisoformat(date_str.strip())
        except (ValueError, TypeError):
            return None
