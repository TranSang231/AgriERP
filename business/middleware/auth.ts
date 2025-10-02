import { useOauthStore } from '@/stores/oauth'
import { navigateTo } from 'nuxt/app'

export default defineNuxtRouteMiddleware((to, from) => {
  const oauthStore = useOauthStore()
  const { tokenInfo } = oauthStore;
  const authenticated = tokenInfo && tokenInfo.access_token && tokenInfo.access_token.length > 0;

  const currentTime = Math.floor(Date.now() / 1000);
  const tokenValid = tokenInfo && tokenInfo.exp && tokenInfo.exp > currentTime;
  if (authenticated && tokenValid) {
    console.log('tokenInfo.exp',tokenInfo.exp);
    if (to.path === '/') {
      return navigateTo('/dashboard');
    }
  }
})
