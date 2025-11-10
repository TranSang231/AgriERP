<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'nuxt/app'
import { useCustomersService } from '~/services/customers'

const { forgotPassword } = useCustomersService()

const form = reactive({ email: '' })
const loading = ref(false)
const err = ref('')
const success = ref(false)

async function onSubmit() {
  loading.value = true
  err.value = ''
  try {
    await forgotPassword(form.email)
    success.value = true
  } catch (e: any) {
    err.value = e?.data?.detail || e?.data?.message || 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-10 max-w-md">
    <h1 class="text-2xl font-semibold mb-6">Quên mật khẩu</h1>
    
    <div v-if="success" class="p-4 bg-green-100 border border-green-300 rounded mb-4">
      <p class="text-green-800">
        Email đặt lại mật khẩu đã được gửi! Vui lòng kiểm tra hộp thư của bạn.
      </p>
      <NuxtLink to="/auth/login" class="underline text-green-700">Quay lại đăng nhập</NuxtLink>
    </div>

    <form v-else class="space-y-4" @submit.prevent="onSubmit">
      <div>
        <label class="block text-sm">Email</label>
        <input v-model="form.email" type="email" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Đang gửi...' : 'Gửi email đặt lại' }}
      </button>
      <NuxtLink to="/auth/login" class="ml-3 underline">Quay lại đăng nhập</NuxtLink>
    </form>
  </div>
</template>
