import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  if (to.path.startsWith('/checkout') && !auth.isAuthenticated) {
    return navigateTo('/auth/login')
  }
})


