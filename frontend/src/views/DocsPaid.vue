<script setup>
import NavBar from '../components/NavBar.vue'
import SiteFooter from '../components/SiteFooter.vue'
import DocsSidebar from '../components/DocsSidebar.vue'
import {
  TrendingUp, Zap, CreditCard, LayoutDashboard, Users, FolderKanban,
  Calculator, Lightbulb, BarChart3, DollarSign, History, Shield, LifeBuoy,
} from 'lucide-vue-next'

const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'getting-started', label: 'Getting Started' },
  { id: 'pricing', label: 'Pricing & Plans' },
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'teams', label: 'Teams' },
  { id: 'projects', label: 'Projects' },
  { id: 'formulas', label: 'Value Formulas' },
  { id: 'assumptions', label: 'Assumptions' },
  { id: 'roi', label: 'ROI Calculations' },
  { id: 'cost-tracker', label: 'Cost Tracker' },
  { id: 'audit', label: 'Audit History' },
  { id: 'enterprise', label: 'Enterprise Features' },
  { id: 'support', label: 'Support' },
]

const plans = [
  {
    name: 'Starter',
    price: '$9',
    period: '/seat/mo',
    seats: 'Up to 25',
    readonlySeats: '200',
    teams: 'Up to 10',
    hierarchy: '2 levels',
    sso: null,
    audit: null,
    scheduled: null,
    support: 'Email',
  },
  {
    name: 'Growth',
    price: '$19',
    period: '/seat/mo',
    seats: 'Up to 100',
    readonlySeats: '1000',
    teams: 'Unlimited',
    hierarchy: '5 levels',
    sso: 'Google',
    audit: 'Yes',
    scheduled: null,
    support: 'Priority email',
  },
  {
    name: 'Enterprise',
    price: 'Contact us',
    period: '',
    seats: 'Unlimited',
    readonlySeats: 'Unlimited',
    teams: 'Unlimited',
    hierarchy: 'Unlimited',
    sso: 'Google + Okta/SAML',
    audit: 'Yes',
    scheduled: 'Yes',
    support: 'Dedicated',
  },
]

