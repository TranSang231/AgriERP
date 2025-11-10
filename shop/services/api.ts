import { useFetch, useRuntimeConfig, type UseFetchOptions } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'
import { CustomerPermission } from '~/stores/auth'

export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()
  let isRefreshing = false
  let refreshPromise: Promise<any> | null = null

  async function attemptRefresh() {
    if (isRefreshing && refreshPromise) {
      return refreshPromise
    }

    if (!auth.hasRefreshToken()) {
      auth.clear()
      throw new Error('No refresh token available')
    }

    isRefreshing = true
    refreshPromise = (async () => {
      try {
        const { useCustomersService } = await import('~/services/customers')
        const { refreshToken } = useCustomersService()
        await refreshToken()
        return true
      } catch (error) {
        auth.clear()
        throw error
      } finally {
        isRefreshing = false
        refreshPromise = null
      }
    })()

    return refreshPromise
  }

  function request<T = unknown>(path: string, opts: UseFetchOptions<T> = {}) {
    // Validate token before making request
    if (auth.accessToken && !auth.validateToken()) {
      // Token is expired, clear auth state
      auth.clear()
    }

    // Check permissions for specific endpoints
    const method = typeof opts.method === 'string' ? opts.method : opts.method?.value
    const upperMethod = (method || 'GET').toUpperCase()
    const requiredPermission = getRequiredPermission(path, method)
    if (requiredPermission && !auth.hasPermission(requiredPermission)) {
      throw new Error(`Insufficient permissions: ${requiredPermission} required for ${path}`)
    }

    const headers: Record<string, string> = {
      ...(opts.headers as any || {})
    }
    // Always attach Authorization when authenticated; backend now issues OAuth tokens
    if (auth.accessToken && auth.isAuthenticated) {
      headers['Authorization'] = `Bearer ${auth.accessToken}`
    }
    // Add Idempotency-Key for order creation requests
    if (path.includes('/orders') && upperMethod === 'POST') {
      headers['Idempotency-Key'] = headers['Idempotency-Key'] || cryptoRandomKey()
    }
    
    const fullUrl = `${config.public.apiBase}${path}`
    console.log('🔥 API Request:', upperMethod, fullUrl, 'params:', (opts as any).params)
    
    // Always use $fetch for client-side requests to avoid mounted component warnings
    // This is especially important for dynamic routes and client-side navigation
    return $fetch<T>(fullUrl, {
      method: upperMethod as any,
      headers,
      credentials: 'include',
      body: (opts as any).body,
      params: (opts as any).params,
      onResponseError({ response }: { response: any }) {
        console.error('❌ API Error:', response.status, response.statusText, 'URL:', fullUrl)
        if (response.status === 401) {
          if (auth.hasRefreshToken()) {
            attemptRefresh().catch(() => auth.clear())
          } else {
            auth.clear()
          }
        }
      }
    }) as any
  }

  // Helper function to determine required permission based on endpoint and method
  function getRequiredPermission(path: string, method?: string): CustomerPermission | null {
    // Profile-related endpoints
    if (path.includes('/customers/profile') && method === 'PUT') {
      return CustomerPermission.EDIT_PROFILE
    }
    if (path.includes('/customers/change-password')) {
      return CustomerPermission.EDIT_PROFILE
    }
    
    // Order-related endpoints - rely on backend authentication for viewing own orders
    // Backend will check if user is authenticated and filter orders by customer_id
    if (path.includes('/orders')) {
      return null  // No client-side permission check needed
    }
    
    // Cart-related endpoints
    if (path.includes('/cart') && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
      return CustomerPermission.CREATE_ORDER
    }
    
    // Checkout endpoints
    if (path.includes('/checkout')) {
      return CustomerPermission.CREATE_ORDER
    }
    
    // No specific permission required for other endpoints
    return null
  }

  return { request }
}


function cryptoRandomKey(): string {
  try {
    // Browser crypto API
    const arr = new Uint8Array(16)
    if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
      crypto.getRandomValues(arr)
      return Array.from(arr).map(b => b.toString(16).padStart(2, '0')).join('')
    }
  } catch (_) {}
  // Fallback
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}


