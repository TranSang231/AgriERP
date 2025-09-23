import { useApi } from '~/services/api'
import { useAuthStore } from '~/stores/auth'

type LoginPayload = { username: string; password: string }
type RegisterPayload = { email: string; password: string; name?: string }

export function useCustomersService() {
  const { request } = useApi()
  const auth = useAuthStore()

  async function login(payload: LoginPayload) {
    const { data, error } = await request<{ access: string; refresh?: string }>(`/customers/login`, {
      method: 'POST', body: payload
    })
    if (error.value) throw error.value
    auth.setTokens(data.value!.access, data.value!.refresh || '')
    await fetchUser()
  }

  async function register(payload: RegisterPayload) {
    const { error } = await request(`/customers/register`, { method: 'POST', body: payload })
    if (error.value) throw error.value
  }

  async function logout() {
    await request(`/customers/logout`, { method: 'POST' })
    auth.clear()
  }

  async function fetchUser() {
    const { data, error } = await request(`/customers/userinfo`)
    if (!error.value) auth.user = data.value as any
  }

  return { login, register, logout, fetchUser }
}


