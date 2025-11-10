import { useAuthStore } from '~/stores/auth'

export const useTokenValidation = () => {
  const auth = useAuthStore()

  // Kiểm tra token có hợp lệ không
  const isTokenValid = () => {
    return auth.validateToken()
  }

  // Kiểm tra token có sắp hết hạn không (trong vòng 5 phút)
  const isTokenExpiringSoon = () => {
    if (!auth.timeUntilExpiry) return false
    return auth.timeUntilExpiry < 5 * 60 * 1000 // 5 phút
  }

  // Lấy thời gian còn lại của token (milliseconds)
  const getTimeUntilExpiry = () => {
    return auth.timeUntilExpiry
  }

  // Format thời gian còn lại thành string dễ đọc
  const getFormattedTimeUntilExpiry = () => {
    const timeLeft = auth.timeUntilExpiry
    if (!timeLeft) return null

    const minutes = Math.floor(timeLeft / (1000 * 60))
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000)
    
    if (minutes > 0) {
      return `${minutes}m ${seconds}s`
    }
    return `${seconds}s`
  }

  // Kiểm tra và xử lý token hết hạn
  const handleTokenExpiry = () => {
    if (auth.isTokenExpired) {
      auth.clear()
      return false
    }
    return true
  }

  // Auto-refresh token nếu cần
  const refreshTokenIfNeeded = async () => {
    if (isTokenExpiringSoon() && auth.hasRefreshToken()) {
      try {
        const { useCustomersService } = await import('~/services/customers')
        const { refreshToken } = useCustomersService()
        await refreshToken()
        return true
      } catch (error) {
        console.error('Failed to refresh token:', error)
        auth.clear()
        return false
      }
    }
    return true
  }

  // Force refresh token
  const forceRefreshToken = async () => {
    if (!auth.hasRefreshToken()) {
      throw new Error('No refresh token available')
    }
    
    try {
      const { useCustomersService } = await import('~/services/customers')
      const { refreshToken } = useCustomersService()
      await refreshToken()
      return true
    } catch (error) {
      console.error('Failed to refresh token:', error)
      auth.clear()
      throw error
    }
  }

  return {
    isTokenValid,
    isTokenExpiringSoon,
    getTimeUntilExpiry,
    getFormattedTimeUntilExpiry,
    handleTokenExpiry,
    refreshTokenIfNeeded,
    forceRefreshToken
  }
}
