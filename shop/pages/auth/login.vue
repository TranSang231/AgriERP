<script setup lang="ts">
import { useCustomersService } from '~/services/customers'
const router = useRouter()
const { login } = useCustomersService()
const auth = useAuthStore()

// TODO(auth): Implement login, database table: ecommerce_customers

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const err = ref('')

async function onSubmit() {
  loading.value = true
  err.value = ''
  try {
    await login({ username: form.username, password: form.password })
    router.push('/')
  } catch (e: any) {
    err.value = e?.data?.detail || 'Login failed'
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

      <!-- TODO(auth): Make sure token has scopes for ecommerce (orders:view-mine, orders:edit-mine, products:view) -->
      
      <button type="button" :disabled="loading" class="btn-primary" @click="onSubmit">
        {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
      </button>
      <NuxtLink to="/auth/register" class="ml-3 underline">Tạo tài khoản</NuxtLink>
    </form>
  </div>
  
</template>


