<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n'; // Import useI18n
import { useCartStore } from "~/stores/cart";
import { useCheckoutStore } from "~/stores/checkout";
import { useCurrency } from "~/composables/useCurrency";
import CartItem from "~/components/CartItem.vue";

const router = useRouter();
const cartStore = useCartStore();
const checkoutStore = useCheckoutStore();
const { format } = useCurrency();
const { t } = useI18n(); // Khởi tạo hàm t để dịch thuật trong script

// Sử dụng storeToRefs để đảm bảo các getter và state giữ được reactivity
const { items, selectedCount, selectedTotal, selectedItems } = storeToRefs(cartStore);

// Các computed property tính toán
const originalSelectedTotal = computed(() => {
  return selectedItems.value.reduce((acc, item: any) => {
    const base = (item.originalPrice ?? item.price) || 0;
    return acc + base * (item.qty || 0);
  }, 0);
});
const productsDiscount = computed(() => Math.max(0, originalSelectedTotal.value - selectedTotal.value));
const tax = computed(() => selectedTotal.value * 0.08);
const totalWithTax = computed(() => selectedTotal.value + tax.value);

// Tải cart từ backend lần đầu
if (!cartStore.hasLoaded && !cartStore.isLoading) {
  cartStore.load();
}

// Computed property để xác định trạng thái của checkbox "Select All".
const isAllSelected = computed(() =>
  items.value.length > 0 && items.value.every(item => item.selected)
);

// Các hàm xử lý sự kiện
const updateQuantity = (productId: number, quantity: number) => {
  cartStore.setQty(productId, quantity);
};
const removeItem = (productId: number) => {
  cartStore.remove(productId);
};
const clearCart = () => {
  if (confirm(t('cart.actions.clearConfirm'))) { // Sử dụng t() cho confirm
    cartStore.clear();
  }
};
const proceedToCheckout = () => {
  if (selectedItems.value.length === 0) {
    alert(t('cart.actions.selectItemWarning')); // Sử dụng t() cho alert
    return;
  }
  checkoutStore.setItems(selectedItems.value);
  router.push("/checkout");
};

// Cấu hình SEO cho trang
useHead({
  title: t('cart.meta.title'), // Sử dụng t() cho SEO
  meta: [
    { name: "description", content: t('cart.meta.description') },
  ],
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <nav class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
      <NuxtLink to="/" class="hover:text-orange-600">{{ $t('cart.breadcrumb.home') }}</NuxtLink>
      <span>/</span>
      <span class="text-gray-900">{{ $t('cart.breadcrumb.cart') }}</span>
    </nav>
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ $t('cart.title') }}</h1>

    <!-- Phần hiển thị khi giỏ hàng trống -->
    <div v-if="!items || items.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">🛒</div>
      <h2 class="text-xl font-semibold text-gray-700 mb-2">{{ $t('cart.empty.title') }}</h2>
      <p class="text-gray-500 mb-6">{{ $t('cart.empty.subtitle') }}</p>
      <NuxtLink to="/products" class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
        {{ $t('cart.empty.continueShopping') }}
      </NuxtLink>
    </div>

    <!-- Bọc toàn bộ phần hiển thị giỏ hàng trong <ClientOnly> -->
    <ClientOnly>
      <div v-if="items && items.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Danh sách sản phẩm trong giỏ hàng -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-sm border">
            <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h2 class="text-lg font-semibold text-gray-900">{{ $t('cart.items.title', { count: cartStore.count }) }}</h2>
              <div class="flex items-center space-x-2">
                  <input type="checkbox" id="selectAll" :checked="isAllSelected" @change="cartStore.toggleSelectAll(!isAllSelected)" class="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 cursor-pointer"/>
                  <label for="selectAll" class="text-sm font-medium text-gray-700 cursor-pointer">{{ $t('cart.items.selectAll') }}</label>
              </div>
            </div>
            <div class="divide-y divide-gray-200">
              <CartItem v-for="(item, index) in items" :key="`${item.productId}-${index}`" :item="item" @updateQty="updateQuantity" @removeItem="removeItem"/>
            </div>
          </div>
          <div class="mt-6">
            <NuxtLink to="/products" class="inline-flex items-center text-orange-600 hover:text-orange-700 font-medium">
              <svg class="mr-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
              {{ $t('cart.actions.continueShopping') }}
            </NuxtLink>
          </div>
        </div>

        <!-- Phần tóm tắt đơn hàng -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm border sticky top-4">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-semibold text-gray-900">{{ $t('cart.summary.title') }}</h2>
            </div>
            <div class="px-6 py-4 space-y-4">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('cart.summary.subtotal', { count: selectedCount }) }}</span>
                <div class="font-medium">
                  <span v-if="productsDiscount > 0" class="text-gray-400 line-through mr-2">{{ format(originalSelectedTotal) }}</span>
                  <span>{{ format(selectedTotal) }}</span>
                </div>
              </div>
              <div v-if="productsDiscount > 0" class="flex justify-between">
                <span class="text-gray-600">{{ $t('cart.summary.discounts') }}</span>
                <span class="font-medium text-green-600">-{{ format(productsDiscount) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('cart.summary.shipping') }}</span>
                <span class="font-medium text-green-600">{{ $t('cart.summary.shippingFree') }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('cart.summary.tax') }}</span>
                <span class="font-medium">{{ format(tax) }}</span>
              </div>
              <div class="border-t border-gray-200 pt-4">
                <div class="flex justify-between text-lg font-bold">
                  <span>{{ $t('cart.summary.total') }}</span>
                  <span class="text-orange-600">{{ format(totalWithTax) }}</span>
                </div>
              </div>
            </div>
            <div class="px-6 pb-6">
              <button @click="proceedToCheckout" class="w-full bg-orange-500 hover:bg-orange-600 text-white py-3 px-4 rounded-lg font-semibold transition-colors mb-3">
                {{ $t('cart.summary.checkoutButton') }}
              </button>
              <button @click="clearCart" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors">
                {{ $t('cart.summary.clearButton') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>