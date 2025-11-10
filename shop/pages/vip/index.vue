<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        {{ $t('vip.dashboard.title', 'VIP Dashboard') }}
      </h1>
      <p class="text-gray-600">
        {{ $t('vip.dashboard.subtitle', 'Chào mừng đến với khu vực VIP') }}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Express Checkout -->
      <div v-if="canExpressCheckout()" class="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg shadow-md p-6 text-white">
        <div class="flex items-center mb-4">
          <svg class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <h3 class="text-lg font-semibold">{{ $t('vip.express_checkout.title', 'Thanh toán nhanh') }}</h3>
        </div>
        <p class="mb-4 opacity-90">{{ $t('vip.express_checkout.description', 'Thanh toán đơn hàng với tốc độ cao') }}</p>
        <NuxtLink to="/checkout?express=true" class="bg-white text-purple-600 px-4 py-2 rounded hover:bg-gray-100 transition-colors">
          {{ $t('vip.express_checkout.use', 'Sử dụng ngay') }}
        </NuxtLink>
      </div>

      <!-- Exclusive Products -->
      <div v-if="canAccessExclusiveProducts()" class="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg shadow-md p-6 text-white">
        <div class="flex items-center mb-4">
          <svg class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          <h3 class="text-lg font-semibold">{{ $t('vip.exclusive_products.title', 'Sản phẩm độc quyền') }}</h3>
        </div>
        <p class="mb-4 opacity-90">{{ $t('vip.exclusive_products.description', 'Truy cập các sản phẩm chỉ dành cho VIP') }}</p>
        <NuxtLink to="/products?exclusive=true" class="bg-white text-orange-600 px-4 py-2 rounded hover:bg-gray-100 transition-colors">
          {{ $t('vip.exclusive_products.view', 'Xem sản phẩm') }}
        </NuxtLink>
      </div>

      <!-- Priority Support -->
      <div v-if="canGetPrioritySupport()" class="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg shadow-md p-6 text-white">
        <div class="flex items-center mb-4">
          <svg class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 2.25a9.75 9.75 0 100 19.5 9.75 9.75 0 000-19.5z" />
          </svg>
          <h3 class="text-lg font-semibold">{{ $t('vip.priority_support.title', 'Hỗ trợ ưu tiên') }}</h3>
        </div>
        <p class="mb-4 opacity-90">{{ $t('vip.priority_support.description', 'Nhận hỗ trợ 24/7 với độ ưu tiên cao') }}</p>
        <NuxtLink to="/support?priority=true" class="bg-white text-blue-600 px-4 py-2 rounded hover:bg-gray-100 transition-colors">
          {{ $t('vip.priority_support.contact', 'Liên hệ ngay') }}
        </NuxtLink>
      </div>
    </div>

    <!-- VIP Benefits -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h3 class="text-lg font-semibold mb-4">{{ $t('vip.benefits.title', 'Quyền lợi VIP') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 class="font-medium text-gray-900 mb-2">{{ $t('vip.benefits.shopping', 'Mua sắm') }}</h4>
          <ul class="list-disc list-inside text-sm text-gray-600 space-y-1">
            <li>{{ $t('vip.benefits.express_checkout', 'Thanh toán nhanh') }}</li>
            <li>{{ $t('vip.benefits.exclusive_products', 'Sản phẩm độc quyền') }}</li>
            <li>{{ $t('vip.benefits.free_shipping', 'Miễn phí vận chuyển') }}</li>
            <li>{{ $t('vip.benefits.early_access', 'Truy cập sớm sản phẩm mới') }}</li>
          </ul>
        </div>
        <div>
          <h4 class="font-medium text-gray-900 mb-2">{{ $t('vip.benefits.support', 'Hỗ trợ') }}</h4>
          <ul class="list-disc list-inside text-sm text-gray-600 space-y-1">
            <li>{{ $t('vip.benefits.priority_support', 'Hỗ trợ ưu tiên 24/7') }}</li>
            <li>{{ $t('vip.benefits.dedicated_manager', 'Quản lý tài khoản riêng') }}</li>
            <li>{{ $t('vip.benefits.return_policy', 'Chính sách đổi trả linh hoạt') }}</li>
            <li>{{ $t('vip.benefits.personal_shopper', 'Tư vấn mua sắm cá nhân') }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- User Info -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h3 class="text-lg font-semibold mb-4">{{ $t('vip.user_info.title', 'Thông tin VIP') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p><strong>{{ $t('vip.user_info.type', 'Loại khách hàng') }}:</strong> {{ customerType }}</p>
          <p><strong>{{ $t('vip.user_info.is_vip', 'Là VIP') }}:</strong> {{ isVip() ? 'Có' : 'Không' }}</p>
          <p v-if="daysUntilExpiry !== null">
            <strong>{{ $t('vip.user_info.expires_in', 'Hết hạn sau') }}:</strong> {{ daysUntilExpiry }} ngày
          </p>
        </div>
        <div>
          <p><strong>{{ $t('vip.user_info.permissions', 'Quyền hạn VIP') }}:</strong></p>
          <ul class="list-disc list-inside text-sm text-gray-600">
            <li v-for="permission in vipPermissions" :key="permission">
              {{ permission }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthorization } from '~/composables/useAuthorization'
import { CustomerPermission } from '~/stores/auth'

const { 
  getCustomerType, 
  isVip, 
  getUserPermissions,
  canExpressCheckout,
  canAccessExclusiveProducts,
  canGetPrioritySupport,
  canGetFreeShipping,
  canGetEarlyAccess,
  getDaysUntilVipExpiry
} = useAuthorization()

const customerType = getCustomerType()
const userPermissions = getUserPermissions()

// Filter VIP-specific permissions
const vipPermissions = userPermissions.filter(permission => 
  permission === CustomerPermission.EXPRESS_CHECKOUT ||
  permission === CustomerPermission.PRIORITY_SUPPORT ||
  permission === CustomerPermission.EXCLUSIVE_PRODUCTS ||
  permission === CustomerPermission.FREE_SHIPPING ||
  permission === CustomerPermission.EARLY_ACCESS
)

const daysUntilExpiry = getDaysUntilVipExpiry()

// Set page meta - require VIP access
// @ts-ignore - Nuxt auto-import
definePageMeta({
  middleware: 'vip',
  layout: 'default',
  title: 'VIP Dashboard'
})
</script>
