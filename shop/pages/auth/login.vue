<script setup lang="ts">
const router = useRouter()
const { login } = useCustomersService()
const auth = useAuthStore()

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
    <h1 class="text-2xl font-semibold mb-6">Login</h1>
    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <label class="block text-sm">Email or Phone</label>
        <input v-model="form.username" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Password</label>
        <input type="password" v-model="form.password" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      <button :disabled="loading" class="bg-black text-white rounded px-4 py-2">
        {{ loading ? 'Signing in...' : 'Login' }}
      </button>
      <NuxtLink to="/auth/register" class="ml-3 underline">Create an account</NuxtLink>
    </form>
  </div>
  
</template>


