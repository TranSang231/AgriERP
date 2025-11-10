import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  
  // Validate token trước khi kiểm tra authentication
  if (auth.accessToken && !auth.validateToken()) {
    // Token đã hết hạn, thử refresh nếu có refresh token
    if (auth.hasRefreshToken()) {
      try {
        const { useCustomersService } = await import('~/services/customers')
        const { refreshToken } = useCustomersService()
        await refreshToken()
        // Token đã được refresh thành công, tiếp tục
      } catch (error) {
        // Refresh thất bại, clear auth state
        auth.clear()
      }
    } else {
      // Không có refresh token, clear auth state
      auth.clear()
    }
  }
  
  // Danh sách các route cần bảo vệ (yêu cầu đăng nhập)
  const protectedRoutes = [
    '/checkout',
    '/cart', 
    '/profile',
    '/orders'
  ]
  
  // Kiểm tra xem route hiện tại có cần bảo vệ không
  const isProtectedRoute = protectedRoutes.some(route => 
    to.path.startsWith(route)
  )
  
  // Nếu là route được bảo vệ và user chưa đăng nhập hoặc token hết hạn
  if (isProtectedRoute && !auth.isAuthenticated) {
    // Lưu route hiện tại để redirect sau khi đăng nhập
    const returnUrl = to.fullPath
    return navigateTo(`/auth/login?returnUrl=${encodeURIComponent(returnUrl)}`)
  }
  
  // Nếu user đã đăng nhập và đang truy cập trang login/register, redirect về trang chủ
  if (auth.isAuthenticated && to.path.startsWith('/auth/')) {
    return navigateTo('/')
  }
})


