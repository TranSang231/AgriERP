<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <NuxtLink to="/" class="text-2xl font-bold text-orange-600">
            AgriShop
          </NuxtLink>

          <div class="flex-1 max-w-lg mx-8">
            <div class="relative">
              <input
                v-model="searchQuery"
                @keyup.enter="performSearch"
                type="text"
                :placeholder="$t('header.searchPlaceholder')"
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

          <div class="flex items-center space-x-4">
            <LanguageSwitcher />

            <NuxtLink
              to="/orders"
              class="p-2 text-gray-600 hover:text-orange-600 transition-colors"
              :aria-label="$t('header.orders')"
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

            <NuxtLink
              to="/cart"
              class="relative p-2 text-gray-600 hover:text-orange-600 transition-colors"
              :aria-label="$t('header.cart')"
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
              <span
                v-if="auth.isAuthenticated && cart.count > 0"
                class="absolute -top-1 -right-1 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {{ cart.count }}
              </span>
            </NuxtLink>

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

              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50"
              >
                <NuxtLink
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  {{ $t('header.profile') }}
                </NuxtLink>
                <NuxtLink
                  to="/orders"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  {{ $t('header.myOrders') }}
                </NuxtLink>
                <button
                  @click="onLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  {{ $t('header.logout') }}
                </button>
              </div>
            </div>

            <div v-else class="flex items-center space-x-2">
              <NuxtLink
                to="/auth/login"
                class="text-gray-600 hover:text-orange-600 transition-colors"
              >
                {{ $t('header.login') }}
              </NuxtLink>
              <span class="text-gray-400">|</span>
              <NuxtLink
                to="/auth/register"
                class="text-gray-600 hover:text-orange-600 transition-colors"
              >
                {{ $t('header.register') }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main>
      <slot />
    </main>

    <footer class="bg-gray-800 text-white mt-16">
      <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">AgriShop</h3>
            <p class="text-gray-400 text-sm">
              {{ $t('footer.tagline') }}
            </p>
          </div>

          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.quickLinks') }}</h4>
            <ul class="text-sm text-gray-400 space-y-2">
              <li>
                <NuxtLink
                  to="/products"
                  class="hover:text-white transition-colors"
                  >{{ $t('footer.products') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/categories"
                  class="hover:text-white transition-colors"
                  >{{ $t('footer.categories') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/about" class="hover:text-white transition-colors"
                  >{{ $t('footer.aboutUs') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/contact"
                  class="hover:text-white transition-colors"
                  >{{ $t('footer.contact') }}</NuxtLink
                >
              </li>
            </ul>
          </div>

          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.customerService') }}</h4>
            <ul class="text-sm text-gray-400 space-y-2">
              <li>
                <NuxtLink to="/help" class="hover:text-white transition-colors"
                  >{{ $t('footer.helpCenter') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/shipping"
                  class="hover:text-white transition-colors"
                  >{{ $t('footer.shippingInfo') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink
                  to="/returns"
                  class="hover:text-white transition-colors"
                  >{{ $t('footer.returns') }}</NuxtLink
                >
              </li>
              <li>
                <NuxtLink to="/faq" class="hover:text-white transition-colors"
                  >{{ $t('footer.faq') }}</NuxtLink
                >
              </li>
            </ul>
          </div>

          <div>
            <h4 class="font-semibold mb-4">{{ $t('footer.contactInfo') }}</h4>
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
          <p>{{ $t('footer.copyright') }}</p>
        </div>

      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, watch } from "vue";
import LanguageSwitcher from "~/components/LanguageSwitcher.vue";
import { useCustomersService } from "~/services/customers";
import { useAuthStore } from "~/stores/auth";
import { useCartStore } from "~/stores/cart";

const { searchQuery, performSearch } = useSearch();
const { showUserMenu, toggleUserMenu, closeMenus } = useUI();

const auth = useAuthStore();
const cart = useCartStore();

const { logout } = useCustomersService();

const onLogout = async () => {
  try {
    const result = await logout();
    auth.logout();
    cart.clear(); // Clear cart items when logging out
    closeMenus();
    await navigateTo('/auth/login'); 
    const { $toast } = useNuxtApp();
    if (result?.success) {
      $toast.success('Đăng xuất thành công');
    }
  } catch (error) {
    console.error("Logout failed:", error);
    auth.logout();
    cart.clear(); // Clear cart items even if logout API fails
    await navigateTo('/auth/login');
    const { $toast } = useNuxtApp();
    $toast.success('Đăng xuất thành công');
  }
};

const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  if (!target.closest(".relative")) {
    closeMenus();
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  try { cart.load() } catch (_) {}
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

watch(
  () => auth.isAuthenticated,
  () => {
    try { cart.load() } catch (_) {}
  }
)
</script>