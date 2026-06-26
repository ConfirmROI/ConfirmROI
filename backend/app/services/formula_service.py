from decimal import Decimal
from simpleeval import EvalWithCompoundTypes, NameNotDefined

from app.extensions import db
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    ProjectFormula,
    ProjectAssumptionValue,
)
from app.models.roi import RoiCalculation
from app.models.cost import CostEntry


class FormulaService:
    @staticmethod
    def evaluate(formula: str, variables: dict) -> Decimal | float | int:
        evaluator = EvalWithCompoundTypes(names=variables)
        return evaluator.eval(formula)

    @staticmethod
    def validate_formula(formula: str, expected_keys: list[str]) -> tuple[bool, str | None]:
        try:
            test_vars = {k: 1 for k in expected_keys}
            FormulaService.evaluate(formula, test_vars)
            return True, None
        except NameNotDefined as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)


class RoiService:

    @staticmethod
    def _get_cost_breakdown(project_id: int) -> dict:
        """Return cost breakdown by cost_type for a project."""
        rows = db.session.query(
            CostEntry.cost_type,
            db.func.coalesce(db.func.sum(CostEntry.amount), 0),
        ).filter_by(project_id=project_id).group_by(CostEntry.cost_type).all()

        breakdown = {"one_time": 0.0, "recurring_monthly": 0.0, "recurring_annual": 0.0}
        for cost_type, total in rows:
            key = cost_type.value if cost_type else "one_time"
            if key in breakdown:
                breakdown[key] = float(total)
        return breakdown

    @staticmethod
    def calculate_roi(project_formula_id: int) -> dict:
        pa = db.session.get(ProjectFormula, project_formula_id)
        if not pa:
            return None

        formula = pa.formula
        assumptions = formula.assumptions

        values = {}
        for assumption in assumptions:
            pav = next(
                (v for v in pa.assumption_values if v.assumption_id == assumption.id),
                None,
            )
            values[assumption.key] = float(pav.value) if pav else float(assumption.default_value)

        # Set implementation_cost to 0 so the formula produces gross annual value;
        # actual costs are subtracted separately to handle recurring costs correctly.
        if "implementation_cost" in values:
            values["implementation_cost"] = 0

        gross_annual = FormulaService.evaluate(formula.formula, values)
        gross_annual = float(gross_annual)

        costs = RoiService._get_cost_breakdown(pa.project_id)
        roi_value_1yr = RoiService.compute_roi(gross_annual, costs, years=1)
        roi_value_3yr = RoiService.compute_roi(gross_annual, costs, years=3)

        calculation = RoiCalculation(
            project_formula_id=project_formula_id,
            roi_value=roi_value_1yr,
            roi_value_3yr=roi_value_3yr,
        )
        db.session.add(calculation)
        db.session.commit()

        return {
            "roi_value": roi_value_1yr,
            "roi_value_3yr": roi_value_3yr,
            "calculation_id": calculation.id,
            "calculated_at": calculation.calculated_at.isoformat() if calculation.calculated_at else None,
        }

    @staticmethod
    def compute_roi(gross_annual: float, costs: dict, years: int = 1) -> float:
        """Compute ROI for a given number of years.

        Args:
            gross_annual: Annual value before costs (formula result with implementation_cost=0).
            costs: dict with keys 'one_time', 'recurring_monthly', 'recurring_annual'.
            years: Number of years to compute ROI for.
        """
        one_time = costs.get("one_time", 0) if isinstance(costs, dict) else costs
        monthly_recurring = costs.get("recurring_monthly", 0) if isinstance(costs, dict) else 0
        annual_recurring = costs.get("recurring_annual", 0) if isinstance(costs, dict) else 0
        recurring_per_year = monthly_recurring * 12 + annual_recurring
        return gross_annual * years - one_time - recurring_per_year * years

    @staticmethod
    def compute_3yr_roi(gross_annual: float, one_time: float, monthly_recurring: float = 0, annual_recurring: float = 0) -> float:
        """Backward-compatible 3-year ROI computation."""
        costs = {"one_time": one_time, "recurring_monthly": monthly_recurring, "recurring_annual": annual_recurring}
        return RoiService.compute_roi(gross_annual, costs, years=3)

    @staticmethod
    def get_latest_roi(project_formula_id: int) -> dict | None:
        calc = (
            RoiCalculation.query
            .filter_by(project_formula_id=project_formula_id)
            .order_by(RoiCalculation.calculated_at.desc())
            .first()
        )
        if not calc:
            return None
        return calc.to_dict()
