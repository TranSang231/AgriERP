import { useFetch, useRuntimeConfig, type UseFetchOptions } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  function request<T>(path: string, opts: UseFetchOptions<T> = {}) {
    const headers: Record<string, string> = {
      ...(opts.headers as any || {})
    }
    if (auth.accessToken) {
      headers['Authorization'] = `Bearer ${auth.accessToken}`
    }
    return useFetch<T>(`${config.public.apiBase}${path}`, {
      ...opts,
      headers,
    })
  }

  return { request }
}


