from datetime import date

DEMO_DATA_VERSION = "1.0.0"

DEMO_PASSWORD = "Demo1234!"

DEMO_USERS = [
    {"name": "Sarah Chen",     "email": "sarah.chen@meridian.dev",    "free_role": "user",  "free_tier": "free", "paid_role": "admin", "paid_tier": "paid"},
    {"name": "Marcus Johnson", "email": "marcus.johnson@meridian.dev", "free_role": "user",  "free_tier": "free", "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Priya Patel",    "email": "priya.patel@meridian.dev",    "free_role": "user",  "free_tier": "free", "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Diego Ramirez",  "email": "diego.ramirez@meridian.dev",  "free_role": "user",  "free_tier": "free", "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Yuki Tanaka",    "email": "yuki.tanaka@meridian.dev",    "free_role": "user",  "free_tier": "free", "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Aisha Okonkwo",  "email": "aisha.okonkwo@meridian.dev",  "free_role": "user",  "free_tier": "free", "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Tom O'Brien",    "email": "tom.obrien@meridian.dev",     "free_role": None,    "free_tier": None,   "paid_role": "user",  "paid_tier": "paid"},
    {"name": "Lena Volkov",    "email": "lena.volkov@meridian.dev",    "free_role": None,    "free_tier": None,   "paid_role": "admin", "paid_tier": "paid"},
]

DEMO_TEAMS_FREE = [
    {"name": "Frontend Engineering",  "manager_email": "sarah.chen@meridian.dev",    "parent_name": None},
    {"name": "Backend Services",      "manager_email": "marcus.johnson@meridian.dev", "parent_name": None},
    {"name": "Infrastructure & DevOps","manager_email": "priya.patel@meridian.dev",   "parent_name": None},
    {"name": "Quality Engineering",   "manager_email": "diego.ramirez@meridian.dev",  "parent_name": None},
    {"name": "Mobile Development",    "manager_email": "yuki.tanaka@meridian.dev",    "parent_name": None},
    {"name": "Data Platform",         "manager_email": "aisha.okonkwo@meridian.dev",  "parent_name": None},
]

DEMO_TEAMS_PAID = [
    {"name": "Engineering",            "manager_email": "sarah.chen@meridian.dev",    "parent_name": None},
    {"name": "Platform Engineering",   "manager_email": "marcus.johnson@meridian.dev", "parent_name": "Engineering"},
    {"name": "Infrastructure & DevOps","manager_email": "priya.patel@meridian.dev",   "parent_name": "Engineering"},
    {"name": "Quality Engineering",    "manager_email": "diego.ramirez@meridian.dev",  "parent_name": "Engineering"},
    {"name": "Mobile Development",     "manager_email": "yuki.tanaka@meridian.dev",    "parent_name": "Engineering"},
    {"name": "Data Platform",          "manager_email": "aisha.okonkwo@meridian.dev",  "parent_name": "Engineering"},
    {"name": "Security & Compliance",  "manager_email": "tom.obrien@meridian.dev",     "parent_name": None},
    {"name": "Executive Leadership",   "manager_email": "lena.volkov@meridian.dev",    "parent_name": None},
]

DEMO_TEAM_MEMBERS_FREE = [
    {"team_name": "Backend Services",       "member_email": "priya.patel@meridian.dev"},
    {"team_name": "Backend Services",       "member_email": "diego.ramirez@meridian.dev"},
    {"team_name": "Infrastructure & DevOps","member_email": "marcus.johnson@meridian.dev"},
    {"team_name": "Infrastructure & DevOps","member_email": "aisha.okonkwo@meridian.dev"},
    {"team_name": "Frontend Engineering",   "member_email": "yuki.tanaka@meridian.dev"},
    {"team_name": "Quality Engineering",    "member_email": "marcus.johnson@meridian.dev"},
    {"team_name": "Data Platform",          "member_email": "priya.patel@meridian.dev"},
    {"team_name": "Mobile Development",     "member_email": "diego.ramirez@meridian.dev"},
]

