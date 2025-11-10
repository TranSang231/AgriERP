import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Check if user is authenticated
  if (!auth.isAuthenticated) {
    return navigateTo('/auth/login')
  }

  // Check if user is VIP
  if (!auth.isVipActive) {
    return navigateTo('/unauthorized')
  }
})
