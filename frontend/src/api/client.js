import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken && !error.config._retry) {
        error.config._retry = true
        try {
          const resp = await axios.post(
            `${apiClient.defaults.baseURL}/auth/refresh`,
            {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          )
          const newToken = resp.data.access_token
          localStorage.setItem('access_token', newToken)
          error.config.headers.Authorization = `Bearer ${newToken}`
          return apiClient(error.config)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          try {
            const autoResp = await axios.post(`${apiClient.defaults.baseURL}/auth/auto-login`)
            localStorage.setItem('access_token', autoResp.data.access_token)
            if (autoResp.data.refresh_token) {
              localStorage.setItem('refresh_token', autoResp.data.refresh_token)
            }
            error.config.headers.Authorization = `Bearer ${autoResp.data.access_token}`
            return apiClient(error.config)
          } catch {
            window.location.href = '/login'
          }
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
