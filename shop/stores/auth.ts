import { defineStore } from 'pinia'

// Customer types
export enum CustomerType {
  REGULAR = 'regular',
  VIP = 'vip'
}

// Customer permissions
export enum CustomerPermission {
  VIEW_PROFILE = 'view_profile',
  EDIT_PROFILE = 'edit_profile',
  VIEW_ORDERS = 'view_orders',
  CREATE_ORDER = 'create_order',
  CANCEL_ORDER = 'cancel_order',
  
  // VIP-only permissions
  EXPRESS_CHECKOUT = 'express_checkout',
  PRIORITY_SUPPORT = 'priority_support',
  EXCLUSIVE_PRODUCTS = 'exclusive_products',
  FREE_SHIPPING = 'free_shipping',
  EARLY_ACCESS = 'early_access'
}

type Customer = {
  id: number
  email?: string
  name?: string
  customer_type?: CustomerType
  permissions?: CustomerPermission[]
  is_vip?: boolean
  vip_expires_at?: string // ISO date string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: '' as string,
    refreshToken: '' as string,
    tokenExpiresAt: null as number | null, // Unix timestamp
    user: null as Customer | null,
  }),
  persist: true,
  getters: {
    isAuthenticated: (s) => {
      if (!s.accessToken) return false
      if (!s.tokenExpiresAt) return true // Fallback nếu không có expiry time
      return Date.now() < s.tokenExpiresAt
    },
    isTokenExpired: (s) => {
      if (!s.tokenExpiresAt) return false
      return Date.now() >= s.tokenExpiresAt
    },
    timeUntilExpiry: (s) => {
      if (!s.tokenExpiresAt) return null
      return Math.max(0, s.tokenExpiresAt - Date.now())
    },
    // Customer type getters
    customerType: (s) => s.user?.customer_type || CustomerType.REGULAR,
    isVip: (s) => s.user?.is_vip || s.user?.customer_type === CustomerType.VIP,
    isRegular: (s) => s.user?.customer_type === CustomerType.REGULAR || (!s.user?.is_vip && !s.user?.customer_type),
    userPermissions: (s) => s.user?.permissions || [],
    
    // VIP status checkers
    isVipActive: (s) => {
      if (!s.user?.is_vip) return false
      if (!s.user?.vip_expires_at) return true // No expiry = permanent VIP
      return new Date(s.user.vip_expires_at) > new Date()
    },
    
    // Permission checkers
    hasPermission: (s) => (permission: CustomerPermission) => {
      if (!s.user) return false
      // VIP customers have all permissions
      const isVipActive = s.user?.is_vip && (!s.user?.vip_expires_at || new Date(s.user.vip_expires_at) > new Date())
      if (isVipActive) return true
      // Check specific permission
      return (s.user?.permissions || []).includes(permission)
    },
    hasCustomerType: (s) => (type: CustomerType) => {
      return (s.user?.customer_type || CustomerType.REGULAR) === type
    },
    hasAllPermissions: (s) => (permissions: CustomerPermission[]) => {
      if (!s.user) return false
      const isVipActive = s.user?.is_vip && (!s.user?.vip_expires_at || new Date(s.user.vip_expires_at) > new Date())
      if (isVipActive) return true
      return permissions.every(permission => (s.user?.permissions || []).includes(permission))
    }
  },
  actions: {
    setTokens(access: string, refresh = '', expiresIn?: number) {
      this.accessToken = access
      if (refresh) this.refreshToken = refresh
      // Set expiration time (expiresIn is in seconds, convert to milliseconds)
      if (expiresIn) {
        this.tokenExpiresAt = Date.now() + (expiresIn * 1000)
      }
    },
    clear() {
      this.accessToken = ''
      this.refreshToken = ''
      this.tokenExpiresAt = null
      this.user = null
    },
    logout() {
      this.clear()
    },
    // Validate token by checking if it's expired
    validateToken() {
      if (!this.accessToken) return false
      if (this.isTokenExpired) {
        this.clear()
        return false
      }
      return true
    },
    // Check if refresh token is available
    hasRefreshToken() {
      return !!this.refreshToken
    },
    // Set new tokens after refresh
    updateTokens(access: string, refresh?: string, expiresIn?: number) {
      this.accessToken = access
      if (refresh) this.refreshToken = refresh
      if (expiresIn) {
        this.tokenExpiresAt = Date.now() + (expiresIn * 1000)
      }
    }
  }
})


