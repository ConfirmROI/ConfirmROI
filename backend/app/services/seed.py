from app import create_app
from app.extensions import db
from app.models.value_formula import (
    ValueFormula,
    ValueAssumption,
    AssumptionDataType,
    FormulaAssumption,
)


SYSTEM_ASSUMPTIONS = [
    {"key": "monthly_cost_before", "label": "Monthly Cost Before", "data_type": "currency", "default_value": 10000, "description": "Monthly cost before the project"},
    {"key": "monthly_cost_after", "label": "Monthly Cost After", "data_type": "currency", "default_value": 5000, "description": "Expected monthly cost after the project"},
    {"key": "implementation_cost", "label": "Implementation Cost", "data_type": "currency", "default_value": 25000, "description": "One-time implementation cost"},
    {"key": "estimated_monthly_revenue", "label": "Estimated Monthly Revenue", "data_type": "currency", "default_value": 8000, "description": "Estimated new monthly revenue from the project"},
    {"key": "hours_saved_per_week", "label": "Hours Saved Per Week", "data_type": "number", "default_value": 20, "description": "Hours saved per week across the team"},
    {"key": "hourly_rate", "label": "Hourly Rate", "data_type": "currency", "default_value": 75, "description": "Average hourly rate of saved labor"},
    {"key": "risk_probability", "label": "Risk Probability", "data_type": "percentage", "default_value": 0.3, "description": "Annual probability of the risk event (0-1)"},
    {"key": "risk_impact", "label": "Risk Impact ($)", "data_type": "currency", "default_value": 100000, "description": "Financial impact if the risk event occurs"},
    {"key": "realization", "label": "Realization", "data_type": "percentage", "default_value": 0.6, "description": "Fraction of the estimated value that actually materializes"},
    {"key": "ic_count", "label": "IC Count", "data_type": "number", "default_value": 50, "description": "Number of individual contributors affected by the initiative"},
    {"key": "uplift_pct", "label": "Uplift %", "data_type": "percentage", "default_value": 0.02, "description": "Delivery speed increase as a decimal (e.g., 0.02 for 2%)"},
    {"key": "eng_cost", "label": "Engineer Cost", "data_type": "currency", "default_value": 180000, "description": "Fully loaded annual engineering cost"},
    {"key": "ramp_factor", "label": "Ramp Factor", "data_type": "percentage", "default_value": 0.75, "description": "Year-1 discount for adoption lag"},
    {"key": "attribution", "label": "Attribution", "data_type": "percentage", "default_value": 0.5, "description": "Haircut when multiple teams share credit (0.5 if co-owned)"},
    {"key": "downstream_npv_total", "label": "Downstream NPV Total", "data_type": "currency", "default_value": 500000, "description": "Sum of downstream NPV × P(ships) across dependent projects"},
    {"key": "enabler_attr", "label": "Enabler Attribution", "data_type": "percentage", "default_value": 0.20, "description": "Attribution percentage credited to this enabler (default 20%, cap 30%)"},
    {"key": "horizon_years", "label": "Horizon Years", "data_type": "number", "default_value": 3, "description": "Amortization period in years"},
    {"key": "delta_incidents_per_year", "label": "Incident Reduction (per year)", "data_type": "number", "default_value": 8, "description": "Reduction in major incidents per year"},
    {"key": "p_partner_impact", "label": "Partner Impact Probability", "data_type": "percentage", "default_value": 0.5, "description": "Probability a given incident generates partner escalation or friction"},
    {"key": "p_churn", "label": "Partner Churn Probability", "data_type": "percentage", "default_value": 0.05, "description": "Probability of partner churn given impact"},
    {"key": "avg_partner_arr", "label": "Average Partner ARR", "data_type": "currency", "default_value": 1500000, "description": "Revenue at risk per churned partner"},
    {"key": "p_vol_reduction", "label": "Volume Reduction Probability", "data_type": "percentage", "default_value": 0.30, "description": "Probability of deal-flow reduction short of churn"},
    {"key": "avg_vol_reduction_rev", "label": "Average Volume Reduction Revenue", "data_type": "currency", "default_value": 40000, "description": "Revenue impact of deal-flow reduction short of churn"},
    {"key": "team_cost", "label": "Team Cost", "data_type": "currency", "default_value": 979000, "description": "Fully loaded annual cost of the team"},
    {"key": "capacity", "label": "Allocated Capacity", "data_type": "number", "default_value": 1, "description": "Number of engineers allocated to this function"},
    {"key": "headcount", "label": "Team Headcount", "data_type": "number", "default_value": 4, "description": "Total engineers on the team"},
]

