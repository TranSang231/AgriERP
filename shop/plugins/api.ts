import { useAuthStore } from '@/stores/auth';
import { useLocaleStore } from '@/stores/locale';

export default defineNuxtPlugin(() => {
  const runtimeConfig = useRuntimeConfig()
  const authStore = useAuthStore();
  const localeStore = useLocaleStore();
  const api = $fetch.create({
    baseURL: runtimeConfig.public.apiBase,
    onRequest({ request, options }) {
      const tokenInfo = authStore ? authStore.accessToken : null;
      let access_token = tokenInfo ? tokenInfo.trim() : null;
      if (access_token && access_token.trim() === '') {
        access_token = null;
      }
      let language = localeStore && localeStore.current_langue && localeStore.current_langue.code
        ? localeStore.current_langue.code : 
        null;
      if (language && language.trim() === '') {
        language = null;
      }
      const authenticationEnpoint = request.endsWith('/login');

      // Update headers
      if (access_token || language) {
        const headers = (options as any).headers ||= {}
        if (Array.isArray(headers)) {
          if (access_token && !authenticationEnpoint) {
            headers.push(['Authorization', `Bearer ${access_token}`]);
          }
          if(language) {
            headers.push(['Accept-Language', language]);
          }
        } else if (headers instanceof Headers) {
          if (access_token && !authenticationEnpoint) {
            headers.set('Authorization', `Bearer ${access_token}`);
          }
          if(language) {
            headers.set('Accept-Language', language);
          }
        } else {
          if (access_token && !authenticationEnpoint) {
            headers.Authorization = `Bearer ${access_token}`
          }
          if(language) {
            headers['Accept-Language'] = language;
          }
        }
      }
    },
    async onResponseError({ response }) {
      if (response.status === 401) {
        // Token expired, clear auth store
        authStore.clear();
        // Redirect to login if not already there
        if (process.client && !window.location.pathname.includes('/login')) {
          await navigateTo('/login');
        }
      }
    }
  })

  return {
    provide: {
      api
    }
  }
})
