import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    archetypes: [],
    projectArchetypes: [],
    roiResults: {},
    projectRoi: {},
    projectRoiBreakdown: {},
    usageStats: { assumptions: {}, archetypes: {} },
    loading: false,
    error: null,
  }),

  actions: {
    async fetchArchetypes() {
      this.loading = true
      try {
        const resp = await apiClient.get('/formulas')
        this.archetypes = resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch archetypes'
      } finally {
        this.loading = false
      }
    },

    async fetchUsage() {
      try {
        const resp = await apiClient.get('/formulas/usage')
        this.usageStats = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch usage stats'
        return null
      }
    },

    async fetchArchetype(id) {
      try {
        const resp = await apiClient.get(`/formulas/${id}`)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch archetype'
        return null
      }
    },

    async createArchetype(data) {
      try {
        const resp = await apiClient.post('/formulas', data)
        this.archetypes.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create archetype'
        return null
      }
    },

    async deleteArchetype(id) {
      try {
        await apiClient.delete(`/formulas/${id}`)
        this.archetypes = this.archetypes.filter((a) => a.id !== id)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to delete archetype'
        return false
      }
    },

    async updateArchetype(id, data) {
      try {
        const resp = await apiClient.put(`/formulas/${id}`, data)
        const idx = this.archetypes.findIndex((a) => a.id === id)
        if (idx !== -1) this.archetypes[idx] = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update archetype'
        return null
      }
    },

    async assignArchetype(projectId, archetypeId) {
      try {
        const resp = await apiClient.post(`/projects/${projectId}/formulas`, { archetype_id: archetypeId })
        this.projectArchetypes.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to assign archetype'
        return null
      }
    },

    async unassignArchetype(projectId, paId) {
      try {
        await apiClient.delete(`/projects/${projectId}/formulas/${paId}`)
        this.projectArchetypes = this.projectArchetypes.filter((pa) => pa.id !== paId)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to unassign archetype'
        return false
      }
    },

    async fetchProjectArchetypes(projectId) {
      try {
        const resp = await apiClient.get(`/projects/${projectId}/formulas`)
        this.projectArchetypes = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch project archetypes'
        return null
      }
    },

    async updateAssumptionValue(projectId, paId, assumptionId, value) {
      try {
        const resp = await apiClient.put(
          `/projects/${projectId}/formulas/${paId}/assumptions/${assumptionId}`,
          { value }
        )
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update assumption'
        return null
      }
    },

    async calculateRoi(projectId, paId) {
      try {
        const resp = await apiClient.post(`/projects/${projectId}/formulas/${paId}/calculate`)
        this.roiResults[paId] = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to calculate ROI'
        return null
      }
    },

    async getLatestRoi(projectId, paId) {
      try {
        const resp = await apiClient.get(`/projects/${projectId}/formulas/${paId}/roi`)
        this.roiResults[paId] = resp.data
        return resp.data
      } catch (err) {
        return null
      }
    },

    async fetchProjectRoi(projects) {
      this.projectRoi = {}
      this.projectRoiBreakdown = {}
      for (const project of projects) {
        try {
          const resp = await apiClient.get(`/projects/${project.id}/formulas`)
          const pas = resp.data || []
          let total = 0
          const breakdown = {}
          for (const pa of pas) {
            const roi = await this.getLatestRoi(project.id, pa.id)
            if (roi && typeof roi.roi_value === 'number') {
              total += roi.roi_value
              const name = pa.formula?.name || 'Unknown'
              breakdown[name] = (breakdown[name] || 0) + roi.roi_value
            }
          }
          this.projectRoi[project.id] = total
          this.projectRoiBreakdown[project.id] = breakdown
        } catch {
          this.projectRoi[project.id] = 0
          this.projectRoiBreakdown[project.id] = {}
        }
      }
    },
  },
})