DEMO_TEAM_MEMBERS_PAID = [
    {"team_name": "Platform Engineering",   "member_email": "diego.ramirez@meridian.dev"},
    {"team_name": "Platform Engineering",   "member_email": "lena.volkov@meridian.dev"},
    {"team_name": "Infrastructure & DevOps","member_email": "marcus.johnson@meridian.dev"},
    {"team_name": "Infrastructure & DevOps","member_email": "aisha.okonkwo@meridian.dev"},
    {"team_name": "Quality Engineering",    "member_email": "priya.patel@meridian.dev"},
    {"team_name": "Security & Compliance",  "member_email": "priya.patel@meridian.dev"},
    {"team_name": "Security & Compliance",  "member_email": "lena.volkov@meridian.dev"},
    {"team_name": "Engineering",            "member_email": "lena.volkov@meridian.dev"},
    {"team_name": "Data Platform",          "member_email": "marcus.johnson@meridian.dev"},
    {"team_name": "Mobile Development",     "member_email": "diego.ramirez@meridian.dev"},
]

DEMO_PROJECTS_FREE = [
    {
        "name": "Migrate CI/CD to GitHub Actions",
        "team_name": "Infrastructure & DevOps",
        "status": "completed",
        "external_source": "manual",
        "external_id": None,
        "description": "Replace legacy Jenkins pipelines with GitHub Actions for faster, cheaper CI/CD.",
        "start_date": date(2023, 6, 1),
        "end_date": date(2023, 9, 30),
        "formulas": [
            {
                "formula_name": "Cost Savings",
                "assumption_overrides": {
                    "monthly_cost_before": 12000,
                    "monthly_cost_after": 3500,
                    "implementation_cost": 18000,
                },
            }
        ],
        "costs": [
            {"description": "GitHub Actions infrastructure", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 800},
            {"description": "Migration consultant", "category": "vendor", "cost_type": "one_time", "amount": 12000},
        ],
    },
    {
        "name": "Launch Customer Portal v2",
        "team_name": "Frontend Engineering",
        "status": "in_progress",
        "external_source": "jira",
        "external_id": "PORT-142",
        "description": "Redesign customer-facing portal with self-service billing and usage analytics.",
        "start_date": date(2024, 1, 15),
        "end_date": date(2024, 7, 31),
        "formulas": [
            {
                "formula_name": "Revenue Generation",
                "assumption_overrides": {
                    "estimated_monthly_revenue": 15000,
                    "implementation_cost": 60000,
                },
            }
        ],
    },
    {
        "name": "Automate QA Regression Suite",
        "team_name": "Quality Engineering",
        "status": "in_progress",
        "external_source": "csv",
        "external_id": None,
        "description": "Build a fully automated regression suite to cut manual QA cycles from 3 days to 4 hours.",
        "start_date": date(2024, 2, 1),
        "end_date": date(2024, 6, 30),
        "formulas": [
            {
                "formula_name": "Time Saved",
                "assumption_overrides": {
                    "hours_saved_per_week": 40,
                    "hourly_rate": 85,
                    "implementation_cost": 22000,
                },
            }
        ],
        "costs": [
            {"description": "BrowserStack cross-browser testing", "category": "vendor", "cost_type": "recurring_monthly", "amount": 1200},
            {"description": "CI runner minutes (additional)", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 450},
        ],
    },
    {
        "name": "Implement SOC2 Compliance Controls",
        "team_name": "Infrastructure & DevOps",
        "status": "planning",
        "external_source": "manual",
        "external_id": None,
        "description": "Implement the 42 technical controls required for SOC2 Type II certification.",
        "start_date": date(2024, 8, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Risk Reduction",
                "assumption_overrides": {
                    "risk_probability": 0.45,
                    "risk_impact": 500000,
                    "implementation_cost": 80000,
                },
            }
        ],
        "costs": [
            {"description": "SOC2 Type II audit (external auditor)", "category": "vendor", "cost_type": "one_time", "amount": 45000},
            {"description": "Drata compliance automation platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 24000},
            {"description": "Security monitoring tooling", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 1500},
        ],
    },
    {
        "name": "Adopt TypeScript Across Frontend",
        "team_name": "Frontend Engineering",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Migrate the entire frontend codebase from JavaScript to TypeScript for long-term maintainability.",
        "start_date": date(2024, 1, 8),
        "end_date": date(2024, 9, 30),
        "formulas": [
            {
                "formula_name": "Velocity Multiplier",
                "assumption_overrides": {
                    "ic_count": 12,
                    "uplift_pct": 0.04,
                    "eng_cost": 175000,
                    "realization": 0.7,
                    "ramp_factor": 0.8,
                    "attribution": 1.0,
                },
            }
        ],
        "costs": [
            {"description": "TypeScript training workshop", "category": "vendor", "cost_type": "one_time", "amount": 8000},
        ],
    },
    {
        "name": "Reduce P1 Incidents by 50%",
        "team_name": "Infrastructure & DevOps",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Implement SLO alerting, chaos engineering, and runbook automation to halve P1 incidents.",
        "start_date": date(2024, 3, 1),
        "end_date": date(2024, 12, 31),
        "formulas": [
            {
                "formula_name": "Reputation Shield",
                "assumption_overrides": {
                    "delta_incidents_per_year": 12,
                    "p_partner_impact": 0.6,
                    "p_churn": 0.08,
                    "avg_partner_arr": 1200000,
                    "p_vol_reduction": 0.25,
                    "avg_vol_reduction_rev": 35000,
                    "realization": 0.65,
                },
            }
        ],
        "costs": [
            {"description": "Datadog APM & alerting", "category": "vendor", "cost_type": "recurring_monthly", "amount": 2800},
            {"description": "Gremlin chaos engineering platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 36000},
            {"description": "Additional on-call compensation", "category": "other", "cost_type": "recurring_annual", "amount": 15000},
        ],
    },
    {
        "name": "Maintain Legacy Billing System",
        "team_name": "Backend Services",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Ongoing maintenance of the legacy Perl-based billing engine pending full replacement.",
        "start_date": date(2024, 1, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Support / KTLO",
                "assumption_overrides": {
                    "team_cost": 920000,
                    "capacity": 1,
                    "headcount": 5,
                },
            }
        ],
        "costs": [
            {"description": "Legacy server hosting (on-prem)", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 4200},
            {"description": "Oracle database licensing", "category": "vendor", "cost_type": "recurring_annual", "amount": 48000},
        ],
    },
    {
        "name": "Containerize Monolith Services",
        "team_name": "Backend Services",
        "status": "completed",
        "external_source": "csv",
        "external_id": None,
        "description": "Break down the Rails monolith into Docker containers and deploy to ECS for elastic scaling.",
        "start_date": date(2023, 3, 1),
        "end_date": date(2023, 11, 30),
        "formulas": [
            {
                "formula_name": "Cost Savings",
                "assumption_overrides": {
                    "monthly_cost_before": 18000,
                    "monthly_cost_after": 7200,
                    "implementation_cost": 45000,
                },
            }
        ],
    },
    {
        "name": "Add Real-time Analytics Dashboard",
        "team_name": "Data Platform",
        "status": "planning",
        "external_source": "manual",
        "external_id": None,
        "description": "Build a real-time analytics dashboard for customer success teams to monitor usage trends.",
        "start_date": date(2024, 9, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Revenue Generation",
                "assumption_overrides": {
                    "estimated_monthly_revenue": 10000,
                    "implementation_cost": 55000,
                },
            },
            {
                "formula_name": "Velocity Multiplier",
                "assumption_overrides": {
                    "ic_count": 8,
                    "uplift_pct": 0.03,
                    "eng_cost": 170000,
                    "realization": 0.6,
                    "ramp_factor": 0.75,
                    "attribution": 0.5,
                },
            },
        ],
        "costs": [
            {"description": "Snowflake data warehouse", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 3500},
            {"description": "Looker analytics platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 30000},
        ],
    },
    {
        "name": "Onboarding Portal for New Hires",
        "team_name": "Frontend Engineering",
        "status": "cancelled",
        "external_source": "manual",
        "external_id": None,
        "description": "Self-service onboarding portal for new engineers. Cancelled — scope absorbed into internal wiki revamp.",
        "start_date": date(2023, 10, 1),
        "end_date": date(2023, 12, 15),
        "formulas": [
            {
                "formula_name": "Time Saved",
                "assumption_overrides": {
                    "hours_saved_per_week": 10,
                    "hourly_rate": 80,
                    "implementation_cost": 15000,
                },
            }
        ],
    },
    {
        "name": "Zero-Trust Network Migration",
        "team_name": "Infrastructure & DevOps",
        "status": "planning",
        "external_source": "jira",
        "external_id": "ZTN-11",
        "description": "Replace perimeter-based VPN with zero-trust access controls for all internal services.",
        "start_date": date(2024, 10, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Risk Reduction",
                "assumption_overrides": {
                    "risk_probability": 0.35,
                    "risk_impact": 750000,
                    "implementation_cost": 120000,
                },
            },
            {
                "formula_name": "Enabler / Option Value",
                "assumption_overrides": {
                    "downstream_npv_total": 800000,
                    "enabler_attr": 0.25,
                    "horizon_years": 3,
                },
            },
        ],
        "costs": [
            {"description": "Cloudflare Zero Trust platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 54000},
            {"description": "Network security audit", "category": "vendor", "cost_type": "one_time", "amount": 20000},
            {"description": "Hardware refresh (routers/switches)", "category": "infrastructure", "cost_type": "one_time", "amount": 35000},
        ],
    },
    {
        "name": "Build Internal Developer Platform",
        "team_name": "Backend Services",
        "status": "planning",
        "external_source": "jira",
        "external_id": "IDP-7",
        "description": "Create a golden-path platform with scaffolding, pipelines, and observability baked in.",
        "start_date": date(2024, 11, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Enabler / Option Value",
                "assumption_overrides": {
                    "downstream_npv_total": 1200000,
                    "enabler_attr": 0.20,
                    "horizon_years": 3,
                },
            }
        ],
        "costs": [
            {"description": "Backstage platform hosting", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 1200},
            {"description": "GitHub Enterprise licenses", "category": "vendor", "cost_type": "recurring_annual", "amount": 42000},
        ],
    },
]

