import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchTeams() {
      this.loading = true
      try {
        const resp = await apiClient.get('/teams')
        this.teams = resp.data
      } catch {
        try {
          const resp = await apiClient.get('/projects/teams')
          this.teams = resp.data
        } catch (err) {
          this.teams = []
          this.error = err.response?.data?.error || 'Failed to fetch teams'
        }
      } finally {
        this.loading = false
      }
    },

    async createTeam(data) {
      try {
        const resp = await apiClient.post('/teams', data)
        this.teams.push(resp.data)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create team'
        return null
      }
    },

    async updateTeam(id, data) {
      try {
        const resp = await apiClient.put(`/teams/${id}`, data)
        const idx = this.teams.findIndex((t) => t.id === id)
        if (idx !== -1) this.teams[idx] = resp.data
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to update team'
        return null
      }
    },

    async deleteTeam(id) {
      try {
        await apiClient.delete(`/teams/${id}`)
        this.teams = this.teams.filter((t) => t.id !== id)
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to delete team'
        return false
      }
    },

    async fetchTeamMembers(teamId) {
      try {
        const resp = await apiClient.get(`/teams/${teamId}/members`)
        return resp.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch team members'
        return []
      }
    },
  },
})
