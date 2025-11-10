import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'
import { useAuthStore, CustomerType, CustomerPermission } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  
  // Get customer type and permission requirements from route meta
  const requiredCustomerTypes = to.meta.customerTypes as CustomerType[] || []
  const requiredPermissions = to.meta.permissions as CustomerPermission[] || []
  const requiredCustomerType = to.meta.customerType as CustomerType
  
  // Check if user is authenticated
  if (!auth.isAuthenticated) {
    return navigateTo('/auth/login')
  }

  // Check single customer type requirement
  if (requiredCustomerType && !auth.hasCustomerType(requiredCustomerType)) {
    return navigateTo('/unauthorized')
  }

  // Check multiple customer types requirement
  if (requiredCustomerTypes.length > 0 && !requiredCustomerTypes.includes(auth.customerType)) {
    return navigateTo('/unauthorized')
  }

  // Check permissions requirement
  if (requiredPermissions.length > 0 && !auth.hasAllPermissions(requiredPermissions)) {
    return navigateTo('/unauthorized')
  }
})
