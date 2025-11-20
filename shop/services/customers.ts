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
    // CRITICAL: Clear any existing auth data BEFORE making the login request
    // This prevents old tokens/user data from contaminating the new login
    auth.clear()
    
    // ALSO clear Pinia's persisted localStorage to prevent race conditions
    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem('auth')
      } catch (_) {}
    }
    
    console.log('[LOGIN SERVICE] Sending login request with:', payload)
    
    try {
      // Since POST uses $fetch (not useFetch), it returns data directly
      const data = await request<{ access_token: string; refresh_token?: string; customer: any; message: string; expires_in?: number }>(`/customers/login`, {
        method: 'POST', 
        body: payload,
        // Force no cache to prevent browser from using cached response
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        },
        // Disable Nuxt/ofetch cache
        cache: 'no-store'
      })
      
      console.log('[LOGIN] Backend returned customer:', data.customer.id, data.customer.email, data.customer.first_name)
      
      // Set NEW tokens from the login response
      auth.setTokens(data.access_token, data.refresh_token || '', data.expires_in)
      
      // Set the user IMMEDIATELY from the login response (not from cached profile)
      auth.user = data.customer
      
      // Clear any cached useFetch data from previous session
      try { clearNuxtData() } catch (_) {}
      
      // Verify profile matches (optional double-check, but use login response as source of truth)
      try {
        const fresh = await getProfile()
        if ((fresh as any)?.customer) {
          const freshCustomer = (fresh as any).customer
          console.log('[LOGIN] Profile verification returned customer:', freshCustomer.id, freshCustomer.email, freshCustomer.first_name)
          // Log any mismatch for debugging
          if (freshCustomer.id !== data.customer.id) {
            console.error('[LOGIN] Profile mismatch!', {
              loginResponse: data.customer.id,
              profileResponse: freshCustomer.id
            })
          }
          auth.user = freshCustomer
        }
      } catch (e) {
        console.warn('[LOGIN] Could not verify profile, using login response:', e)
        // Keep the user from login response
      }
      
      console.log('[LOGIN] Final auth.user set to:', auth.user?.id, auth.user?.email, (auth.user as any)?.first_name)
      
      // Immediately load cart for this account
      try {
        const cart = useCartStore()
        cart.items = []
        await cart.load()
      } catch (e) {
        console.error('[LOGIN] Failed to load cart:', e)
      }
      
      return data
    } catch (error) {
      console.error('[LOGIN] Login failed:', error)
      throw error
    }
  }

  async function register(payload: RegisterPayload) {
    try {
      const data = await request<{ message: string; customer: any }>(`/customers/register`, { method: 'POST', body: payload })
      return data
    } catch (error) {
      throw error
    }
  }

  async function verify(payload: VerifyPayload) {
    try {
      await request(`/customers/verify`, { method: 'POST', body: payload })
    } catch (error) {
      throw error
    }
  }

  async function logout() {
    try {
      await request(`/customers/logout`, { 
        method: 'POST',
        body: {
          access_token: auth.accessToken,
          refresh_token: auth.refreshToken
        }
      })
      
      auth.clear()
      
      // CRITICAL: Clear Pinia's persisted localStorage
      if (typeof window !== 'undefined') {
        try {
          localStorage.removeItem('auth')
        } catch (_) {}
      }
      
      // Clear cached data tied to previous authenticated session
      try { clearNuxtData() } catch (_) {}
      // Reload cart in guest context
      try {
        const cart = useCartStore()
        cart.items = []
        cart.load()
      } catch (_) {}
      
      return { success: true }
    } catch (e) {
      console.warn('[LOGOUT] API call failed, clearing local state anyway:', e)
      
      auth.clear()
      
      // CRITICAL: Clear Pinia's persisted localStorage even on error
      if (typeof window !== 'undefined') {
        try {
          localStorage.removeItem('auth')
        } catch (_) {}
      }
      
      // Clear cached data tied to previous authenticated session
      try { clearNuxtData() } catch (_) {}
      // Reload cart in guest context
      try {
        const cart = useCartStore()
        cart.items = []
        cart.load()
      } catch (_) {}
      
      // Return success even on API error since we cleared local state
      return { success: true, error: e }
    }
  }

  async function fetchUser() {
    try {
      const data = await request(`/customers/userinfo`, { method: 'GET' })
      auth.user = data as any
    } catch (error) {
      console.error('Error fetching user:', error)
    }
  }

  async function forgotPassword(email: string) {
    try {
      await request(`/customers/forgot_password`, { method: 'POST', body: { email } })
    } catch (error) {
      throw error
    }
  }

  async function resetPassword(token: string, password: string) {
    try {
      await request(`/customers/reset_password`, { method: 'POST', body: { token, password } })
    } catch (error) {
      throw error
    }
  }

  async function getProfile() {
    // Use the request() helper which properly handles auth headers
    const data = await request<{ customer: any }>(`/customers/userinfo`, { method: 'GET' })
    return data
  }

  async function updateProfile(payload: any) {
    try {
      const data = await request<{ message: string; customer: any }>(`/customers/profile`, {
        method: 'PUT', body: payload
      })
      return data
    } catch (error) {
      throw error
    }
  }

  async function changePassword(payload: { current_password: string; new_password: string }) {
    try {
      const data = await request<{ message: string }>(`/customers/change-password`, {
        method: 'POST', body: payload
      })
      return data
    } catch (error) {
      throw error
    }
  }

  async function refreshToken() {
    if (!auth.refreshToken) {
      throw new Error('No refresh token available')
    }
    
    const data = await request<{ access_token: string; refresh_token?: string; expires_in?: number }>(`/customers/refresh`, {
      method: 'POST', 
      body: { refresh_token: auth.refreshToken }
    })
    
    // Update tokens with new access token
    auth.setTokens(data.access_token, data.refresh_token || auth.refreshToken, data.expires_in)
    
    return data
  }

  return { login, register, verify, logout, fetchUser, forgotPassword, resetPassword, getProfile, updateProfile, changePassword, refreshToken }
}