DEMO_PROJECTS_PAID = [
    {
        "name": "Migrate CI/CD to GitHub Actions",
        "team_name": "Infrastructure & DevOps",
        "status": "completed",
        "external_source": "manual",
        "external_id": None,
        "description": "Replace legacy Jenkins pipelines with GitHub Actions for faster, cheaper CI/CD.",
        "start_date": date(2023, 6, 1),
        "end_date": date(2023, 9, 30),
        "formulas": [
            {
                "formula_name": "Cost Savings",
                "assumption_overrides": {
                    "monthly_cost_before": 12000,
                    "monthly_cost_after": 3500,
                    "implementation_cost": 18000,
                },
            }
        ],
        "costs": [
            {"description": "GitHub Actions infrastructure", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 800},
            {"description": "Migration consultant", "category": "vendor", "cost_type": "one_time", "amount": 12000},
        ],
    },
    {
        "name": "Launch Customer Portal v2",
        "team_name": "Platform Engineering",
        "status": "in_progress",
        "external_source": "jira",
        "external_id": "PORT-142",
        "description": "Redesign customer-facing portal with self-service billing and usage analytics.",
        "start_date": date(2024, 1, 15),
        "end_date": date(2024, 7, 31),
        "formulas": [
            {
                "formula_name": "Revenue Generation",
                "assumption_overrides": {
                    "estimated_monthly_revenue": 15000,
                    "implementation_cost": 60000,
                },
            }
        ],
        "costs": [
            {"description": "Cloud hosting (portal + API)", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 3200},
            {"description": "Auth0 identity platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 18000},
            {"description": "UX design contractor", "category": "vendor", "cost_type": "one_time", "amount": 25000},
        ],
    },
    {
        "name": "Automate QA Regression Suite",
        "team_name": "Quality Engineering",
        "status": "in_progress",
        "external_source": "csv",
        "external_id": None,
        "description": "Build a fully automated regression suite to cut manual QA cycles from 3 days to 4 hours.",
        "start_date": date(2024, 2, 1),
        "end_date": date(2024, 6, 30),
        "formulas": [
            {
                "formula_name": "Time Saved",
                "assumption_overrides": {
                    "hours_saved_per_week": 40,
                    "hourly_rate": 85,
                    "implementation_cost": 22000,
                },
            }
        ],
        "costs": [
            {"description": "BrowserStack cross-browser testing", "category": "vendor", "cost_type": "recurring_monthly", "amount": 1200},
            {"description": "CI runner minutes (additional)", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 450},
        ],
    },
    {
        "name": "Implement SOC2 Compliance Controls",
        "team_name": "Security & Compliance",
        "status": "planning",
        "external_source": "manual",
        "external_id": None,
        "description": "Implement the 42 technical controls required for SOC2 Type II certification.",
        "start_date": date(2024, 8, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Risk Reduction",
                "assumption_overrides": {
                    "risk_probability": 0.45,
                    "risk_impact": 500000,
                    "implementation_cost": 80000,
                },
            }
        ],
        "costs": [
            {"description": "SOC2 Type II audit (external auditor)", "category": "vendor", "cost_type": "one_time", "amount": 45000},
            {"description": "Drata compliance automation platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 24000},
            {"description": "Security monitoring tooling", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 1500},
        ],
    },
    {
        "name": "Adopt TypeScript Across Frontend",
        "team_name": "Engineering",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Migrate the entire frontend codebase from JavaScript to TypeScript for long-term maintainability.",
        "start_date": date(2024, 1, 8),
        "end_date": date(2024, 9, 30),
        "formulas": [
            {
                "formula_name": "Velocity Multiplier",
                "assumption_overrides": {
                    "ic_count": 22,
                    "uplift_pct": 0.04,
                    "eng_cost": 175000,
                    "realization": 0.7,
                    "ramp_factor": 0.8,
                    "attribution": 1.0,
                },
            }
        ],
        "costs": [
            {"description": "TypeScript training workshop", "category": "vendor", "cost_type": "one_time", "amount": 8000},
        ],
    },
    {
        "name": "Build Internal Developer Platform",
        "team_name": "Platform Engineering",
        "status": "planning",
        "external_source": "jira",
        "external_id": "IDP-7",
        "description": "Create a golden-path platform with scaffolding, pipelines, and observability baked in.",
        "start_date": date(2024, 11, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Enabler / Option Value",
                "assumption_overrides": {
                    "downstream_npv_total": 1200000,
                    "enabler_attr": 0.20,
                    "horizon_years": 3,
                },
            }
        ],
        "costs": [
            {"description": "Backstage platform hosting", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 1200},
            {"description": "GitHub Enterprise licenses", "category": "vendor", "cost_type": "recurring_annual", "amount": 42000},
        ],
    },
    {
        "name": "Reduce P1 Incidents by 50%",
        "team_name": "Infrastructure & DevOps",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Implement SLO alerting, chaos engineering, and runbook automation to halve P1 incidents.",
        "start_date": date(2024, 3, 1),
        "end_date": date(2024, 12, 31),
        "formulas": [
            {
                "formula_name": "Reputation Shield",
                "assumption_overrides": {
                    "delta_incidents_per_year": 12,
                    "p_partner_impact": 0.6,
                    "p_churn": 0.08,
                    "avg_partner_arr": 1200000,
                    "p_vol_reduction": 0.25,
                    "avg_vol_reduction_rev": 35000,
                    "realization": 0.65,
                },
            }
        ],
        "costs": [
            {"description": "Datadog APM & alerting", "category": "vendor", "cost_type": "recurring_monthly", "amount": 2800},
            {"description": "Gremlin chaos engineering platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 36000},
            {"description": "Additional on-call compensation", "category": "other", "cost_type": "recurring_annual", "amount": 15000},
        ],
    },
    {
        "name": "Maintain Legacy Billing System",
        "team_name": "Platform Engineering",
        "status": "in_progress",
        "external_source": "manual",
        "external_id": None,
        "description": "Ongoing maintenance of the legacy Perl-based billing engine pending full replacement.",
        "start_date": date(2024, 1, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Support / KTLO",
                "assumption_overrides": {
                    "team_cost": 920000,
                    "capacity": 1,
                    "headcount": 5,
                },
            }
        ],
        "costs": [
            {"description": "Legacy server hosting (on-prem)", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 4200},
            {"description": "Oracle database licensing", "category": "vendor", "cost_type": "recurring_annual", "amount": 48000},
        ],
    },
    {
        "name": "Containerize Monolith Services",
        "team_name": "Platform Engineering",
        "status": "completed",
        "external_source": "csv",
        "external_id": None,
        "description": "Break down the Rails monolith into Docker containers and deploy to ECS for elastic scaling.",
        "start_date": date(2023, 3, 1),
        "end_date": date(2023, 11, 30),
        "formulas": [
            {
                "formula_name": "Cost Savings",
                "assumption_overrides": {
                    "monthly_cost_before": 18000,
                    "monthly_cost_after": 7200,
                    "implementation_cost": 45000,
                },
            }
        ],
        "costs": [
            {"description": "ECS Fargate compute", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 2800},
            {"description": "Docker Business licenses", "category": "vendor", "cost_type": "recurring_annual", "amount": 12000},
        ],
    },
    {
        "name": "Add Real-time Analytics Dashboard",
        "team_name": "Data Platform",
        "status": "planning",
        "external_source": "manual",
        "external_id": None,
        "description": "Build a real-time analytics dashboard for customer success teams to monitor usage trends.",
        "start_date": date(2024, 9, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Revenue Generation",
                "assumption_overrides": {
                    "estimated_monthly_revenue": 10000,
                    "implementation_cost": 55000,
                },
            },
            {
                "formula_name": "Velocity Multiplier",
                "assumption_overrides": {
                    "ic_count": 8,
                    "uplift_pct": 0.03,
                    "eng_cost": 170000,
                    "realization": 0.6,
                    "ramp_factor": 0.75,
                    "attribution": 0.5,
                },
            },
        ],
        "costs": [
            {"description": "Snowflake data warehouse", "category": "infrastructure", "cost_type": "recurring_monthly", "amount": 3500},
            {"description": "Looker analytics platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 30000},
        ],
    },
    {
        "name": "Onboarding Portal for New Hires",
        "team_name": "Engineering",
        "status": "cancelled",
        "external_source": "manual",
        "external_id": None,
        "description": "Self-service onboarding portal for new engineers. Cancelled — scope absorbed into internal wiki revamp.",
        "start_date": date(2023, 10, 1),
        "end_date": date(2023, 12, 15),
        "formulas": [
            {
                "formula_name": "Time Saved",
                "assumption_overrides": {
                    "hours_saved_per_week": 10,
                    "hourly_rate": 80,
                    "implementation_cost": 15000,
                },
            }
        ],
    },
    {
        "name": "Zero-Trust Network Migration",
        "team_name": "Security & Compliance",
        "status": "planning",
        "external_source": "jira",
        "external_id": "ZTN-11",
        "description": "Replace perimeter-based VPN with zero-trust access controls for all internal services.",
        "start_date": date(2024, 10, 1),
        "end_date": None,
        "formulas": [
            {
                "formula_name": "Risk Reduction",
                "assumption_overrides": {
                    "risk_probability": 0.35,
                    "risk_impact": 750000,
                    "implementation_cost": 120000,
                },
            },
            {
                "formula_name": "Enabler / Option Value",
                "assumption_overrides": {
                    "downstream_npv_total": 800000,
                    "enabler_attr": 0.25,
                    "horizon_years": 3,
                },
            },
        ],
        "costs": [
            {"description": "Cloudflare Zero Trust platform", "category": "vendor", "cost_type": "recurring_annual", "amount": 54000},
            {"description": "Network security audit", "category": "vendor", "cost_type": "one_time", "amount": 20000},
            {"description": "Hardware refresh (routers/switches)", "category": "infrastructure", "cost_type": "one_time", "amount": 35000},
        ],
    },
]

