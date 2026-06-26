import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: [],
    currentProject: null,
    loading: false,
    error: null,
    viewMode: 'cards',
  }),

  getters: {
    projectCount: (state) => state.projects.length,
  },

  actions: {
    async fetchProjects(teamId, dateRange, includeRoi = false, managedOnly = false) {
      this.loading = true
      try {
        const params = {}
        if (teamId) params.team_id = teamId
        if (managedOnly) params.managed_only = 'true'
        if (dateRange) {
          if (dateRange.start) params.start_date = dateRange.start
          if (dateRange.end) params.end_date = dateRange.end
        }
        if (includeRoi) params.include_roi = 'true'
        const resp = await apiClient.get('/projects', { params })
        this.projects = resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch projects'
      } finally {
        this.loading = false
      }
    },

    async fetchProject(id) {
      this.loading = true
      try {
        const resp = await apiClient.get(`/projects/${id}`)
        this.currentProject = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch project'
        return null
      } finally {
        this.loading = false
      }
    },

    async createProject(data) {
      try {
        const resp = await apiClient.post('/projects', data)
        this.projects.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create project'
        return null
      }
    },

    async updateProject(id, data) {
      try {
        const resp = await apiClient.put(`/projects/${id}`, data)
        const idx = this.projects.findIndex((p) => p.id === id)
        if (idx !== -1) {
          const existing = this.projects[idx]
          this.projects[idx] = { ...resp.data, roi_1yr: existing.roi_1yr, roi_3yr: existing.roi_3yr }
        }
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update project'
        return null
      }
    },

    async deleteProject(id) {
      try {
        await apiClient.delete(`/projects/${id}`)
        this.projects = this.projects.filter((p) => p.id !== id)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to delete project'
        return false
      }
    },

    async importCsv(teamId, csvContent) {
      try {
        const resp = await apiClient.post(
          `/projects/import?team_id=${teamId}`,
          csvContent,
          { headers: { 'Content-Type': 'text/csv' } }
        )
        await this.fetchProjects(teamId, null, this.viewMode === 'table')
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'CSV import failed'
        return null
      }
    },
  },
})
