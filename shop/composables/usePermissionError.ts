import { useAuthorization } from '~/composables/useAuthorization'
import { CustomerPermission } from '~/stores/auth'
import { useNuxtApp } from 'nuxt/app'

export const usePermissionError = () => {
  const { can } = useAuthorization()

  const handlePermissionError = (permission: CustomerPermission, action: string) => {
    const hasPermission = can(permission)
    
    if (!hasPermission) {
      const errorMessages = {
        [CustomerPermission.VIEW_PROFILE]: 'Bạn không có quyền xem thông tin cá nhân',
        [CustomerPermission.EDIT_PROFILE]: 'Bạn không có quyền chỉnh sửa thông tin cá nhân',
        [CustomerPermission.VIEW_ORDERS]: 'Bạn không có quyền xem đơn hàng',
        [CustomerPermission.CREATE_ORDER]: 'Bạn không có quyền tạo đơn hàng',
        [CustomerPermission.CANCEL_ORDER]: 'Bạn không có quyền hủy đơn hàng',
        [CustomerPermission.EXPRESS_CHECKOUT]: 'Bạn không có quyền sử dụng thanh toán nhanh',
        [CustomerPermission.PRIORITY_SUPPORT]: 'Bạn không có quyền sử dụng hỗ trợ ưu tiên',
        [CustomerPermission.EXCLUSIVE_PRODUCTS]: 'Bạn không có quyền truy cập sản phẩm độc quyền',
        [CustomerPermission.FREE_SHIPPING]: 'Bạn không có quyền miễn phí vận chuyển',
        [CustomerPermission.EARLY_ACCESS]: 'Bạn không có quyền truy cập sớm'
      }

      const message = errorMessages[permission] || `Bạn không có quyền thực hiện hành động: ${action}`
      
      // Show error notification
      const { $toast } = useNuxtApp() as any
      $toast.error(message)
      
      return {
        hasPermission: false,
        message,
        shouldShowUpgrade: isVipOnlyPermission(permission)
      }
    }

    return {
      hasPermission: true,
      message: null,
      shouldShowUpgrade: false
    }
  }

  const isVipOnlyPermission = (permission: CustomerPermission): boolean => {
    const vipPermissions = [
      CustomerPermission.EXPRESS_CHECKOUT,
      CustomerPermission.PRIORITY_SUPPORT,
      CustomerPermission.EXCLUSIVE_PRODUCTS,
      CustomerPermission.FREE_SHIPPING,
      CustomerPermission.EARLY_ACCESS
    ]
    return vipPermissions.includes(permission)
  }

  const getUpgradeMessage = (permission: CustomerPermission): string => {
    const upgradeMessages: Record<string, string> = {
      [CustomerPermission.EXPRESS_CHECKOUT]: 'Nâng cấp lên VIP để sử dụng thanh toán nhanh',
      [CustomerPermission.PRIORITY_SUPPORT]: 'Nâng cấp lên VIP để được hỗ trợ ưu tiên',
      [CustomerPermission.EXCLUSIVE_PRODUCTS]: 'Nâng cấp lên VIP để truy cập sản phẩm độc quyền',
      [CustomerPermission.FREE_SHIPPING]: 'Nâng cấp lên VIP để được miễn phí vận chuyển',
      [CustomerPermission.EARLY_ACCESS]: 'Nâng cấp lên VIP để được truy cập sớm'
    }
    return upgradeMessages[permission] || 'Nâng cấp tài khoản để sử dụng tính năng này'
  }

  const showPermissionError = (permission: CustomerPermission, action: string) => {
    const result = handlePermissionError(permission, action)
    
    if (!result.hasPermission) {
      // Log the error for debugging
      console.warn(`Permission denied: ${permission} for action: ${action}`)
      
      // Show upgrade option if it's a VIP-only feature
      if (result.shouldShowUpgrade) {
        const upgradeMessage = getUpgradeMessage(permission)
        const { $toast } = useNuxtApp() as any
        $toast.error(`${result.message}. ${upgradeMessage}`)
      }
    }
    
    return result
  }

  const validateAndExecute = async <T>(
    permission: CustomerPermission, 
    action: string, 
    executeFn: () => Promise<T> | T
  ): Promise<T | null> => {
    const result = handlePermissionError(permission, action)
    
    if (!result.hasPermission) {
      showPermissionError(permission, action)
      return null
    }
    
    try {
      return await executeFn()
    } catch (error) {
      console.error(`Error executing ${action}:`, error)
      throw error
    }
  }

  return {
    handlePermissionError,
    showPermissionError,
    validateAndExecute,
    isVipOnlyPermission,
    getUpgradeMessage
  }
}
