<script setup>
import NavBar from '../components/NavBar.vue'
import SiteFooter from '../components/SiteFooter.vue'
import DocsSidebar from '../components/DocsSidebar.vue'
import {
  TrendingUp, Zap, LayoutDashboard, FolderKanban, Calculator,
  Lightbulb, DollarSign, Upload, FileText, BarChart3,
} from 'lucide-vue-next'

const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'getting-started', label: 'Getting Started' },
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'projects', label: 'Projects' },
  { id: 'formulas', label: 'Value Formulas' },
  { id: 'assumptions', label: 'Assumptions' },
  { id: 'roi', label: 'ROI Calculations' },
  { id: 'cost-tracker', label: 'Cost Tracker / Investment' },
  { id: 'csv', label: 'CSV Import / Export' },
  { id: 'self-hosting', label: 'Self-Hosting' },
]

const systemFormulas = [
  {
    name: 'Cost Savings',
    description: 'Annual ROI from reducing monthly operational costs.',
    formula: '(monthly_cost_before - monthly_cost_after) * 12 - implementation_cost',
    assumptions: ['monthly_cost_before', 'monthly_cost_after', 'implementation_cost'],
    useCase: 'Cloud migration, vendor renegotiation, infrastructure consolidation.',
  },
  {
    name: 'Revenue Generation',
    description: 'Annual ROI from generating new revenue.',
    formula: 'estimated_monthly_revenue * 12 - implementation_cost',
    assumptions: ['estimated_monthly_revenue', 'implementation_cost'],
    useCase: 'New product features, monetization changes, conversion rate improvements.',
  },
  {
    name: 'Time Saved',
    description: 'Annual ROI from time savings converted to dollar value.',
    formula: 'hours_saved_per_week * 52 * hourly_rate - implementation_cost',
    assumptions: ['hours_saved_per_week', 'hourly_rate', 'implementation_cost'],
    useCase: 'Automation, tooling improvements, process optimization.',
  },
  {
    name: 'Risk Reduction',
    description: 'Annual ROI from reducing risk probability and impact.',
    formula: 'risk_probability * risk_impact - implementation_cost',
    assumptions: ['risk_probability', 'risk_impact', 'implementation_cost'],
    useCase: 'Security hardening, compliance initiatives, disaster recovery.',
  },
  {
    name: 'Velocity Multiplier',
    description: 'Structural improvements that compound across many engineers\' delivery speed, valued as a fraction of their total cost.',
    formula: 'ic_count * uplift_pct * eng_cost * realization * ramp_factor * attribution',
    assumptions: ['ic_count', 'uplift_pct', 'eng_cost', 'realization', 'ramp_factor', 'attribution'],
    useCase: 'CI/CD improvements, dev environment upgrades, framework migrations that speed up delivery.',
  },
  {
    name: 'Enabler / Option Value',
    description: 'No direct cash value — the initiative unlocks downstream projects that do. Value is attributed upstream.',
    formula: 'downstream_npv_total * enabler_attr / horizon_years',
    assumptions: ['downstream_npv_total', 'enabler_attr', 'horizon_years'],
    useCase: 'Platform investments, API design, data migrations that enable future projects.',
  },
  {
    name: 'Reputation Shield',
    description: 'Reducing incident frequency to avoid erosion of partner and dealer trust — churn and deal-flow loss that follows reliability failures.',
    formula: 'delta_incidents_per_year * p_partner_impact * (p_churn * avg_partner_arr + p_vol_reduction * avg_vol_reduction_rev) * realization',
    assumptions: ['delta_incidents_per_year', 'p_partner_impact', 'p_churn', 'avg_partner_arr', 'p_vol_reduction', 'avg_vol_reduction_rev', 'realization'],
    useCase: 'Reliability improvements, on-call automation, monitoring investments.',
  },
  {
    name: 'Support / KTLO',
    description: 'A deliberate capacity allocation decision, not a value-generation initiative. Cost = Opportunity, net ROI is zero by design.',
    formula: 'team_cost * (capacity / headcount)',
    assumptions: ['team_cost', 'capacity', 'headcount'],
    useCase: 'Keep-the-lights-on work, support rotations, maintenance — track the opportunity cost of allocated capacity.',
  },
]

