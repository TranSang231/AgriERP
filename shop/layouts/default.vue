<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <NuxtLink to="/" class="text-2xl font-bold text-orange-600">
            AgriShop
          </NuxtLink>

          <!-- Search Bar -->
          <div class="flex-1 max-w-lg mx-8">
            <div class="relative">
              <input
                v-model="searchQuery"
                @keyup.enter="performSearch"
                type="text"
                placeholder="Search products..."
                class="w-full px-4 py-2 pl-10 pr-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
              <svg
                class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                ></path>
              </svg>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center space-x-4">
            <!-- Orders -->
            <NuxtLink
              to="/orders"
              class="p-2 text-gray-600 hover:text-orange-600 transition-colors"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                ></path>
              </svg>
            </NuxtLink>

            <!-- Cart -->
            <NuxtLink
              to="/cart"
              class="relative p-2 text-gray-600 hover:text-orange-600 transition-colors"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5-6m0 0h.01M16 19h.01m0 0c.55 0 1 .45 1 1s-.45 1-1 1-.99-.45-.99-1 .44-1 .99-1zm-5.99 0h.01m0 0c.55 0 1 .45 1 1s-.45 1-1 1-.99-.45-.99-1 .44-1 .99-1z"
                ></path>
              </svg>
              <!-- Cart Count Badge -->
              <span
                v-if="cart.count > 0"
                class="absolute -top-1 -right-1 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {{ cart.count }}
              </span>
            </NuxtLink>

            <!-- User Menu -->
            <div class="relative" v-if="auth.isAuthenticated">
              <button
                @click="toggleUserMenu"
                class="flex items-center space-x-2 text-gray-600 hover:text-orange-600 transition-colors"
              >
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  ></path>
                </svg>
              </button>

              <!-- User Dropdown -->
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50"
              >
                <NuxtLink
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Profile
                </NuxtLink>
                <NuxtLink
                  to="/orders"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  My Orders
                </NuxtLink>
                <button
                  @click="onLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Logout
                </button>
              </div>
            </div>

            <!-- Login/Register -->
            <div v-else class="flex items-center space-x-2">
              <NuxtLink
                to="/auth/login"
                class="text-gray-600 hover:text-orange-600 transition-colors"
              >
                Login
              </NuxtLink>
              <span class="text-gray-400">|</span>
              <NuxtLink
                to="/auth/register"
                class="text-gray-600 hover:text-orange-600 transition-colors"
              >
                Register
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-16">
      <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">AgriShop</h3>
            <p class="text-gray-400 text-sm">
              Your trusted partner for agricultural products and supplies.
            </p>
          </div>

          <div>
            <h4 class="font-semibold mb-4">Quick Links</h4>
            <ul class="text-sm text-gray-400 space-y-2">
              <li>
                <NuxtLink
                  to="/products"
                  class="hover:text-white transition-colors"
                  >Products</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/categories"
                  class="hover:text-white transition-colors"
                  >Categories</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/about" class="hover:text-white transition-colors"
                  >About Us</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/contact"
                  class="hover:text-white transition-colors"
                  >Contact</NuxtLink
                >
              </li>
            </ul>
          </div>

          <div>
            <h4 class="font-semibold mb-4">Customer Service</h4>
            <ul class="text-sm text-gray-400 space-y-2">
              <li>
                <NuxtLink to="/help" class="hover:text-white transition-colors"
                  >Help Center</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/shipping"
                  class="hover:text-white transition-colors"
                  >Shipping Info</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/returns"
                  class="hover:text-white transition-colors"
                  >Returns</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/faq" class="hover:text-white transition-colors"
                  >FAQ</NuxtLink
                >
              </li>
            </ul>
          </div>

          <div>
            <h4 class="font-semibold mb-4">Contact Info</h4>
            <div class="text-sm text-gray-400 space-y-2">
              <p>📧 support@agrishop.com</p>
              <p>📞 +1 (555) 123-4567</p>
              <p>📍 123 Agriculture St, Farm City</p>
            </div>
          </div>
        </div>

        <div
          class="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400"
        >
          <p>&copy; 2024 AgriShop. All rights reserved.</p>
        </div>

      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useCustomersService } from "~/services/customers";
import { useAuthStore } from "~/stores/auth";
import { useCartStore } from "~/stores/cart";

// Composables
const { searchQuery, performSearch } = useSearch();
const { showUserMenu, toggleUserMenu, closeMenus } = useUI();

// Stores
const auth = useAuthStore();
const cart = useCartStore();

// Services
const { logout } = useCustomersService();

// Methods
const onLogout = async () => {
  try {
    await logout();
    auth.logout(); // Clear auth store
    closeMenus();
    await navigateTo('/auth/login'); // Navigate to login page
    // Show success message after navigation
    const { $toast } = useNuxtApp();
    $toast.success('Đăng xuất thành công');
  } catch (error) {
    console.error("Logout failed:", error);
    // Force navigation even if logout API fails
    auth.logout();
    await navigateTo('/auth/login');
    const { $toast } = useNuxtApp();
    $toast.success('Đăng xuất thành công');
  }
};

// Close menus when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  if (!target.closest(".relative")) {
    closeMenus();
  }
};

// Lifecycle
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
