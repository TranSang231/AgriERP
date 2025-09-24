import { useApi } from '~/services/api'
import { useAuthStore } from '~/stores/auth'

type LoginPayload = { username: string; password: string }
type RegisterPayload = { email: string; first_name?: string; last_name?: string; password: string }
type VerifyPayload = { token: string; password: string; email: string; first_name?: string; last_name?: string }

export function useCustomersService() {
  const { request } = useApi()
  const auth = useAuthStore()

  async function login(payload: LoginPayload) {
    const { data, error } = await request<{ access_token: string; customer: any; message: string }>(`/customers/login`, {
      method: 'POST', body: payload
    })
    if (error.value) throw error.value
    auth.setTokens(data.value!.access_token, '')
    auth.user = data.value!.customer
    return data.value
  }

  async function register(payload: RegisterPayload) {
    const { data, error } = await request<{ message: string; customer: any }>(`/customers/register`, { method: 'POST', body: payload })
    if (error.value) throw error.value
    return data.value
  }

  async function verify(payload: VerifyPayload) {
    const { error } = await request(`/customers/verify`, { method: 'POST', body: payload })
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

  async function forgotPassword(email: string) {
    const { error } = await request(`/customers/forgot_password`, { method: 'POST', body: { email } })
    if (error.value) throw error.value
  }

  async function resetPassword(token: string, password: string) {
    const { error } = await request(`/customers/reset_password`, { method: 'POST', body: { token, password } })
    if (error.value) throw error.value
  }

  return { login, register, verify, logout, fetchUser, forgotPassword, resetPassword }
}


