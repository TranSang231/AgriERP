import { useFetch, useRuntimeConfig, type UseFetchOptions } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  function request<T = unknown>(path: string, opts: UseFetchOptions<T> = {}) {
    const headers: Record<string, string> = {
      ...(opts.headers as any || {})
    }
    if (auth.accessToken) {
      headers['Authorization'] = `Bearer ${auth.accessToken}`
    }
    // Scope fetch cache/deduplication by the current auth identity to avoid
    // leaking data between accounts when switching users.
    const authScope = auth.accessToken ? auth.accessToken : 'guest'
    const key = (opts as any).key ?? `${path}::${authScope}`
    const requestOptions: any = {
      ...(opts as any),
      headers,
      credentials: 'include', // Include cookies in requests
      key,
      // Do not reuse payload-hydrated cache; always refetch in a new auth context
      initialCache: false,  
    }
    return useFetch<T>(`${config.public.apiBase}${path}`, requestOptions)
  }

  return { request }
}