const planFeatures = [
  { key: 'seats', label: 'Seats' },
  { key: 'readonlySeats', label: 'Read-only seats' },
  { key: 'teams', label: 'Teams' },
  { key: 'hierarchy', label: 'Hierarchy levels' },
  { key: 'sso', label: 'SSO' },
  { key: 'audit', label: 'Audit trail' },
  { key: 'scheduled', label: 'Scheduled reports' },
  { key: 'support', label: 'Support' },
]
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-12">
        <DocsSidebar :sections="sections" />

        <article class="prose prose-slate max-w-none">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Paid (Hosted SaaS) Documentation</h1>
          <p class="text-gray-500 mb-8">Guide for the managed ConfirmROI platform — multi-team collaboration, hierarchical rollups, and enterprise features.</p>

          <!-- Overview -->
          <section id="overview" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <TrendingUp class="w-6 h-6 text-primary-600" /> Overview
            </h2>
            <p class="text-gray-700 mb-3">
              Engineering leaders struggle to prove the value of complex work — risk reduction, velocity improvements,
              enabler projects, keep-the-lights-on investments. ConfirmROI solves this with transparent, defensible
              formulas instead of gut feelings.
            </p>
            <p class="text-gray-700 mb-3">
              <strong>Why hosted?</strong> The managed platform adds what self-hosting can't:
            </p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Multi-team collaboration</strong> — multiple managers, shared assumptions, org-wide visibility</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Hierarchical rollups</strong> — aggregate ROI across sub-teams and parent teams</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Audit trails</strong> — every change tracked with who, what, when, and why</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>SSO</strong> — Google and Okta/SAML integration for enterprise authentication</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>No infrastructure to manage</strong> — we handle updates, backups, and scaling</li>
            </ul>
            <p class="text-gray-700 mt-3">All core features from the free version are included — 8 system formulas, 26 assumptions, cost tracking, CSV import/export, and Jira integration.</p>
          </section>

          <!-- Getting Started -->
          <section id="getting-started" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap class="w-6 h-6 text-primary-600" /> Getting Started
            </h2>
            <ol class="space-y-3 text-gray-700">
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">1</span>
                <div><strong>Choose a plan</strong> — Select Starter, Growth, or Enterprise based on your team size and needs. See <a href="#pricing" class="text-primary-600 hover:underline">Pricing & Plans</a> below.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">2</span>
                <div><strong>Register your account</strong> — Sign up at <router-link to="/register" class="text-primary-600 hover:underline">/register</router-link> with your plan selected.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">3</span>
                <div><strong>Set up teams</strong> — Create teams that match your org structure. Assign managers and members.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">4</span>
                <div><strong>Create projects</strong> — Add projects and assign them to teams. Import from CSV or Jira for bulk setup.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">5</span>
                <div><strong>Assign formulas and track ROI</strong> — Assign value formulas, adjust assumptions, and watch ROI update live.</div>
              </li>
            </ol>
          </section>

          <!-- Pricing & Plans -->
          <section id="pricing" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <CreditCard class="w-6 h-6 text-primary-600" /> Pricing & Plans
            </h2>
            <p class="text-gray-700 mb-4">Three tiers based on organization size and feature needs. All plans include the full formula engine, cost tracker, CSV import/export, and Jira integration.</p>

            <div class="grid md:grid-cols-3 gap-4 mb-6">
              <div v-for="plan in plans" :key="plan.name" class="border-2 border-slate-200 rounded-xl p-6 flex flex-col">
                <h3 class="text-lg font-bold text-gray-900">{{ plan.name }}</h3>
                <div class="mt-2 flex items-baseline gap-1">
                  <span class="text-2xl font-extrabold text-gray-900">{{ plan.price }}</span>
                  <span class="text-sm text-gray-500">{{ plan.period }}</span>
                </div>
                <ul class="mt-4 space-y-2 flex-1 text-sm">
                  <li v-for="feat in planFeatures" :key="feat.key" class="flex items-start gap-2">
                    <span v-if="plan[feat.key]" class="text-accent-600 flex-shrink-0">✓</span>
                    <span v-else class="text-slate-300 flex-shrink-0">—</span>
                    <span class="text-gray-600">
                      <span class="font-medium text-gray-700">{{ feat.label }}:</span>
                      {{ plan[feat.key] || '—' }}
                    </span>
                  </li>
                </ul>
                <router-link
                  :to="{ path: '/register', query: { plan: plan.name } }"
                  class="mt-6 inline-flex items-center justify-center px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-semibold hover:bg-primary-700 transition-colors"
                >
                  Get Started
                </router-link>
              </div>
            </div>

            <div class="rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Read-only seats</strong> are included at 8x the manager seat count. Read-only users can view dashboards, projects, and ROI but cannot edit assumptions or costs.
              </p>
            </div>
          </section>

          <!-- Dashboard -->
          <section id="dashboard" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <LayoutDashboard class="w-6 h-6 text-primary-600" /> Dashboard
            </h2>
            <p class="text-gray-700 mb-3">The paid dashboard extends the free version with multi-team visibility:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Summary cards</strong> — total projects, total ROI, formula count (filtered by team selection)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>ROI bar chart</strong> with formula breakdown across selected teams</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Team filter dropdown</strong> — filter by a specific team or view org-wide (all teams)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Date range filtering</strong> — focus on a specific period with start/end date filters</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Recent projects list</strong> with quick links to project details</li>
            </ul>
          </section>

          <!-- Teams -->
          <section id="teams" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Users class="w-6 h-6 text-primary-600" /> Teams
            </h2>
            <p class="text-gray-700 mb-3">Teams organize your projects and enable hierarchical rollups. Create as many teams as your plan allows.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Team Management</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Create, edit, and delete teams from the Teams page</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Assign team managers who can create and manage projects within their team</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Projects are assigned to a team on creation</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Team Hierarchy</h3>
            <p class="text-gray-700 mb-3">Create parent and sub-team relationships to match your org structure:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Set a <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">parent_team_id</code> to create sub-teams</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Hierarchy depth depends on your plan (Starter: 2 levels, Growth: 5 levels, Enterprise: unlimited)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Rollup aggregations sum ROI across all sub-teams up to the parent</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Team Labor Cost Settings</h3>
            <p class="text-gray-700 mb-3">Set <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">avg_labor_cost_per_week</code> at the team level. This rate is used to auto-calculate development costs from person-weeks when no project-level rate is set.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Jira Integration</h3>
            <p class="text-gray-700">Connect Jira per team using an API token. Import projects from Jira into the connected team. Imported projects are tagged with their Jira source.</p>
          </section>

          <!-- Projects -->
          <section id="projects" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FolderKanban class="w-6 h-6 text-primary-600" /> Projects
            </h2>
            <p class="text-gray-700 mb-3">Projects represent your engineering initiatives. In the paid version, projects are organized across multiple teams.</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Create:</strong> Click "New Project" and fill in name, description, team, and status</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Edit / Delete:</strong> Use the pencil/trash icons on the project detail page</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Search:</strong> Filter by name on the Projects page</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Multi-team organization:</strong> Assign projects to any team you manage</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>External source tags:</strong> Projects imported from Jira or CSV are tagged with their source</li>
            </ul>
            <p class="text-gray-700 mt-3">Project statuses: <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">planning</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">in_progress</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">completed</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">cancelled</span></p>
          </section>

          <!-- Value Formulas -->
          <section id="formulas" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Calculator class="w-6 h-6 text-primary-600" /> Value Formulas
            </h2>
            <p class="text-gray-700 mb-3">All 8 system formulas are available (Cost Savings, Revenue Generation, Time Saved, Risk Reduction, Velocity Multiplier, Enabler/Option Value, Reputation Shield, Support/KTLO). See the <router-link to="/docs/free#formulas" class="text-primary-600 hover:underline">free docs</router-link> for the full formula reference.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Org-Wide Sharing</h3>
            <p class="text-gray-700">Custom formulas created by any manager are shared across the organization. This ensures consistent ROI methodology — everyone uses the same formula definitions, and changes are tracked via the audit trail.</p>
          </section>

          <!-- Assumptions -->
          <section id="assumptions" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Lightbulb class="w-6 h-6 text-primary-600" /> Assumptions
            </h2>
            <p class="text-gray-700 mb-3">All 26 system assumptions are available. See the <router-link to="/docs/free#assumptions" class="text-primary-600 hover:underline">free docs</router-link> for the full assumption reference table.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Collaborative Assumptions</h3>
            <p class="text-gray-700 mb-3">In the paid version, assumptions are collaborative:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Multiple managers can edit assumption values on shared projects</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Every change is recorded in the audit trail with who, what, when, and why</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Custom assumptions are shared org-wide, ensuring consistent definitions</li>
            </ul>
          </section>

          <!-- ROI Calculations -->
          <section id="roi" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 class="w-6 h-6 text-primary-600" /> ROI Calculations
            </h2>
            <p class="text-gray-700 mb-3">ROI calculation works the same as the free version — assign formulas, adjust assumptions, ROI updates live. See the <router-link to="/docs/free#roi" class="text-primary-600 hover:underline">free docs</router-link> for the full walkthrough.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Rollup Aggregation</h3>
            <p class="text-gray-700">In the paid version, ROI rolls up across teams. A parent team's dashboard shows aggregated ROI from all its sub-teams. This gives engineering leaders an org-wide view without manually consolidating spreadsheets.</p>
          </section>

          <!-- Cost Tracker -->
          <section id="cost-tracker" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <DollarSign class="w-6 h-6 text-primary-600" /> Cost Tracker
            </h2>
            <p class="text-gray-700 mb-3">The Cost Tracker works the same as the free version — track development, infrastructure, vendor, and other costs per project. See the <router-link to="/docs/free#cost-tracker" class="text-primary-600 hover:underline">free docs</router-link> for the full guide.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Team Labor Rate Defaults</h3>
            <p class="text-gray-700">Set <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">avg_labor_cost_per_week</code> at the team level to standardize development cost calculations across all projects in that team. The labor rate fallback chain is: project-level rate → team-level rate → system default.</p>
          </section>

          <!-- Audit History -->
          <section id="audit" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <History class="w-6 h-6 text-primary-600" /> Audit History
            </h2>
            <p class="text-gray-700 mb-3">Every change to projects, assumptions, formulas, and costs is tracked in the audit history. This creates a defensible record of how ROI numbers evolved over time.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">What's Tracked</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Who</strong> — the user that made the change</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>What</strong> — the entity and field that changed</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>When</strong> — timestamp of the change</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Old → New values</strong> — the before and after values for each field</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Change reason</strong> — optional explanation of why the change was made</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Accessing Audit History</h3>
            <p class="text-gray-700">Click "Change History" on any project, formula, or assumption detail page. The history expands inline to show all changes with timestamps and user attribution.</p>

            <div class="mt-4 rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Plan availability:</strong> Audit trail is available on Growth and Enterprise plans.
              </p>
            </div>
          </section>

          <!-- Enterprise Features -->
          <section id="enterprise" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Shield class="w-6 h-6 text-primary-600" /> Enterprise Features
            </h2>

            <h3 class="text-lg font-semibold text-gray-900 mb-2">SSO (Single Sign-On)</h3>
            <p class="text-gray-700 mb-3">Authenticate users through your existing identity provider:</p>
            <ul class="space-y-2 text-gray-700 mb-4">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Google SSO</strong> — Available on Growth and Enterprise plans</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Okta / SAML</strong> — Available on Enterprise plan only</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Users authenticated via SSO are mapped to their existing ConfirmROI accounts</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mb-2">Scheduled Reports</h3>
            <p class="text-gray-700 mb-3">Automate ROI reporting with scheduled report delivery:</p>
            <ul class="space-y-2 text-gray-700 mb-4">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Schedule weekly or monthly ROI summary reports</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Reports delivered via email to specified recipients</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Available on Enterprise plan only</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mb-2">PDF Export</h3>
            <p class="text-gray-700 mb-3">Export ROI reports and project summaries as PDF documents for sharing with stakeholders who don't have ConfirmROI access. Available on Growth and Enterprise plans.</p>

            <h3 class="text-lg font-semibold text-gray-900 mb-2">Collaboration</h3>
            <p class="text-gray-700">Multiple managers can work on the same projects and assumptions. Shared assumptions ensure everyone uses consistent inputs. All changes are tracked in the audit trail.</p>
          </section>

          <!-- Support -->
          <section id="support" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <LifeBuoy class="w-6 h-6 text-primary-600" /> Support
            </h2>
            <ul class="space-y-3 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Starter:</strong> Email support. Response within 1-2 business days.</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Growth:</strong> Priority email support. Response within same business day.</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Enterprise:</strong> Dedicated support with a named contact. SLA-backed response times.</li>
            </ul>
            <p class="text-gray-700 mt-4">For self-hosting questions, see the <router-link to="/docs/free#self-hosting" class="text-primary-600 hover:underline">free docs self-hosting guide</router-link>. For open-source community support, visit <a href="https://github.com/confirmroi/confirmroi" class="text-primary-600 hover:underline">GitHub</a>.</p>
          </section>

          <!-- Footer note -->
          <div class="border-t border-gray-200 pt-8 mt-12">
            <div class="flex items-center gap-2 text-gray-500">
              <TrendingUp class="w-5 h-5" />
              <span class="text-sm">ConfirmROI is open-source software licensed under MIT. <a href="https://github.com/confirmroi/confirmroi" class="text-primary-600 hover:underline">View on GitHub</a> · <router-link to="/docs/free" class="text-primary-600 hover:underline">Free docs</router-link></span>
            </div>
          </div>
        </article>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>
