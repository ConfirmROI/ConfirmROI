import pytest
from decimal import Decimal

from app.extensions import db
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    AssumptionDataType,
    FormulaAssumption,
    ProjectFormula,
    ProjectAssumptionValue,
)
from app.models.roi import RoiCalculation
from app.services.formula_service import RoiService


@pytest.fixture
def setup_project_formula(app, auth_user):
    with app.app_context():
        arch = ValueFormula(
            name="Test Formula",
            formula="(a - b) * 12 - d",
            is_system=False,
            user_id=auth_user,
        )
        db.session.add(arch)
        db.session.flush()

        for i, (key, label, default) in enumerate([
            ("a", "A", 10000),
            ("b", "B", 5000),
            ("d", "D", 25000),
        ]):
            assumption = ValueAssumption(
                key=key,
                label=label,
                data_type=AssumptionDataType.currency,
                default_value=default,
                sort_order=i,
                is_system=False,
                user_id=auth_user,
            )
            db.session.add(assumption)
            db.session.flush()
            link = FormulaAssumption(
                formula_id=arch.id,
                assumption_id=assumption.id,
                sort_order=i,
            )
            db.session.add(link)

        db.session.flush()

        pa = ProjectFormula(
            project_id=1,
            formula_id=arch.id,
        )
        db.session.add(pa)
        db.session.flush()

        for assumption in arch.assumptions:
            pav = ProjectAssumptionValue(
                project_formula_id=pa.id,
                assumption_id=assumption.id,
                value=assumption.default_value,
            )
            db.session.add(pav)

        db.session.commit()
        return pa.id


class TestRoiService:
    def test_calculate_roi_with_defaults(self, app, setup_project_formula):
        with app.app_context():
            result = RoiService.calculate_roi(setup_project_formula)
            assert result is not None
            assert result["roi_value"] == 35000
            assert result["roi_value_3yr"] == 105000
            assert "calculation_id" in result

    def test_calculate_roi_stores_calculation(self, app, setup_project_formula):
        with app.app_context():
            RoiService.calculate_roi(setup_project_formula)
            calcs = RoiCalculation.query.filter_by(project_formula_id=setup_project_formula).all()
            assert len(calcs) == 1
            assert float(calcs[0].roi_value) == 35000
            assert float(calcs[0].roi_value_3yr) == 105000

    def test_get_latest_roi(self, app, setup_project_formula):
        with app.app_context():
            RoiService.calculate_roi(setup_project_formula)
            result = RoiService.get_latest_roi(setup_project_formula)
            assert result is not None
            assert result["roi_value"] == 35000
            assert result["roi_value_3yr"] == 105000

    def test_get_latest_roi_none(self, app, setup_project_formula):
        with app.app_context():
            result = RoiService.get_latest_roi(setup_project_formula)
            assert result is None

    def test_calculate_roi_nonexistent(self, app):
        with app.app_context():
            result = RoiService.calculate_roi(9999)
            assert result is None

    def test_compute_3yr_roi_formula(self):
        # 3yr = gross * 3 - one_time - (monthly*12 + annual) * 3
        assert RoiService.compute_3yr_roi(35000, 25000) == 80000
        assert RoiService.compute_3yr_roi(0, 0) == 0
        assert RoiService.compute_3yr_roi(100000, 50000) == 250000
        # With recurring monthly: gross=100000, one_time=25000, monthly=1000
        # 3yr = 300000 - 25000 - (12000 * 3) = 300000 - 25000 - 36000 = 239000
        assert RoiService.compute_3yr_roi(100000, 25000, monthly_recurring=1000) == 239000
