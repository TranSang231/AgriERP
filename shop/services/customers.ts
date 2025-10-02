import { useApi } from '~/services/api'
import { useRuntimeConfig, clearNuxtData } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'

type LoginPayload = { username: string; password: string }
type RegisterPayload = { email: string; first_name?: string; last_name?: string; password: string }
type VerifyPayload = { token: string; password: string; email: string; first_name?: string; last_name?: string }

export function useCustomersService() {
  const { request } = useApi()
  const auth = useAuthStore()
  const config = useRuntimeConfig()

  async function login(payload: LoginPayload) {
    const { data, error } = await request<{ access_token: string; customer: any; message: string }>(`/customers/login`, {
      method: 'POST', body: payload
    })
    if (error.value) throw error.value
    auth.setTokens(data.value!.access_token, '')
    // Clear any cached useFetch data from previous (or guest) session
    try { clearNuxtData() } catch (_) {}
    // Always refresh profile from backend to avoid stale user/session
    try {
      const fresh = await getProfile()
      if ((fresh as any)?.customer) auth.user = (fresh as any).customer
      else auth.user = data.value!.customer
    } catch (_) {
      auth.user = data.value!.customer
    }
    // Immediately load cart for this account so UI updates without manual refresh
    try {
      const cart = useCartStore()
      cart.items = []
      await cart.load()
    } catch (_) {}
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
    // Clear cached data tied to previous authenticated session
    try { clearNuxtData() } catch (_) {}
    // Reload cart in guest context
    try {
      const cart = useCartStore()
      cart.items = []
      cart.load()
    } catch (_) {}
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

  async function getProfile() {
    // Use $fetch to avoid useFetch warning when called after mount (e.g., from stores)
    const headers: Record<string, string> = {}
    if (auth.accessToken) headers['Authorization'] = `Bearer ${auth.accessToken}`
    return await $fetch<{ customer: any }>(`${config.public.apiBase}/customers/userinfo`, {
      method: 'GET',
      headers,
      credentials: 'include'
    })
  }

  async function updateProfile(payload: any) {
    const { data, error } = await request<{ message: string; customer: any }>(`/customers/profile`, {
      method: 'PUT', body: payload
    })
    if (error.value) throw error.value
    return data.value
  }

  async function changePassword(payload: { current_password: string; new_password: string }) {
    const { data, error } = await request<{ message: string }>(`/customers/change-password`, {
      method: 'POST', body: payload
    })
    if (error.value) throw error.value
    return data.value
  }

  return { login, register, verify, logout, fetchUser, forgotPassword, resetPassword, getProfile, updateProfile, changePassword }
}