DEMO_CUSTOM_ASSUMPTIONS_FREE = [
    {
        "key": "onboarding_time_saved_days",
        "label": "Onboarding Time Saved (days)",
        "data_type": "number",
        "default_value": 5,
        "description": "Days saved per new hire through improved onboarding tooling.",
        "owner_email": "sarah.chen@meridian.dev",
    },
    {
        "key": "compliance_fine_amount",
        "label": "Compliance Fine Amount",
        "data_type": "currency",
        "default_value": 250000,
        "description": "Estimated regulatory fine if compliance controls are not in place.",
        "owner_email": "priya.patel@meridian.dev",
    },
    {
        "key": "retention_improvement_pct",
        "label": "Retention Improvement %",
        "data_type": "percentage",
        "default_value": 0.03,
        "description": "Expected improvement in annual engineer retention rate.",
        "owner_email": "marcus.johnson@meridian.dev",
    },
]

DEMO_CUSTOM_ASSUMPTIONS_PAID = [
    {
        "key": "onboarding_time_saved_days",
        "label": "Onboarding Time Saved (days)",
        "data_type": "number",
        "default_value": 5,
        "description": "Days saved per new hire through improved onboarding tooling.",
        "owner_email": "sarah.chen@meridian.dev",
    },
    {
        "key": "compliance_fine_amount",
        "label": "Compliance Fine Amount",
        "data_type": "currency",
        "default_value": 250000,
        "description": "Estimated regulatory fine if compliance controls are not in place.",
        "owner_email": "tom.obrien@meridian.dev",
    },
    {
        "key": "retention_improvement_pct",
        "label": "Retention Improvement %",
        "data_type": "percentage",
        "default_value": 0.03,
        "description": "Expected improvement in annual engineer retention rate.",
        "owner_email": "marcus.johnson@meridian.dev",
    },
]

