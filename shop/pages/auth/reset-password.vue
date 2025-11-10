<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'nuxt/app'
import { useCustomersService } from '~/services/customers'

const router = useRouter()
const route = useRoute()
const { resetPassword } = useCustomersService()

const form = reactive({ 
  password: '', 
  confirmPassword: '',
  token: route.query.token as string || ''
})
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
    await resetPassword(form.token, form.password)
    alert('Đặt lại mật khẩu thành công! Bạn có thể đăng nhập với mật khẩu mới.')
    router.push('/auth/login')
  } catch (e: any) {
    err.value = e?.data?.detail || e?.data?.message || 'Reset password failed'
  } finally {
    loading.value = false
  }
}

// Auto-populate token from URL
onMounted(() => {
  if (route.query.token) {
    form.token = route.query.token as string
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-10 max-w-md">
    <h1 class="text-2xl font-semibold mb-6">Đặt lại mật khẩu</h1>
    <form class="space-y-4" @submit.prevent="onSubmit">
      <div>
        <label class="block text-sm">Token đặt lại</label>
        <input v-model="form.token" class="border rounded w-full p-2" readonly />
      </div>
      <div>
        <label class="block text-sm">Mật khẩu mới</label>
        <input type="password" v-model="form.password" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Xác nhận mật khẩu mới</label>
        <input type="password" v-model="form.confirmPassword" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Đang đặt lại...' : 'Đặt lại mật khẩu' }}
      </button>
      <NuxtLink to="/auth/login" class="ml-3 underline">Quay lại đăng nhập</NuxtLink>
    </form>
  </div>
</template>
