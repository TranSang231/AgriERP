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
    const requestOptions: any = {
      ...(opts as any),
      headers,
    }
    return useFetch<T>(`${config.public.apiBase}${path}`, requestOptions)
  }

  return { request }
}


