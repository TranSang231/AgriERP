import { useAuthStore, CustomerType, CustomerPermission } from '~/stores/auth'

export const useAuthorization = () => {
  const auth = useAuthStore()

  // Check if user has specific permission
  const can = (permission: CustomerPermission): boolean => {
    return auth.hasPermission(permission)
  }

  // Check if user has any of the specified permissions
  const canAny = (permissions: CustomerPermission[]): boolean => {
    if (!auth.user) return false
    if (auth.isVipActive) return true
    return permissions.some(permission => auth.userPermissions.includes(permission))
  }

  // Check if user has all specified permissions
  const canAll = (permissions: CustomerPermission[]): boolean => {
    return auth.hasAllPermissions(permissions)
  }

  // Check if user has specific customer type
  const hasCustomerType = (type: CustomerType): boolean => {
    return auth.hasCustomerType(type)
  }

  // Check if user is VIP
  const isVip = (): boolean => {
    return auth.isVipActive
  }

  // Check if user is regular customer
  const isRegular = (): boolean => {
    return auth.isRegular
  }

  // Get customer type
  const getCustomerType = (): CustomerType => {
    return auth.customerType
  }

  // Get user permissions
  const getUserPermissions = (): CustomerPermission[] => {
    return auth.userPermissions
  }

  // Check if user can view profile
  const canViewProfile = (): boolean => {
    return can(CustomerPermission.VIEW_PROFILE)
  }

  // Check if user can edit profile
  const canEditProfile = (): boolean => {
    return can(CustomerPermission.EDIT_PROFILE)
  }

  // Check if user can view orders
  const canViewOrders = (): boolean => {
    return can(CustomerPermission.VIEW_ORDERS)
  }

  // Check if user can create orders
  const canCreateOrders = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  // Check if user can cancel orders
  const canCancelOrders = (): boolean => {
    return can(CustomerPermission.CANCEL_ORDER)
  }

  // Check if user can use express checkout
  const canExpressCheckout = (): boolean => {
    return can(CustomerPermission.EXPRESS_CHECKOUT)
  }

  // Check if user can access exclusive products
  const canAccessExclusiveProducts = (): boolean => {
    return can(CustomerPermission.EXCLUSIVE_PRODUCTS)
  }

  // Check if user can get priority support
  const canGetPrioritySupport = (): boolean => {
    return can(CustomerPermission.PRIORITY_SUPPORT)
  }

  // Check if user can get free shipping
  const canGetFreeShipping = (): boolean => {
    return can(CustomerPermission.FREE_SHIPPING)
  }

  // Check if user can get early access
  const canGetEarlyAccess = (): boolean => {
    return can(CustomerPermission.EARLY_ACCESS)
  }

  // Check if VIP is expired
  const isVipExpired = (): boolean => {
    if (!auth.user?.is_vip) return false
    if (!auth.user?.vip_expires_at) return false // No expiry = permanent
    return new Date(auth.user.vip_expires_at) <= new Date()
  }

  // Get VIP expiry date
  const getVipExpiryDate = (): Date | null => {
    if (!auth.user?.vip_expires_at) return null
    return new Date(auth.user.vip_expires_at)
  }

  // Get days until VIP expires
  const getDaysUntilVipExpiry = (): number | null => {
    const expiryDate = getVipExpiryDate()
    if (!expiryDate) return null
    const now = new Date()
    const diffTime = expiryDate.getTime() - now.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return Math.max(0, diffDays)
  }

  return {
    // Permission checks
    can,
    canAny,
    canAll,
    
    // Customer type checks
    hasCustomerType,
    isVip,
    isRegular,
    
    // User info
    getCustomerType,
    getUserPermissions,
    
    // Basic permission checks
    canViewProfile,
    canEditProfile,
    canViewOrders,
    canCreateOrders,
    canCancelOrders,
    
    // VIP-specific permission checks
    canExpressCheckout,
    canAccessExclusiveProducts,
    canGetPrioritySupport,
    canGetFreeShipping,
    canGetEarlyAccess,
    
    // VIP status helpers
    isVipExpired,
    getVipExpiryDate,
    getDaysUntilVipExpiry
  }
}
