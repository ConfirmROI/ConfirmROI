<script setup>
import NavBar from '../components/NavBar.vue'
import SiteFooter from '../components/SiteFooter.vue'
import { TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Upload, FileText, Zap } from 'lucide-vue-next'

const sections = [
  { id: 'getting-started', label: 'Getting Started' },
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'teams', label: 'Teams' },
  { id: 'projects', label: 'Projects' },
  { id: 'formulas', label: 'Value Formulas' },
  { id: 'assumptions', label: 'Assumptions' },
  { id: 'roi', label: 'ROI Calculations' },
  { id: 'csv', label: 'CSV Import / Export' },
  { id: 'self-hosting', label: 'Self-Hosting' },
]
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-12">
        <!-- Sidebar TOC -->
        <aside class="hidden lg:block">
          <nav class="sticky top-24 space-y-1">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Contents</p>
            <a
              v-for="s in sections"
              :key="s.id"
              :href="`#${s.id}`"
              class="block text-sm text-gray-600 hover:text-primary-700 transition-colors py-1.5"
            >
              {{ s.label }}
            </a>
          </nav>
        </aside>

        <!-- Content -->
        <article class="prose prose-slate max-w-none">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Documentation</h1>
          <p class="text-gray-500 mb-8">Learn how to use ConfirmROI to measure and prove the value of your engineering initiatives.</p>

          <!-- Getting Started -->
          <section id="getting-started" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap class="w-6 h-6 text-primary-600" /> Getting Started
            </h2>
            <ol class="space-y-3 text-gray-700">
              <li class="flex gap-3">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">1</span>
                <div><strong>Create an account</strong> — Register at <router-link to="/register" class="text-primary-600 hover:underline">/register</router-link>. You'll start on the free tier with one team.</div>
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
            </ol>

            <div class="mt-6 rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Paid tier:</strong> Upgrading to paid unlocks unlimited teams, multi-team dashboards, and team-level project organization. The free tier includes a single auto-created team.
              </p>
            </div>
          </section>

          <!-- Dashboard -->
          <section id="dashboard" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <LayoutDashboard class="w-6 h-6 text-primary-600" /> Dashboard
            </h2>
            <p class="text-gray-700 mb-3">The Dashboard provides an at-a-glance view of your organization's projects and their ROI. You'll see:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Summary cards showing total projects, total ROI, and number of value formulas</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> A bar chart visualizing ROI across projects</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> A recent projects list with quick links to details (use the Projects page for full search)</li>
            </ul>
            <div class="mt-4 rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Paid tier:</strong> A team filter dropdown appears on the dashboard, letting you filter projects by team or view org-wide (all teams).
              </p>
            </div>
          </section>

          <!-- Teams -->
          <section id="teams" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Users class="w-6 h-6 text-primary-600" /> Teams
            </h2>
            <p class="text-gray-700 mb-3">Teams organize your projects. Every account gets at least one team.</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Create, edit, and delete teams from the Teams page</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Projects are assigned to a team on creation</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Team managers can create and manage projects within their team</li>
            </ul>
            <div class="mt-4 rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Paid tier:</strong> Create unlimited teams. Free tier is limited to a single auto-created team. The Teams page is only visible in the sidebar for paid users.
              </p>
            </div>
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
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Detail View:</strong> Click any project to see assigned formulas, assumptions, and ROI calculations</li>
            </ul>
            <p class="text-gray-700 mt-3">Project statuses: <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">planning</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">in_progress</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">completed</span>, <span class="font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">cancelled</span></p>
          </section>

          <!-- Value Formulas -->
          <section id="formulas" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Calculator class="w-6 h-6 text-primary-600" /> Value Formulas
            </h2>
            <p class="text-gray-700 mb-3">Value Formulas are ROI models that define <em>how</em> you calculate value. Each formula has a set of linked assumptions.</p>
            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">System Formulas</h3>
            <p class="text-gray-700 mb-3">ConfirmROI ships with four built-in formulas:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Cost Savings</strong> — Calculate ROI from reducing monthly operational costs</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Revenue Generation</strong> — Calculate ROI from new revenue generated</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Time Saved</strong> — Calculate ROI from hours saved multiplied by hourly rate</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Risk Reduction</strong> — Calculate ROI from reducing risk probability and impact</li>
            </ul>
            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Custom Formulas</h3>
            <p class="text-gray-700 mb-3">You can create your own formulas with custom expressions. When creating a formula:</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Provide a name, description, and formula (e.g. <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">hours_saved * hourly_rate - cost</code>)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Select which assumptions to link — assumptions are reusable across multiple formulas</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Formula variables must match the <code>key</code> of linked assumptions</li>
            </ul>
            <p class="text-gray-700 mt-3">You can edit and delete custom formulas. System formulas cannot be modified.</p>
          </section>

          <!-- Assumptions -->
          <section id="assumptions" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Lightbulb class="w-6 h-6 text-primary-600" /> Assumptions
            </h2>
            <p class="text-gray-700 mb-3">Assumptions are the input variables used by value formulas. They are <strong>standalone entities</strong> that can be shared across multiple formulas.</p>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Key:</strong> A unique identifier used in formulas (e.g. <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">hours_saved</code>)</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Label:</strong> Human-readable name shown in the UI</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Data Type:</strong> <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">number</code>, <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">currency</code>, or <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">percentage</code></li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Default Value:</strong> The starting value when a formula is assigned to a project</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> <strong>Description:</strong> Optional context for what the assumption represents</li>
            </ul>
            <p class="text-gray-700 mt-3">System assumptions (like <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">years</code> and <code class="text-sm bg-gray-100 px-1.5 py-0.5 rounded">implementation_cost</code>) are shared across multiple system formulas. You can create custom assumptions and link them to any formula from the Value Formulas page.</p>
          </section>

          <!-- ROI -->
          <section id="roi" class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Calculator class="w-6 h-6 text-primary-600" /> ROI Calculations
            </h2>
            <p class="text-gray-700 mb-3">To calculate ROI for a project:</p>
            <ol class="space-y-2 text-gray-700">
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">1</span> Open the project detail page</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">2</span> Click "Assign Formula" and choose a formula</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">3</span> Adjust the assumption values for this specific project — ROI updates live as you type</li>
              <li class="flex gap-3"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-700 text-sm font-bold flex items-center justify-center">4</span> The ROI value is calculated automatically and persisted to the backend</li>
            </ol>
            <p class="text-gray-700 mt-3">The ROI value updates instantly as you edit assumption values — no need to click a button. Changes are automatically persisted to the backend and displayed on the project detail page and the dashboard chart.</p>
            <p class="text-gray-700 mt-3">A project can have multiple formulas assigned — each with its own set of assumption values and ROI result.</p>
          </section>

          <!-- CSV -->
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

            <h3 class="text-lg font-semibold text-gray-900 mt-4 mb-2">Requirements</h3>
            <ul class="space-y-2 text-gray-700">
              <li class="flex gap-2"><span class="text-primary-600">•</span> Python 3.12+</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> Node.js 18+</li>
              <li class="flex gap-2"><span class="text-primary-600">•</span> PostgreSQL (production) or SQLite (development/testing)</li>
            </ul>

            <div class="mt-6 rounded-lg bg-blue-50 border border-blue-200 p-4">
              <p class="text-sm text-blue-900">
                <strong>Paid tier:</strong> The paid tier is configured via the <code class="text-sm bg-blue-100 px-1 py-0.5 rounded">DEFAULT_USER_TIER</code> environment variable. Set it to <code class="text-sm bg-blue-100 px-1 py-0.5 rounded">paid</code> to enable multi-team features, the Teams sidebar link, and org-wide dashboard filtering. The open-source version defaults to the free tier.
              </p>
            </div>
          </section>

          <!-- Footer note -->
          <div class="border-t border-gray-200 pt-8 mt-12">
            <div class="flex items-center gap-2 text-gray-500">
              <TrendingUp class="w-5 h-5" />
              <span class="text-sm">ConfirmROI is open-source software licensed under MIT. <a href="https://github.com/confirmroi/confirmroi" class="text-primary-600 hover:underline">View on GitHub</a></span>
            </div>
          </div>
        </article>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>
