<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useRouter, useRoute } from 'nuxt/app'
import { useAuthStore } from '~/stores/auth'
import { useCustomersService } from '~/services/customers'
const router = useRouter()
const route = useRoute()
const { login } = useCustomersService()
const auth = useAuthStore()

// TODO(auth): Implement login, database table: ecommerce_customers

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const err = ref('')

// Lấy returnUrl từ query parameter
const returnUrl = computed(() => {
  const url = route.query.returnUrl as string
  return url && url !== '/auth/login' ? url : '/'
})

async function onSubmit() {
  loading.value = true
  err.value = ''
  try {
    const result = await login({ username: form.username, password: form.password })
    console.log('Login successful:', result)
    alert('Đăng nhập thành công!')
    // Redirect về trang ban đầu hoặc trang chủ
    router.push(returnUrl.value)
  } catch (e: any) {
    console.error('Login error:', e)
    err.value = e?.data?.error || e?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-10 max-w-md">
    <h1 class="text-2xl font-semibold mb-6">Đăng nhập</h1>
    <form class="space-y-4">
      <div>
        <label class="block text-sm">Email hoặc SĐT</label>
        <input v-model="form.username" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Mật khẩu</label>
        <input type="password" v-model="form.password" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>

      <!-- Token automatically includes ecommerce scopes -->
      
      <button type="button" :disabled="loading" class="btn-primary" @click="onSubmit">
        {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
      </button>
      <div class="mt-4 text-center">
        <NuxtLink to="/auth/register" class="underline">Tạo tài khoản</NuxtLink>
        <span class="mx-2">|</span>
        <NuxtLink to="/auth/forgot-password" class="underline">Quên mật khẩu?</NuxtLink>
      </div>
    </form>
  </div>
  
</template>


