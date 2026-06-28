import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useAssumptionsStore = defineStore('assumptions', {
  state: () => ({
    assumptions: [],
    archetypes: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAssumptions() {
      this.loading = true
      try {
        const resp = await apiClient.get('/formulas/assumptions')
        this.assumptions = resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch assumptions'
      } finally {
        this.loading = false
      }
    },

    async fetchArchetypes() {
      try {
        const resp = await apiClient.get('/formulas')
        this.archetypes = resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch archetypes'
      }
    },

    async createAssumption(data) {
      try {
        const resp = await apiClient.post('/formulas/assumptions', data)
        this.assumptions.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create assumption'
        return null
      }
    },

    async updateAssumption(assumptionId, data) {
      try {
        const resp = await apiClient.put(`/formulas/assumptions/${assumptionId}`, data)
        const idx = this.assumptions.findIndex((a) => a.id === assumptionId)
        if (idx !== -1) this.assumptions[idx] = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update assumption'
        return null
      }
    },

    async deleteAssumption(assumptionId) {
      try {
        await apiClient.delete(`/formulas/assumptions/${assumptionId}`)
        this.assumptions = this.assumptions.filter((a) => a.id !== assumptionId)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to delete assumption'
        return false
      }
    },
  },
})
