<template>
  <div class="container mx-auto px-4 py-10 max-w-md text-center">
    <div class="mb-6">
      <svg class="mx-auto h-16 w-16 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
      </svg>
    </div>
    
    <h1 class="text-2xl font-semibold mb-4 text-gray-900">
      {{ $t('unauthorized.title', 'Truy cập bị từ chối') }}
    </h1>
    
    <p class="text-gray-600 mb-6">
      {{ $t('unauthorized.message', 'Bạn không có quyền truy cập vào trang này. Vui lòng liên hệ quản trị viên nếu bạn cho rằng đây là lỗi.') }}
    </p>
    
    <div class="space-y-3">
      <NuxtLink 
        to="/" 
        class="block w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
      >
        {{ $t('unauthorized.back_home', 'Về trang chủ') }}
      </NuxtLink>
      
      <button 
        @click="$router.back()" 
        class="block w-full bg-gray-200 text-gray-800 py-2 px-4 rounded hover:bg-gray-300 transition-colors"
      >
        {{ $t('unauthorized.go_back', 'Quay lại') }}
      </button>
    </div>
    
    <!-- Debug info for development -->
    <div v-if="isDev" class="mt-8 p-4 bg-gray-100 rounded text-left text-sm">
      <h3 class="font-semibold mb-2">Debug Info:</h3>
      <p><strong>Customer Type:</strong> {{ customerType }}</p>
      <p><strong>Is VIP:</strong> {{ isVip() }}</p>
      <p><strong>Is Regular:</strong> {{ isRegular() }}</p>
      <p><strong>Permissions:</strong> {{ userPermissions.join(', ') || 'None' }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthorization } from '~/composables/useAuthorization'

const { getCustomerType, isVip, isRegular, getUserPermissions } = useAuthorization()

const customerType = getCustomerType()
const userPermissions = getUserPermissions()

// Check if in development mode
const isDev = process.dev

// Set page meta
definePageMeta({
  layout: 'default',
  title: 'Unauthorized Access'
})
</script>
