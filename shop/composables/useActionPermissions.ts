import { useAuthorization } from '~/composables/useAuthorization'
import { CustomerPermission } from '~/stores/auth'

export const useActionPermissions = () => {
  const { can, canAll, isVip } = useAuthorization()

  // Profile Actions
  const canEditProfile = (): boolean => {
    return can(CustomerPermission.EDIT_PROFILE)
  }

  const canChangePassword = (): boolean => {
    return can(CustomerPermission.EDIT_PROFILE)
  }

  const canUploadAvatar = (): boolean => {
    return can(CustomerPermission.EDIT_PROFILE)
  }

  // Order Actions
  const canViewOrders = (): boolean => {
    return can(CustomerPermission.VIEW_ORDERS)
  }

  const canViewOrderDetails = (orderId: string | number): boolean => {
    // User can only view their own orders
    return can(CustomerPermission.VIEW_ORDERS)
  }

  const canCancelOrder = (order: any): boolean => {
    // Can cancel if has permission and order is in cancellable state
    return can(CustomerPermission.CANCEL_ORDER) && 
           order.order_status === 0 // Only new orders can be cancelled
  }

  const canPayOrder = (order: any): boolean => {
    // Can pay if order requires payment and user has create order permission
    return can(CustomerPermission.CREATE_ORDER) && 
           order.payment_method === 0 && 
           order.payment_status === 0 // Bank transfer orders that haven't been paid
  }

  const canCreateOrder = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  // Cart Actions
  const canAddToCart = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  const canRemoveFromCart = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  const canUpdateCartQuantity = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  // Checkout Actions
  const canProceedToCheckout = (): boolean => {
    return can(CustomerPermission.CREATE_ORDER)
  }

  const canUseExpressCheckout = (): boolean => {
    return can(CustomerPermission.EXPRESS_CHECKOUT)
  }

  // VIP Actions
  const canAccessExclusiveProducts = (): boolean => {
    return can(CustomerPermission.EXCLUSIVE_PRODUCTS)
  }

  const canGetFreeShipping = (): boolean => {
    return can(CustomerPermission.FREE_SHIPPING)
  }

  const canGetEarlyAccess = (): boolean => {
    return can(CustomerPermission.EARLY_ACCESS)
  }

  // const canGetPrioritySupport = (): boolean => {
  //   return can(CustomerPermission.PRIORITY_SUPPORT)
  // }

  // Product Actions
  const canViewProduct = (product: any): boolean => {
    // Regular products: all authenticated users can view
    // Exclusive products: only VIP users can view
    if (product.is_exclusive) {
      return can(CustomerPermission.EXCLUSIVE_PRODUCTS)
    }
    return true // All authenticated users can view regular products
  }

  const canAddExclusiveProductToCart = (product: any): boolean => {
    if (product.is_exclusive) {
      return can(CustomerPermission.EXCLUSIVE_PRODUCTS) && 
             can(CustomerPermission.CREATE_ORDER)
    }
    return can(CustomerPermission.CREATE_ORDER)
  }

  // Support Actions
  const canContactSupport = (): boolean => {
    return true // All authenticated users can contact support
  }

  const canGetPrioritySupport = (): boolean => {
    return can(CustomerPermission.PRIORITY_SUPPORT)
  }

  // Validation helpers
  const validateAction = (action: string, context?: any): { allowed: boolean; reason?: string } => {
    switch (action) {
      case 'edit_profile':
        return { allowed: canEditProfile(), reason: !canEditProfile() ? 'No permission to edit profile' : undefined }
      
      case 'change_password':
        return { allowed: canChangePassword(), reason: !canChangePassword() ? 'No permission to change password' : undefined }
      
      case 'view_orders':
        return { allowed: canViewOrders(), reason: !canViewOrders() ? 'No permission to view orders' : undefined }
      
      case 'cancel_order':
        if (!context?.order) return { allowed: false, reason: 'Order context required' }
        return { 
          allowed: canCancelOrder(context.order), 
          reason: !canCancelOrder(context.order) ? 'Cannot cancel this order' : undefined 
        }
      
      case 'pay_order':
        if (!context?.order) return { allowed: false, reason: 'Order context required' }
        return { 
          allowed: canPayOrder(context.order), 
          reason: !canPayOrder(context.order) ? 'Cannot pay this order' : undefined 
        }
      
      case 'create_order':
        return { allowed: canCreateOrder(), reason: !canCreateOrder() ? 'No permission to create orders' : undefined }
      
      case 'express_checkout':
        return { allowed: canUseExpressCheckout(), reason: !canUseExpressCheckout() ? 'Express checkout not available' : undefined }
      
      case 'view_exclusive_product':
        if (!context?.product) return { allowed: false, reason: 'Product context required' }
        return { 
          allowed: canViewProduct(context.product), 
          reason: !canViewProduct(context.product) ? 'Cannot view exclusive products' : undefined 
        }
      
      default:
        return { allowed: false, reason: 'Unknown action' }
    }
  }

  // Bulk permission check
  const checkMultipleActions = (actions: Array<{ action: string; context?: any }>): Array<{ action: string; allowed: boolean; reason?: string }> => {
    return actions.map(({ action, context }) => ({
      action,
      ...validateAction(action, context)
    }))
  }

  return {
    // Profile actions
    canEditProfile,
    canChangePassword,
    canUploadAvatar,
    
    // Order actions
    canViewOrders,
    canViewOrderDetails,
    canCancelOrder,
    canPayOrder,
    canCreateOrder,
    
    // Cart actions
    canAddToCart,
    canRemoveFromCart,
    canUpdateCartQuantity,
    
    // Checkout actions
    canProceedToCheckout,
    canUseExpressCheckout,
    
    // VIP actions
    canAccessExclusiveProducts,
    canGetFreeShipping,
    canGetEarlyAccess,
    // canGetPrioritySupport,
    
    // Product actions
    canViewProduct,
    canAddExclusiveProductToCart,
    
    // Support actions
    canContactSupport,
    canGetPrioritySupport,
    
    // Validation helpers
    validateAction,
    checkMultipleActions
  }
}
