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
    
    // For mutation requests (POST, PUT, DELETE, PATCH), use $fetch to avoid caching
    // For GET requests, use useFetch for better performance
    const isMutation = ['POST', 'PUT', 'DELETE', 'PATCH'].includes(upperMethod)
    
    if (isMutation) {
      // Use $fetch for mutations - no caching, always fresh request
      return $fetch<T>(`${config.public.apiBase}${path}`, {
        method: upperMethod as any,
        headers,
        credentials: 'include',
        body: (opts as any).body,
        onResponseError({ response }: { response: any }) {
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
    
    // Use useFetch for GET requests (with proper cache scoping)
    const authScope = auth.accessToken ? auth.accessToken : 'guest'
    const key = (opts as any).key ?? `${path}::${authScope}`
    
    const requestOptions: any = {
      ...(opts as any),
      headers,
      credentials: 'include', // Include cookies in requests
      key,
      // Do not reuse payload-hydrated cache; always refetch in a new auth context
      initialCache: false,
      // Add onResponseError to handle 401 responses with refresh logic
      onResponseError({ response }: { response: any }) {
        if (response.status === 401) {
          // Try to refresh token if available
          if (auth.hasRefreshToken()) {
            attemptRefresh().catch(() => {
              // Refresh failed, clear auth state
              auth.clear()
            })
          } else {
            // No refresh token, clear auth state
            auth.clear()
          }
        }
      }
    }
    return useFetch<T>(`${config.public.apiBase}${path}`, requestOptions)
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
    
    // Order-related endpoints
    if (path.includes('/orders') && method === 'GET') {
      return CustomerPermission.VIEW_ORDERS
    }
    // For order creation, rely on server-side authentication; no client permission gate
    if (path.includes('/orders') && method === 'POST') {
      return null
    }
    if (path.includes('/orders') && method === 'PUT') {
      return CustomerPermission.CANCEL_ORDER
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