SYSTEM_FORMULAS = [
    {
        "name": "Cost Savings",
        "description": "Calculate annual ROI from reducing monthly operational costs.",
        "formula": "(monthly_cost_before - monthly_cost_after) * 12 - implementation_cost",
        "assumption_keys": ["monthly_cost_before", "monthly_cost_after", "implementation_cost"],
    },
    {
        "name": "Revenue Generation",
        "description": "Calculate annual ROI from generating new revenue.",
        "formula": "estimated_monthly_revenue * 12 - implementation_cost",
        "assumption_keys": ["estimated_monthly_revenue", "implementation_cost"],
    },
    {
        "name": "Time Saved",
        "description": "Calculate annual ROI from time savings converted to dollar value.",
        "formula": "hours_saved_per_week * 52 * hourly_rate - implementation_cost",
        "assumption_keys": ["hours_saved_per_week", "hourly_rate", "implementation_cost"],
    },
    {
        "name": "Risk Reduction",
        "description": "Calculate annual ROI from reducing risk probability and impact.",
        "formula": "risk_probability * risk_impact - implementation_cost",
        "assumption_keys": ["risk_probability", "risk_impact", "implementation_cost"],
    },
    {
        "name": "Velocity Multiplier",
        "description": "Structural improvements that compound across many engineers' delivery speed, valued as a fraction of their total cost.",
        "formula": "ic_count * uplift_pct * eng_cost * realization * ramp_factor * attribution",
        "assumption_keys": ["ic_count", "uplift_pct", "eng_cost", "realization", "ramp_factor", "attribution"],
    },
    {
        "name": "Enabler / Option Value",
        "description": "No direct cash value — the initiative unlocks downstream projects that do. Value is attributed upstream.",
        "formula": "downstream_npv_total * enabler_attr / horizon_years",
        "assumption_keys": ["downstream_npv_total", "enabler_attr", "horizon_years"],
    },
    {
        "name": "Reputation Shield",
        "description": "Reducing incident frequency to avoid erosion of partner and dealer trust — churn and deal-flow loss that follows reliability failures.",
        "formula": "delta_incidents_per_year * p_partner_impact * (p_churn * avg_partner_arr + p_vol_reduction * avg_vol_reduction_rev) * realization",
        "assumption_keys": ["delta_incidents_per_year", "p_partner_impact", "p_churn", "avg_partner_arr", "p_vol_reduction", "avg_vol_reduction_rev", "realization"],
    },
    {
        "name": "Support / KTLO",
        "description": "A deliberate capacity allocation decision, not a value-generation initiative. Cost = Opportunity, net ROI is zero by design.",
        "formula": "team_cost * (capacity / headcount)",
        "assumption_keys": ["team_cost", "capacity", "headcount"],
    },
]


def seed_formulas():
    assumption_map = {}
    for a_data in SYSTEM_ASSUMPTIONS:
        existing = ValueAssumption.query.filter_by(key=a_data["key"], is_system=True).first()
        if existing:
            assumption_map[a_data["key"]] = existing
            continue
        assumption = ValueAssumption(
            key=a_data["key"],
            label=a_data["label"],
            data_type=AssumptionDataType(a_data["data_type"]),
            default_value=a_data["default_value"],
            description=a_data["description"],
            is_system=True,
            user_id=None,
        )
        db.session.add(assumption)
        db.session.flush()
        assumption_map[a_data["key"]] = assumption

    for arch_data in SYSTEM_FORMULAS:
        existing = ValueFormula.query.filter_by(name=arch_data["name"], is_system=True).first()
        if existing:
            continue

        arch = ValueFormula(
            name=arch_data["name"],
            description=arch_data["description"],
            formula=arch_data["formula"],
            is_system=True,
            user_id=None,
        )
        db.session.add(arch)
        db.session.flush()

        for i, a_key in enumerate(arch_data["assumption_keys"]):
            link = FormulaAssumption(
                formula_id=arch.id,
                assumption_id=assumption_map[a_key].id,
                sort_order=i,
            )
            db.session.add(link)

    db.session.commit()
    print("System formulas and assumptions seeded successfully.")


def seed_default_user():
    from app.models.user import User, UserRole, UserTier
    from app.models.user_identity import UserIdentity
    from app.models.team import Team, TeamMember, TeamMemberRole

    existing = User.query.first()
    if existing:
        return

    user = User(
        email="user@localhost",
        name="User",
        role=UserRole.user,
        tier=UserTier.free,
    )
    db.session.add(user)
    db.session.flush()

    identity = UserIdentity(
        user_id=user.id,
        provider="local",
        provider_user_id="user@localhost",
    )
    db.session.add(identity)

    team = Team(
        name="My Team",
        manager_user_id=user.id,
    )
    db.session.add(team)
    db.session.flush()

    member = TeamMember(
        team_id=team.id,
        user_id=user.id,
        role=TeamMemberRole.manager,
    )
    db.session.add(member)
    db.session.commit()
    print("Default user and team seeded successfully.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_formulas()
        seed_default_user()
