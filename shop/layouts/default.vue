<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b">
      <div class="container mx-auto px-4 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="font-semibold">Shop</NuxtLink>
        <nav class="flex items-center gap-4">
          <NuxtLink to="/cart">Cart ({{ cart.count }})</NuxtLink>
          <template v-if="auth.isAuthenticated">
            <span class="text-sm">Hi, {{ auth.user?.name || 'Customer' }}</span>
            <button @click="onLogout" class="underline">Logout</button>
          </template>
          <template v-else>
            <NuxtLink to="/auth/login">Login</NuxtLink>
          </template>
        </nav>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
    <footer class="border-t">
      <div class="container mx-auto px-4 py-6 text-sm text-gray-500">© 2025</div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useCustomersService } from '~/services/customers'
const auth = useAuthStore()
const cart = useCartStore()
const { logout } = useCustomersService()

async function onLogout() {
  try { await logout() } finally { /* no-op */ }
}
</script>


