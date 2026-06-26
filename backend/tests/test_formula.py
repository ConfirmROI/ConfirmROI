import pytest
from decimal import Decimal

from app.services.formula_service import FormulaService


class TestFormulaEvaluator:
    def test_simple_addition(self):
        result = FormulaService.evaluate("1 + 2", {})
        assert result == 3

    def test_subtraction(self):
        result = FormulaService.evaluate("10 - 4", {})
        assert result == 6

    def test_multiplication(self):
        result = FormulaService.evaluate("3 * 5", {})
        assert result == 15

    def test_division(self):
        result = FormulaService.evaluate("20 / 4", {})
        assert result == 5

    def test_with_variables(self):
        result = FormulaService.evaluate("a + b * c", {"a": 2, "b": 3, "c": 4})
        assert result == 14

    def test_cost_savings_formula(self):
        formula = "(monthly_cost_before - monthly_cost_after) * 12 - implementation_cost"
        result = FormulaService.evaluate(formula, {
            "monthly_cost_before": 10000,
            "monthly_cost_after": 5000,
            "implementation_cost": 25000,
        })
        assert result == 35000

    def test_revenue_generation_formula(self):
        formula = "estimated_monthly_revenue * 12 - implementation_cost"
        result = FormulaService.evaluate(formula, {
            "estimated_monthly_revenue": 8000,
            "implementation_cost": 30000,
        })
        assert result == 66000

    def test_time_saved_formula(self):
        formula = "hours_saved_per_week * 52 * hourly_rate - implementation_cost"
        result = FormulaService.evaluate(formula, {
            "hours_saved_per_week": 20,
            "hourly_rate": 75,
            "implementation_cost": 15000,
        })
        assert result == 63000

    def test_decimal_values(self):
        result = FormulaService.evaluate("a * b", {"a": Decimal("10.5"), "b": Decimal("2.0")})
        assert result == Decimal("21.0")

    def test_missing_variable_raises_error(self):
        with pytest.raises(NameNotDefinedError := __import__("simpleeval", fromlist=["NameNotDefined"]).NameNotDefined):
            FormulaService.evaluate("a + b", {"a": 1})

    def test_invalid_syntax_raises_error(self):
        with pytest.raises(Exception):
            FormulaService.evaluate("1 + * 2", {})

    def test_no_dangerous_functions(self):
        with pytest.raises(Exception):
            FormulaService.evaluate("__import__('os').system('ls')", {})

    def test_complex_formula_with_parens(self):
        result = FormulaService.evaluate("((a + b) * c) - d", {
            "a": 100, "b": 200, "c": 3, "d": 50,
        })
        assert result == 850

    def test_percentage_formula(self):
        result = FormulaService.evaluate("risk_probability * risk_impact", {
            "risk_probability": 0.3,
            "risk_impact": 100000,
        })
        assert result == 30000

    def test_validate_formula_valid(self):
        is_valid, error = FormulaService.validate_formula("a + b * c", ["a", "b", "c"])
        assert is_valid is True
        assert error is None

    def test_validate_formula_missing_var(self):
        is_valid, error = FormulaService.validate_formula("a + b", ["a"])
        assert is_valid is False
        assert "b" in error

    def test_validate_formula_invalid_syntax(self):
        is_valid, error = FormulaService.validate_formula("1 + * 2", [])
        assert is_valid is False
