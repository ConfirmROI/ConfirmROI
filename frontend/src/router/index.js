import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomePageV2.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('../views/Projects.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/projects/:id',
    name: 'project-detail',
    component: () => import('../views/ProjectDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/formulas',
    name: 'formulas',
    component: () => import('../views/Archetypes.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/formulas/:id',
    name: 'formula-detail',
    component: () => import('../views/ArchetypeDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/assumptions',
    name: 'assumptions',
    component: () => import('../views/Assumptions.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/assumptions/:id',
    name: 'assumption-detail',
    component: () => import('../views/AssumptionDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/teams',
    name: 'teams',
    component: () => import('../views/Teams.vue'),
    meta: { requiresAuth: true, requiresPaid: true },
  },
  {
    path: '/docs',
    name: 'docs',
    component: () => import('../views/DocsHub.vue'),
  },
  {
    path: '/docs/free',
    name: 'docs-free',
    component: () => import('../views/DocsFree.vue'),
  },
  {
    path: '/docs/paid',
    name: 'docs-paid',
    component: () => import('../views/DocsPaid.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (auth.token && !auth.user) {
    await auth.fetchUser()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    const success = await auth.autoLogin()
    if (!success) {
      return { name: 'login' }
    }
  }

  if (to.meta.requiresPaid && auth.userTier !== 'paid') {
    return { name: 'dashboard' }
  }
})

export default router