const systemAssumptions = [
  { key: 'monthly_cost_before', label: 'Monthly Cost Before', type: 'currency', default: '$10,000', description: 'Monthly cost before the project' },
  { key: 'monthly_cost_after', label: 'Monthly Cost After', type: 'currency', default: '$5,000', description: 'Expected monthly cost after the project' },
  { key: 'implementation_cost', label: 'Implementation Cost', type: 'currency', default: '$25,000', description: 'One-time implementation cost' },
  { key: 'estimated_monthly_revenue', label: 'Estimated Monthly Revenue', type: 'currency', default: '$8,000', description: 'Estimated new monthly revenue from the project' },
  { key: 'hours_saved_per_week', label: 'Hours Saved Per Week', type: 'number', default: '20', description: 'Hours saved per week across the team' },
  { key: 'hourly_rate', label: 'Hourly Rate', type: 'currency', default: '$75', description: 'Average hourly rate of saved labor' },
  { key: 'risk_probability', label: 'Risk Probability', type: 'percentage', default: '30%', description: 'Annual probability of the risk event (0-1)' },
  { key: 'risk_impact', label: 'Risk Impact ($)', type: 'currency', default: '$100,000', description: 'Financial impact if the risk event occurs' },
  { key: 'realization', label: 'Realization', type: 'percentage', default: '60%', description: 'Fraction of the estimated value that actually materializes' },
  { key: 'ic_count', label: 'IC Count', type: 'number', default: '50', description: 'Number of individual contributors affected by the initiative' },
  { key: 'uplift_pct', label: 'Uplift %', type: 'percentage', default: '2%', description: 'Delivery speed increase as a decimal (e.g., 0.02 for 2%)' },
  { key: 'eng_cost', label: 'Engineer Cost', type: 'currency', default: '$180,000', description: 'Fully loaded annual engineering cost' },
  { key: 'ramp_factor', label: 'Ramp Factor', type: 'percentage', default: '75%', description: 'Year-1 discount for adoption lag' },
  { key: 'attribution', label: 'Attribution', type: 'percentage', default: '50%', description: 'Haircut when multiple teams share credit (0.5 if co-owned)' },
  { key: 'downstream_npv_total', label: 'Downstream NPV Total', type: 'currency', default: '$500,000', description: 'Sum of downstream NPV x P(ships) across dependent projects' },
  { key: 'enabler_attr', label: 'Enabler Attribution', type: 'percentage', default: '20%', description: 'Attribution percentage credited to this enabler (default 20%, cap 30%)' },
  { key: 'horizon_years', label: 'Horizon Years', type: 'number', default: '3', description: 'Amortization period in years' },
  { key: 'delta_incidents_per_year', label: 'Incident Reduction (per year)', type: 'number', default: '8', description: 'Reduction in major incidents per year' },
  { key: 'p_partner_impact', label: 'Partner Impact Probability', type: 'percentage', default: '50%', description: 'Probability a given incident generates partner escalation or friction' },
  { key: 'p_churn', label: 'Partner Churn Probability', type: 'percentage', default: '5%', description: 'Probability of partner churn given impact' },
  { key: 'avg_partner_arr', label: 'Average Partner ARR', type: 'currency', default: '$1,500,000', description: 'Revenue at risk per churned partner' },
  { key: 'p_vol_reduction', label: 'Volume Reduction Probability', type: 'percentage', default: '30%', description: 'Probability of deal-flow reduction short of churn' },
  { key: 'avg_vol_reduction_rev', label: 'Average Volume Reduction Revenue', type: 'currency', default: '$40,000', description: 'Revenue impact of deal-flow reduction short of churn' },
  { key: 'team_cost', label: 'Team Cost', type: 'currency', default: '$979,000', description: 'Fully loaded annual cost of the team' },
  { key: 'capacity', label: 'Allocated Capacity', type: 'number', default: '1', description: 'Number of engineers allocated to this function' },
  { key: 'headcount', label: 'Team Headcount', type: 'number', default: '4', description: 'Total engineers on the team' },
]
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-12">
        <DocsSidebar :sections="sections" />

        <article class="prose prose-slate max-w-none">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Free (Open Source) Documentation</h1>
          <p class="text-gray-500 mb-8">Self-host ConfirmROI to measure and prove the value of your engineering initiatives.</p>

          <!-- Overview -->
          <section id="overview" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <TrendingUp class="w-6 h-6 text-primary-600" /> Overview
            </h2>
            <p class="text-gray-700 mb-3">
              Engineering leaders struggle to prove the value of complex work — risk reduction, velocity improvements,
              enabler projects, keep-the-lights-on investments. Traditional ROI tools are built for sales and finance,
              not engineering. Spreadsheets are error-prone and hard to defend.
            </p>
            <p class="text-gray-700 mb-3">
              ConfirmROI solves this with <strong>transparent, defensible formulas</strong> instead of gut feelings.
              Each value formula is an open expression you can inspect, edit, and audit. Assumptions are explicit
              inputs with defaults you can override per project. The result is an ROI number your stakeholders can
              trace from formula to assumption to source data.
            </p>
            <p class="text-gray-700">
              The free open-source version is fully functional for a single manager and team. You get all 8 system
              formulas, 26 system assumptions, cost tracking, CSV import/export, and Jira integration. No feature
              is locked behind a paywall — the paid version adds <em>collaboration</em> features (multi-team, SSO,
              audit trails) rather than crippling the core.
            </p>
          </section>

          <!-- Getting Started -->
          <section id="getting-started" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap class="w-6 h-6 text-primary-600" /> Getting Started
            </h2>
            <ol class="space-y-3 text-gray-700">
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">1</span>
                <div><strong>Download the software</strong> — Available on GitHub at <a href="https://github.com/ConfirmROI/ConfirmROI" target="_blank" class="text-primary-600 hover:underline">https://github.com/ConfirmROI/ConfirmROI</a>.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">2</span>
                <div><strong>Explore the Dashboard</strong> — After logging in, you'll see an overview of your projects and ROI summaries.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">3</span>
                <div><strong>Create a Project</strong> — Go to Projects and click "New Project" to add your first initiative.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">4</span>
                <div><strong>Assign a Formula</strong> — Open a project, assign a value formula (e.g. Cost Savings), adjust assumptions, and calculate ROI.</div>
              </li>
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">5</span>
                <div><strong>Track Costs</strong> — Add development, infrastructure, vendor, or other cost entries to capture your full investment.</div>
              </li>
            </ol>
          </section>

          <!-- Dashboard -->
          <section id="dashboard" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <LayoutDashboard class="w-6 h-6 text-primary-600" /> Dashboard
            </h2>
            <p class="text-gray-700 mb-3">The Dashboard provides an at-a-glance view of your projects and their ROI. You'll see:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Summary cards</strong> showing total projects, total ROI, and number of value formulas</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>ROI bar chart</strong> visualizing ROI across projects, with a formula breakdown</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Recent projects list</strong> with quick links to project details</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Date range filtering</strong> — filter by start and end dates to focus on a specific period</li>
            </ul>
          </section>

          <!-- Projects -->
          <section id="projects" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FolderKanban class="w-6 h-6 text-primary-600" /> Projects
            </h2>
            <p class="text-gray-700 mb-3">Projects represent your engineering initiatives. Each project can have multiple value formulas assigned to it.</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Create:</strong> Click "New Project" and fill in name, description, team, and status</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Edit / Delete:</strong> Use the pencil/trash icons on the project detail page</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Search:</strong> Use the search bar on the Projects page to filter by name</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Detail View:</strong> Click any project to see assigned formulas, assumptions, ROI calculations, and cost tracker</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>External source tags:</strong> Projects imported from Jira or CSV are tagged with their source</li>
            </ul>
            <p class="text-gray-700 mt-3">Project statuses: <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">planning</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">in_progress</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">completed</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">cancelled</span></p>
          </section>

          <!-- Value Formulas -->
          <section id="formulas" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Calculator class="w-6 h-6 text-primary-600" /> Value Formulas
            </h2>
            <p class="text-gray-700 mb-3">Value Formulas are ROI models that define <em>how</em> you calculate value. Each formula has a set of linked assumptions whose values you adjust per project.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">System Formulas (8 built-in)</h3>
            <div class="space-y-4">
              <div v-for="f in systemFormulas" :key="f.name" class="border border-gray-200 rounded-lg p-4">
                <h4 class="font-semibold text-gray-900">{{ f.name }}</h4>
                <p class="text-sm text-gray-600 mt-1">{{ f.description }}</p>
                <p class="text-xs text-gray-500 mt-2"><strong>Use case:</strong> {{ f.useCase }}</p>
                <pre class="bg-gray-900 text-gray-100 rounded-lg p-3 text-xs mt-3 overflow-x-auto"><code>{{ f.formula }}</code></pre>
                <p class="text-xs text-gray-500 mt-2">Assumptions: <code class="text-xs bg-gray-100 px-1 py-0.5 rounded">{{ f.assumptions.join(', ') }}</code></p>
              </div>
            </div>

            <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">Custom Formulas</h3>
            <p class="text-gray-700 mb-3">You can create your own formulas with custom expressions. When creating a formula:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Provide a name, description, and formula expression (e.g. <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">hours_saved * hourly_rate - cost</code>)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Select which assumptions to link — assumptions are reusable across multiple formulas</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Formula variables must match the <code>key</code> of linked assumptions</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Expressions are evaluated with <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">simpleeval</code> — standard arithmetic, comparison, and boolean operators are supported</li>
            </ul>
            <p class="text-gray-700 mt-3">You can edit and delete custom formulas. System formulas cannot be modified.</p>
          </section>

          <!-- Assumptions -->
          <section id="assumptions" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Lightbulb class="w-6 h-6 text-primary-600" /> Assumptions
            </h2>
            <p class="text-gray-700 mb-3">Assumptions are the input variables used by value formulas. They are <strong>standalone entities</strong> that can be shared across multiple formulas.</p>
            <ul class="space-y-2 text-gray-700 mb-4">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Key:</strong> A unique identifier used in formulas (e.g. <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">hours_saved</code>)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Label:</strong> Human-readable name shown in the UI</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Data Type:</strong> <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">number</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">currency</code>, or <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">percentage</code></li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Default Value:</strong> The starting value when a formula is assigned to a project</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Description:</strong> Optional context for what the assumption represents</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">System Assumptions (26 built-in)</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-sm border-collapse">
                <thead>
                  <tr class="border-b-2 border-gray-200 bg-gray-50">
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Key</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Label</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Type</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Default</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in systemAssumptions" :key="a.key" class="border-b border-gray-100">
                    <td class="py-2 px-3 font-mono text-xs text-gray-600">{{ a.key }}</td>
                    <td class="py-2 px-3 text-gray-700">{{ a.label }}</td>
                    <td class="py-2 px-3"><span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">{{ a.type }}</span></td>
                    <td class="py-2 px-3 text-gray-700">{{ a.default }}</td>
                    <td class="py-2 px-3 text-xs text-gray-500">{{ a.description }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">Custom Assumptions</h3>
            <p class="text-gray-700">Create custom assumptions from the Assumptions page. Provide a key (used in formula expressions), label, data type, and default value. Custom assumptions can be linked to any formula — system or custom.</p>
          </section>

          <!-- ROI Calculations -->
          <section id="roi" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 class="w-6 h-6 text-primary-600" /> ROI Calculations
            </h2>
            <p class="text-gray-700 mb-3">To calculate ROI for a project:</p>
            <ol class="space-y-2 text-gray-700">
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">1</span> Open the project detail page</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">2</span> Click "Assign Formula" and choose a formula</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">3</span> Adjust the assumption values for this specific project — ROI updates live as you type</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">4</span> The ROI value is calculated automatically and persisted to the backend</li>
            </ol>
            <p class="text-gray-700 mt-3">The ROI value updates instantly as you edit assumption values (debounced) — no need to click a button. Changes are automatically persisted and displayed on the project detail page and the dashboard chart.</p>
            <p class="text-gray-700 mt-3">A project can have multiple formulas assigned — each with its own set of assumption values and ROI result.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">ROI Summary</h3>
            <p class="text-gray-700 mb-3">The project detail page includes an ROI Summary that shows:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>1-year ROI</strong> — total value minus implementation cost over one year</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>3-year ROI</strong> — total value minus costs over three years (accounts for recurring costs)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Investment multiples</strong> — ratio of value to investment (e.g. 3x means $3 returned per $1 invested)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>One-time vs recurring cost breakdown</strong> — separates implementation costs from ongoing operational costs</li>
            </ul>
          </section>

          <!-- Cost Tracker -->
          <section id="cost-tracker" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <DollarSign class="w-6 h-6 text-primary-600" /> Cost Tracker / Investment
            </h2>
            <p class="text-gray-700 mb-3">The Cost Tracker lets you capture the full investment behind each project. Costs are tracked per project and feed into the ROI Summary for accurate ROI calculations.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Cost Categories</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Development</strong> — Enter person-weeks; the amount is auto-calculated from the labor rate</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Infrastructure</strong> — Direct dollar amount (e.g. cloud hosting, licensing)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Vendor</strong> — Direct dollar amount (e.g. contractor, consultant fees)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Other</strong> — Any other cost not covered above</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Cost Types</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>One-time</strong> — A single payment (e.g. implementation, setup)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Recurring (monthly)</strong> — Ongoing monthly cost (e.g. SaaS subscription)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Recurring (annual)</strong> — Ongoing annual cost (e.g. license renewal)</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Estimate vs Actual</h3>
            <p class="text-gray-700 mb-3">Each cost entry can be flagged as an <strong>estimate</strong> or <strong>actual</strong>. Track estimates during planning, then update to actuals once costs are known.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Labor Rate</h3>
            <p class="text-gray-700">For development costs, the labor rate determines the dollar amount from person-weeks. The rate falls back through this chain: project-level rate → team-level rate (<code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">avg_labor_cost_per_week</code>) → system default.</p>
          </section>

          <!-- CSV Import / Export -->
          <section id="csv" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Upload class="w-6 h-6 text-primary-600" /> CSV Import / Export
            </h2>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Importing Projects</h3>
            <p class="text-gray-700 mb-3">Bulk import projects from a CSV file:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Click "Import CSV" on the Projects page to bulk-import projects</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Projects are imported into your current team automatically</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Upload a CSV with columns: <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">name</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">description</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">external_id</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">status</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">start_date</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">end_date</code></li>
            </ul>
            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Exporting Projects</h3>
            <p class="text-gray-700 mb-3">Export all projects for your team to CSV, including ROI data. Click "Export CSV" on the Projects page.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Jira Integration</h3>
            <p class="text-gray-700 mb-3">Connect Jira to import projects via the REST API:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Set up a Jira connection with your API token (team-level setting)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Import projects from Jira into your team</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Imported projects are tagged with their Jira source</li>
            </ul>
          </section>

          <!-- Self-Hosting -->
          <section id="self-hosting" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FileText class="w-6 h-6 text-primary-600" /> Self-Hosting
            </h2>
            <p class="text-gray-700 mb-3">ConfirmROI is open-source under the MIT license. You can self-host it with Docker or manually.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Docker (recommended)</h3>
            <pre class="bg-gray-900 text-gray-100 rounded-lg p-4 text-sm overflow-x-auto"><code>cp .env.example .env
docker-compose up --build</code></pre>
            <p class="text-gray-700 mt-2">Frontend will be available at <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">http://localhost:5173</code> and the API at <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">http://localhost:5000/api</code>.</p>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Manual Setup</h3>
            <p class="text-sm font-semibold text-gray-700 mb-1">Backend:</p>
            <pre class="bg-gray-900 text-gray-100 rounded-lg p-4 text-sm overflow-x-auto"><code>cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app wsgi db upgrade
python -m app.services.seed
flask --app wsgi run</code></pre>
            <p class="text-sm font-semibold text-gray-700 mt-3 mb-1">Frontend:</p>
            <pre class="bg-gray-900 text-gray-100 rounded-lg p-4 text-sm overflow-x-auto"><code>cd frontend
npm install
npm run dev</code></pre>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Environment Variables</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-sm border-collapse">
                <thead>
                  <tr class="border-b-2 border-gray-200 bg-gray-50">
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Variable</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Default</th>
                    <th class="text-left py-2 px-3 font-semibold text-gray-700">Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">FLASK_CONFIG</td><td class="py-2 px-3 text-gray-600">development</td><td class="py-2 px-3 text-xs text-gray-500">Flask config name</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">SECRET_KEY</td><td class="py-2 px-3 text-gray-600">dev-secret</td><td class="py-2 px-3 text-xs text-gray-500">Flask secret key — change in production</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">JWT_SECRET_KEY</td><td class="py-2 px-3 text-gray-600">jwt-dev-secret</td><td class="py-2 px-3 text-xs text-gray-500">JWT signing key — change in production</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">DATABASE_URL</td><td class="py-2 px-3 text-gray-600">sqlite:///confirmroi.db</td><td class="py-2 px-3 text-xs text-gray-500">Database URL (use postgresql:// for production)</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">VITE_API_URL</td><td class="py-2 px-3 text-gray-600">http://localhost:5000/api</td><td class="py-2 px-3 text-xs text-gray-500">Backend API URL for the frontend</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">VITE_IS_PAID</td><td class="py-2 px-3 text-gray-600">false</td><td class="py-2 px-3 text-xs text-gray-500">Set to "true" for the paid SaaS version (shows plan selection on register)</td></tr>
                  <tr class="border-b border-gray-100"><td class="py-2 px-3 font-mono text-xs">DEFAULT_USER_TIER</td><td class="py-2 px-3 text-gray-600">free</td><td class="py-2 px-3 text-xs text-gray-500">Tier assigned to newly registered users</td></tr>
                </tbody>
              </table>
            </div>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Requirements</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Python 3.12+</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Node.js 18+</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> PostgreSQL (production) or SQLite (development/testing)</li>
            </ul>

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Demo Mode</h3>
            <p class="text-gray-700 mb-3">Demo deployments with pre-seeded data are available via Docker Compose overrides:</p>
            <pre class="bg-gray-900 text-gray-100 rounded-lg p-4 text-sm overflow-x-auto"><code># Free tier demo
docker-compose -f docker-compose.yml -f docker-compose.demo-free.yml up --build

# Paid tier demo
docker-compose -f docker-compose.yml -f docker-compose.demo-paid.yml up --build</code></pre>
            <p class="text-gray-700 mt-2">Set <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">DEMO_TIER=free</code> or <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">DEMO_TIER=paid</code> to control which users, teams, and projects are seeded.</p>
          </section>

          <!-- Footer note -->
          <div class="border-t border-gray-200 pt-8 mt-12">
            <div class="flex items-center gap-2 text-gray-500">
              <TrendingUp class="w-5 h-5" />
              <span class="text-sm">ConfirmROI is open-source software licensed under MIT. <a href="https://github.com/confirmroi/confirmroi" class="text-primary-600 hover:underline">View on GitHub</a> · <router-link to="/docs/paid" class="text-primary-600 hover:underline">Paid docs</router-link></span>
            </div>
          </div>
        </article>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>
