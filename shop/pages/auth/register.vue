<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'nuxt/app'
import { useCustomersService } from '~/services/customers'
const router = useRouter()
const { register } = useCustomersService()
const form = reactive({ email: '', first_name: '', last_name: '', password: '', confirmPassword: '' })
const loading = ref(false)
const err = ref('')

async function onSubmit() {
  if (form.password !== form.confirmPassword) {
    err.value = 'Mật khẩu xác nhận không khớp'
    return
  }

  if (form.password.length < 6) {
    err.value = 'Mật khẩu phải có ít nhất 6 ký tự'
    return
  }

  loading.value = true
  err.value = ''
  try {
    const result = await register({ 
      email: form.email, 
      first_name: form.first_name, 
      last_name: form.last_name,
      password: form.password 
    })
    
    // Check if registration was successful and has access token
    if (result && (result as any).access_token) {
      alert('Đăng ký thành công! Bạn đã được tự động đăng nhập.')
      // User is already logged in, redirect to home or dashboard
      router.push('/')
    } else {
      alert('Đăng ký thành công! Bạn đã có thể đăng nhập ngay.')
      router.push('/auth/login')
    }
  } catch (e: any) {
    err.value = e?.data?.detail || 'Register failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-10 max-w-md">
    <h1 class="text-2xl font-semibold mb-6">Đăng ký tài khoản</h1>
    <form class="space-y-4">
      <div>
        <label class="block text-sm">Họ</label>
        <input v-model="form.first_name" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Tên</label>
        <input v-model="form.last_name" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Email</label>
        <input v-model="form.email" type="email" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Mật khẩu</label>
        <input v-model="form.password" type="password" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Xác nhận mật khẩu</label>
        <input v-model="form.confirmPassword" type="password" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      <!-- Registration sends verification email, user needs to verify before login -->
      <button type="button" :disabled="loading" class="btn-primary" @click="onSubmit">
        {{ loading ? 'Đang tạo...' : 'Tạo tài khoản' }}
      </button>
      <NuxtLink to="/auth/login" class="ml-3 underline">Đăng nhập</NuxtLink>
    </form>
  </div>
  
</template>


