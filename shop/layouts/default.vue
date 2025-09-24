<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b bg-white/90 sticky top-0 z-40 backdrop-blur">
      <div class="container mx-auto px-4 py-3 flex items-center gap-6">
        <NuxtLink to="/" class="flex items-center gap-2">
          <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-primary-600 text-white font-bold">O</span>
          <span class="font-semibold text-lg">Organic Shop</span>
        </NuxtLink>
        <div class="relative flex-1 max-w-2xl">
          <input placeholder="Tìm sản phẩm..." class="w-full border rounded pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-300" />
          <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>
        <nav class="ml-auto flex items-center gap-5">
          <NuxtLink to="/" class="hover:underline">Trang chủ</NuxtLink>
          <NuxtLink to="/cart" class="relative hover:underline">
            Giỏ hàng
            <span v-if="cart.count" class="absolute -top-2 -right-3 badge">{{ cart.count }}</span>
          </NuxtLink>
          <template v-if="auth.isAuthenticated">
            <button @click="onLogout" class="link-primary">Đăng xuất</button>
          </template>
          <template v-else>
            <NuxtLink to="/auth/login" class="link-primary">Đăng nhập</NuxtLink>
          </template>
        </nav>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
    <footer class="border-t mt-10 bg-gray-50">
      <div class="container mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
        <div>
          <div class="flex items-center gap-2 mb-3">
            <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-primary-600 text-white font-bold">O</span>
            <span class="font-semibold">Organic Shop</span>
          </div>
          <p class="text-gray-600">Thực phẩm sạch cho gia đình bạn.</p>
        </div>
        <div>
          <div class="font-semibold mb-2">Liên kết</div>
          <ul class="space-y-1 text-gray-600">
            <li><NuxtLink to="/" class="hover:underline">Trang chủ</NuxtLink></li>
            <li><a href="#" class="hover:underline">Giới thiệu</a></li>
            <li><a href="#" class="hover:underline">Liên hệ</a></li>
          </ul>
        </div>
        <div class="text-gray-600">© 2025 Organic Shop</div>
      </div>
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


