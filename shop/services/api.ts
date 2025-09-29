import { useFetch, useRuntimeConfig, type UseFetchOptions } from "nuxt/app";
import { useAuthStore } from "~/stores/auth";

export function useApi() {
  const config = useRuntimeConfig();
  const auth = useAuthStore();

  function request<T = unknown>(path: string, opts: UseFetchOptions<T> = {}) {
    const headers: Record<string, string> = {
      ...((opts.headers as any) || {}),
    };
    if (auth.accessToken) {
      headers["Authorization"] = `Bearer ${auth.accessToken}`;
    }
    const requestOptions: any = {
      ...(opts as any),
      headers,
      credentials: "include", // Include cookies in requests
    };
    return useFetch<T>(`${config.public.apiBase}${path}`, requestOptions);
  }

  // Public API requests (no authentication required)
  function publicRequest<T = unknown>(
    path: string,
    opts: UseFetchOptions<T> = {}
  ) {
    const requestOptions: any = {
      ...(opts as any),
      headers: opts.headers || {},
      credentials: "include",
    };
    return useFetch<T>(
      `${config.public.apiBase}/public${path}`,
      requestOptions
    );
  }

  return { request, publicRequest };
}
