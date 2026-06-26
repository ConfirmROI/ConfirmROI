import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../auth'
import apiClient from '../../api/client'

vi.mock('../../api/client', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } },
  },
}))

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('initializes with no token', () => {
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.user).toBe(null)
  })

  it('logout clears state and localStorage', () => {
    const auth = useAuthStore()
    auth.token = 'fake-token'
    auth.user = { name: 'Test', email: 'test@test.com' }
    localStorage.setItem('access_token', 'fake-token')

    auth.logout()

    expect(auth.token).toBe(null)
    expect(auth.user).toBe(null)
    expect(localStorage.getItem('access_token')).toBe(null)
  })

  it('isAuthenticated returns true when token exists', () => {
    const auth = useAuthStore()
    auth.token = 'some-token'
    expect(auth.isAuthenticated).toBe(true)
  })

  it('userName returns user name or empty string', () => {
    const auth = useAuthStore()
    expect(auth.userName).toBe('')
    auth.user = { name: 'Alice' }
    expect(auth.userName).toBe('Alice')
  })

  it('autoLogin sets tokens and user on success', async () => {
    const mockUser = { id: 1, name: 'User', email: 'user@localhost', tier: 'free' }
    apiClient.post.mockResolvedValueOnce({
      data: {
        user: mockUser,
        access_token: 'auto-token',
        refresh_token: 'auto-refresh',
      },
    })

    const auth = useAuthStore()
    const result = await auth.autoLogin()

    expect(result).toBe(true)
    expect(auth.token).toBe('auto-token')
    expect(auth.refreshToken).toBe('auto-refresh')
    expect(auth.user).toEqual(mockUser)
    expect(localStorage.getItem('access_token')).toBe('auto-token')
  })
})
