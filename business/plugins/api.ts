import { useOauthStore } from '@/stores/oauth';
import { useLocaleStore } from '@/stores/locale';

export default defineNuxtPlugin(() => {
  const runtimeConfig = useRuntimeConfig()
  const oauthStore = useOauthStore();
  const localeStore = useLocaleStore();
  const api = $fetch.create({
    baseURL: runtimeConfig.public.apiBase,
    onRequest({ request, options }) {
      const tokenInfo = oauthStore? oauthStore.tokenInfo : null;
      let access_token = tokenInfo? tokenInfo.access_token.trim(): null;
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
      if (response.status === 401 || response.status === 403) {
        const tokenInfo = oauthStore? oauthStore.tokenInfo : null;
        const refresh_token = tokenInfo? tokenInfo.refresh_token: null;
        if (refresh_token && refresh_token.trim() !== '') {
          const formData = new FormData();
          formData.append("refresh_token", refresh_token);
          const refreshTokenUrl = `${runtimeConfig.public.apiBase}/employees/refresh-token`;
          $fetch(refreshTokenUrl,
            {
              method: 'POST',
              body: formData
            }
          ).then((data:any) => {
            const { access_token, refresh_token } = data;
            oauthStore.setTokenInfo({ access_token, refresh_token })
          })
            .catch(error => {
              console.error(error);
              oauthStore.$reset();
            })
        }
      }
    }
  })

  // Expose to useNuxtApp().$api
  return {
    provide: {
      api
    }
  }
})