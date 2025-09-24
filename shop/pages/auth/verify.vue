<script setup lang="ts">
import { useCustomersService } from '~/services/customers'

const router = useRouter()
const route = useRoute()
const { verify } = useCustomersService()

const form = reactive({ 
  email: '', 
  password: '', 
  confirmPassword: '',
  first_name: '',
  last_name: '',
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
    await verify({ 
      token: form.token,
      password: form.password,
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name
    })
    alert('Xác thực thành công! Bạn có thể đăng nhập ngay bây giờ.')
    router.push('/auth/login')
  } catch (e: any) {
    err.value = e?.data?.detail || e?.data?.error || 'Verification failed'
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
    <h1 class="text-2xl font-semibold mb-6">Xác thực tài khoản</h1>
    <form class="space-y-4" @submit.prevent="onSubmit">
      <div>
        <label class="block text-sm">Token xác thực</label>
        <input v-model="form.token" class="border rounded w-full p-2" readonly />
      </div>
      <div>
        <label class="block text-sm">Email</label>
        <input v-model="form.email" type="email" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Họ</label>
        <input v-model="form.first_name" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Tên</label>
        <input v-model="form.last_name" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Mật khẩu</label>
        <input type="password" v-model="form.password" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Xác nhận mật khẩu</label>
        <input type="password" v-model="form.confirmPassword" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Đang xác thực...' : 'Xác thực tài khoản' }}
      </button>
      <NuxtLink to="/auth/login" class="ml-3 underline">Quay lại đăng nhập</NuxtLink>
    </form>
  </div>
</template>
