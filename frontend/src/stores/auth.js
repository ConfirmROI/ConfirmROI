import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userName: (state) => state.user?.name || '',
    userTier: (state) => state.user?.tier || 'free',
  },

  actions: {
    async register(email, password, name) {
      this.loading = true
      this.error = null
      try {
        const resp = await apiClient.post('/auth/register', { email, password, name })
        this._setTokens(resp.data)
        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const resp = await apiClient.post('/auth/login', { email, password })
        this._setTokens(resp.data)
        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async autoLogin() {
      this.loading = true
      this.error = null
      try {
        const resp = await apiClient.post('/auth/auto-login')
        this._setTokens(resp.data)
        this.user = resp.data.user
        return true
      } catch (err) {
        this.error = err.response?.data?.error || 'Auto-login failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        const resp = await apiClient.get('/auth/me')
        this.user = resp.data
      } catch {
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    _setTokens(data) {
      this.token = data.access_token
      this.refreshToken = data.refresh_token
      localStorage.setItem('access_token', data.access_token)
      if (data.refresh_token) {
        localStorage.setItem('refresh_token', data.refresh_token)
      }
    },
  },
})