DEMO_CUSTOM_FORMULAS_FREE = [
    {
        "name": "Developer Productivity",
        "description": "Measure ROI of initiatives that directly lift individual contributor output.",
        "formula": "ic_count * uplift_pct * eng_cost * ramp_factor",
        "owner_email": "sarah.chen@meridian.dev",
        "assumption_keys": ["ic_count", "uplift_pct", "eng_cost", "ramp_factor"],
    },
    {
        "name": "Compliance Fine Avoidance",
        "description": "Estimate value of avoiding a regulatory fine through proactive compliance work.",
        "formula": "risk_probability * risk_impact * realization",
        "owner_email": "priya.patel@meridian.dev",
        "assumption_keys": ["risk_probability", "risk_impact", "realization"],
    },
]

DEMO_CUSTOM_FORMULAS_PAID = [
    {
        "name": "Developer Productivity",
        "description": "Measure ROI of initiatives that directly lift individual contributor output.",
        "formula": "ic_count * uplift_pct * eng_cost * ramp_factor",
        "owner_email": "sarah.chen@meridian.dev",
        "assumption_keys": ["ic_count", "uplift_pct", "eng_cost", "ramp_factor"],
    },
    {
        "name": "Compliance Fine Avoidance",
        "description": "Estimate value of avoiding a regulatory fine through proactive compliance work.",
        "formula": "risk_probability * risk_impact * realization",
        "owner_email": "tom.obrien@meridian.dev",
        "assumption_keys": ["risk_probability", "risk_impact", "realization"],
    },
]
