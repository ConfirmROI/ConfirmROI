import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useCostsStore = defineStore('costs', {
  state: () => ({
    costs: [],
    loading: false,
    error: null,
  }),

  getters: {
    totalCost: (state) => {
      // First-year investment: one_time + recurring_monthly*12 + recurring_annual
      return state.costs.reduce((sum, c) => {
        const amt = c.amount || 0
        const ct = c.cost_type || 'one_time'
        if (ct === 'recurring_monthly') return sum + amt * 12
        if (ct === 'recurring_annual') return sum + amt
        return sum + amt
      }, 0)
    },
    recurringAnnualCost: (state) => {
      // Annual recurring cost (for 3-year display): recurring_monthly*12 + recurring_annual
      return state.costs.reduce((sum, c) => {
        const amt = c.amount || 0
        const ct = c.cost_type || 'one_time'
        if (ct === 'recurring_monthly') return sum + amt * 12
        if (ct === 'recurring_annual') return sum + amt
        return sum
      }, 0)
    },
    oneTimeCost: (state) => {
      return state.costs
        .filter(c => (c.cost_type || 'one_time') === 'one_time')
        .reduce((sum, c) => sum + (c.amount || 0), 0)
    },
    developmentCost: (state) => {
      const dev = state.costs.find(c => c.category === 'development')
      return dev ? dev.amount : 0
    },
  },

  actions: {
    async fetchCosts(projectId) {
      this.loading = true
      try {
        const resp = await apiClient.get(`/projects/${projectId}/costs`)
        this.costs = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch costs'
        return []
      } finally {
        this.loading = false
      }
    },

    async createCost(projectId, data) {
      try {
        const resp = await apiClient.post(`/projects/${projectId}/costs`, data)
        this.costs.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create cost'
        return null
      }
    },

    async updateCost(projectId, costId, data) {
      try {
        const resp = await apiClient.put(`/projects/${projectId}/costs/${costId}`, data)
        const idx = this.costs.findIndex(c => c.id === costId)
        if (idx !== -1) this.costs[idx] = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update cost'
        return null
      }
    },

    async deleteCost(projectId, costId) {
      try {
        await apiClient.delete(`/projects/${projectId}/costs/${costId}`)
        this.costs = this.costs.filter(c => c.id !== costId)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to delete cost'
        return false
      }
    },
  },
})
