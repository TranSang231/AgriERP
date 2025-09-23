<script setup lang="ts">
const router = useRouter()
const { register } = useCustomersService()
const form = reactive({ email: '', password: '', name: '' })
const loading = ref(false)
const err = ref('')

async function onSubmit() {
  loading.value = true
  err.value = ''
  try {
    await register({ email: form.email, password: form.password, name: form.name })
    router.push('/auth/login')
  } catch (e: any) {
    err.value = e?.data?.detail || 'Register failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-10 max-w-md">
    <h1 class="text-2xl font-semibold mb-6">Create account</h1>
    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <label class="block text-sm">Name</label>
        <input v-model="form.name" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Email</label>
        <input v-model="form.email" type="email" class="border rounded w-full p-2" required />
      </div>
      <div>
        <label class="block text-sm">Password</label>
        <input type="password" v-model="form.password" class="border rounded w-full p-2" required />
      </div>
      <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
      <button :disabled="loading" class="bg-black text-white rounded px-4 py-2">
        {{ loading ? 'Creating...' : 'Create' }}
      </button>
      <NuxtLink to="/auth/login" class="ml-3 underline">Sign in</NuxtLink>
    </form>
  </div>
  
</template>


