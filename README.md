# ConfirmROI

Open-source ROI confirmation platform for engineering teams. Measure and prove the value of your engineering initiatives with customizable value archetypes, formula-based ROI calculations, and integrations with Jira and CSV imports.

## Features

- **Value Archetypes** — 8 pre-built ROI models (Cost Savings, Revenue Generation, Time Saved, Risk Reduction, Velocity Multiplier, Enabler/Option Value, Reputation Shield, Support/KTLO) plus custom formulas (powered by `simpleeval`)
- **Assumptions** — 26 system assumptions with number, currency, and percentage data types. Standalone, reusable across formulas. Custom assumptions supported.
- **Project Management** — Create projects, assign to teams, track status (planning/in_progress/completed/cancelled), search, external source tags (Jira/CSV)
- **ROI Calculation** — Assign formulas to projects, adjust assumptions, live recalculation. ROI Summary with 1-year/3-year ROI, investment multiples, one-time vs recurring cost breakdown.
- **Cost Tracker / Investment** — Per-project cost entries by category (development, infrastructure, vendor, other). Person-weeks auto-calculation from labor rate. Cost types: one-time, recurring monthly, recurring annual. Estimate vs actual flag.
- **Dashboard** — Summary cards, ROI bar chart with formula breakdown, date range filtering, recent projects list
- **CSV Import/Export** — Bulk import projects from CSV, export with ROI data
- **Jira Integration** — Connect Jira, fetch and import projects via REST API
- **Audit History** — Change tracking per entity with who/what/when, change reasons, old→new values
- **Team Management** — Multi-team support with free tier (1 team) and paid tier (unlimited teams, hierarchy, labor cost settings)
- **JWT Authentication** — Secure auth with access/refresh tokens
- **Modern SPA Frontend** — Vue 3 + Pinia + Tailwind CSS with charts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.0, SQLAlchemy 2.0, Flask-Migrate (Alembic) |
| Auth | Flask-JWT-Extended, Passlib (bcrypt) |
| Formula Engine | simpleeval |
| Frontend | Vue 3, Vue Router, Pinia, Tailwind CSS |
| Charts | Chart.js + vue-chartjs |
| Icons | Lucide |
| Database | PostgreSQL (production), SQLite (test) |
| Deployment | Docker, docker-compose, Gunicorn |

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL (or use Docker)

### Using Docker

```bash
cp .env.example .env
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app wsgi db upgrade
python -m app.services.seed
flask --app wsgi run
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing

**Backend (94 tests):**
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

**Frontend (14 tests):**
```bash
cd frontend
npm test
```

## API Endpoints

### Auth
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login
- `POST /api/auth/refresh` — Refresh token
- `GET /api/auth/me` — Current user

### Teams
- `POST /api/teams` — Create team
- `GET /api/teams` — List teams
- `GET /api/teams/:id` — Get team
- `PUT /api/teams/:id` — Update team
- `DELETE /api/teams/:id` — Delete team

### Projects
- `POST /api/projects` — Create project
- `GET /api/projects` — List projects (filter by `team_id`)
- `GET /api/projects/:id` — Get project
- `PUT /api/projects/:id` — Update project
- `DELETE /api/projects/:id` — Delete project
- `POST /api/projects/import?team_id=N` — Import from CSV
- `GET /api/projects/export?team_id=N` — Export to CSV

### Archetypes
- `GET /api/archetypes` — List archetypes
- `GET /api/archetypes/:id` — Get archetype
- `POST /api/archetypes` — Create custom archetype
- `DELETE /api/archetypes/:id` — Delete custom archetype

### Assumptions & ROI
- `POST /api/projects/:id/archetypes` — Assign archetype to project
- `GET /api/projects/:id/archetypes` — List project archetypes
- `PUT /api/projects/:id/archetypes/:paId/assumptions/:aId` — Update assumption value
- `POST /api/projects/:id/archetypes/:paId/calculate` — Calculate ROI
- `GET /api/projects/:id/archetypes/:paId/roi` — Get latest ROI

### Jira
- `POST /api/teams/:teamId/jira` — Create Jira connection
- `GET /api/teams/:teamId/jira` — Get Jira connection
- `DELETE /api/teams/:teamId/jira` — Delete Jira connection
- `POST /api/teams/:teamId/jira/import` — Import projects from Jira

## Project Structure

```
confirmroi/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration
│   │   ├── extensions.py        # db, migrate, jwt
│   │   ├── api/                 # Blueprints (auth, teams, projects, etc.)
│   │   ├── models/              # SQLAlchemy models
│   │   ├── services/            # Business logic (auth, import, jira, formula, roi, seed)
│   │   └── utils/
│   ├── migrations/              # Alembic migrations
│   ├── tests/                   # pytest tests (94 tests)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── wsgi.py
├── frontend/
│   ├── src/
│   │   ├── api/client.js        # Axios client with JWT interceptor
│   │   ├── stores/              # Pinia stores (auth, projects, dashboard)
│   │   ├── router/              # Vue Router with auth guards
│   │   ├── views/               # Page views (Login, Register, Dashboard, etc.)
│   │   ├── components/          # Reusable components (RoiChart, ProjectCard, etc.)
│   │   └── style.css
│   ├── Dockerfile
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml
├── .env.example
├── Makefile
└── .gitignore
```

## Free vs Paid Tier

| Feature | Free (OSS) | Paid (SaaS) |
|---------|------|------|
| Price | Free, open source | Per-seat subscription |
| Hosting | Self-hosted (Docker) | Managed cloud |
| Users | Single user | Organization-wide |
| Teams | 1 team | Multiple teams (Starter: 10, Growth: unlimited, Enterprise: unlimited) |
| Team hierarchy | — | 2 levels (Starter), 5 levels (Growth), unlimited (Enterprise) |
| System Archetypes | All 8 | All 8 |
| System Assumptions | All 26 | All 26 |
| Custom Archetypes | Yes | Yes + org-wide sharing |
| Assumptions | Editable per project | Editable + collaborative with audit trail |
| ROI Calculation | Per-project | Per-project + rollup aggregation across teams |
| Cost Tracker | Yes | Yes + team labor rate defaults |
| Dashboard | Single team, date filtering | Multi-team filtering, org-wide view, date filtering |
| Audit History | — | Growth and Enterprise |
| SSO | — | Google (Growth+), Okta/SAML (Enterprise) |
| Scheduled reports | — | Enterprise |
| PDF export | — | Growth and Enterprise |
| CSV Import/Export | Yes | Yes |
| Jira Integration | Yes | Yes |
| Collaboration | — | Multiple managers, shared assumptions |
| Support | Community | Email / Priority / Dedicated |
| License | MIT | Commercial |

## License

MIT
