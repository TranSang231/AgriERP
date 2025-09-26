<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from 'pinia'; // Import storeToRefs
import { useCartStore } from "~/stores/cart";
import { useCheckoutStore } from "~/stores/checkout";
import CartItem from "~/components/CartItem.vue";

const router = useRouter();
const cartStore = useCartStore();
const checkoutStore = useCheckoutStore();

// Sử dụng storeToRefs để đảm bảo các getter và state giữ được reactivity
// và có thể sử dụng trực tiếp trong template.
const { items, selectedCount, selectedTotal, selectedItems } = storeToRefs(cartStore);

// Các computed property tính toán thuế và tổng tiền cuối cùng.
// Chúng sẽ tự động cập nhật khi selectedTotal thay đổi.
const tax = computed(() => selectedTotal.value * 0.08);
const totalWithTax = computed(() => selectedTotal.value + tax.value);

// Computed property để xác định trạng thái của checkbox "Select All".
const isAllSelected = computed(() => 
  items.value.length > 0 && items.value.every(item => item.selected)
);

// Các hàm xử lý sự kiện, gọi trực tiếp action từ cartStore.
const updateQuantity = (productId: number, quantity: number) => {
  cartStore.setQty(productId, quantity);
};
const removeItem = (productId: number) => {
  cartStore.remove(productId);
};
const clearCart = () => {
  if (confirm("Are you sure you want to clear your cart?")) {
    cartStore.clear();
  }
};
const proceedToCheckout = () => {
  if (selectedItems.value.length === 0) {
    alert("Please select at least one item to proceed to checkout.");
    return;
  }
  checkoutStore.setItems(selectedItems.value);
  router.push("/checkout");
};

// Cấu hình SEO cho trang
useHead({
  title: "Shopping Cart - AgriShop",
  meta: [
    { name: "description", content: "Review your cart and proceed to checkout for your agricultural supplies." },
  ],
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <nav class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
      <NuxtLink to="/" class="hover:text-orange-600">Home</NuxtLink>
      <span>/</span>
      <span class="text-gray-900">Shopping Cart</span>
    </nav>
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

    <!-- Phần hiển thị khi giỏ hàng trống -->
    <div v-if="!items || items.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">🛒</div>
      <h2 class="text-xl font-semibold text-gray-700 mb-2">Your cart is empty</h2>
      <p class="text-gray-500 mb-6">Add some products to get started</p>
      <NuxtLink to="/products" class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
        Continue Shopping
      </NuxtLink>
    </div>

    <!-- 
      FIX LỖI QUAN TRỌNG: 
      Bọc toàn bộ phần hiển thị giỏ hàng trong <ClientOnly> để tránh lỗi Hydration Mismatch.
      Điều này đảm bảo phần code này chỉ được render ở phía trình duyệt, nơi có localStorage.
    -->
    <ClientOnly>
      <div v-if="items && items.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Danh sách sản phẩm trong giỏ hàng -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-sm border">
            <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h2 class="text-lg font-semibold text-gray-900">Cart Items ({{ cartStore.count }})</h2>
              <div class="flex items-center space-x-2">
                  <input type="checkbox" id="selectAll" :checked="isAllSelected" @change="cartStore.toggleSelectAll(!isAllSelected)" class="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 cursor-pointer"/>
                  <label for="selectAll" class="text-sm font-medium text-gray-700 cursor-pointer">Select All</label>
              </div>
            </div>
            <div class="divide-y divide-gray-200">
              <!-- FIX LỖI QUAN TRỌNG: Nâng cấp :key để đảm bảo tính duy nhất tuyệt đối -->
              <CartItem v-for="(item, index) in items" :key="`${item.productId}-${index}`" :item="item" @updateQty="updateQuantity" @removeItem="removeItem"/>
            </div>
          </div>
          <div class="mt-6">
            <NuxtLink to="/products" class="inline-flex items-center text-orange-600 hover:text-orange-700 font-medium">
              <svg class="mr-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
              Continue Shopping
            </NuxtLink>
          </div>
        </div>

        <!-- Phần tóm tắt đơn hàng -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm border sticky top-4">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-semibold text-gray-900">Order Summary</h2>
            </div>
            <div class="px-6 py-4 space-y-4">
              <div class="flex justify-between">
                <span class="text-gray-600">Subtotal ({{ selectedCount }} items)</span>
                <span class="font-medium">${{ selectedTotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Shipping</span>
                <span class="font-medium text-green-600">Free</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Tax</span>
                <span class="font-medium">${{ tax.toFixed(2) }}</span>
              </div>
              <div class="border-t border-gray-200 pt-4">
                <div class="flex justify-between text-lg font-bold">
                  <span>Total</span>
                  <span class="text-orange-600">${{ totalWithTax.toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <div class="px-6 pb-6">
              <button @click="proceedToCheckout" class="w-full bg-orange-500 hover:bg-orange-600 text-white py-3 px-4 rounded-lg font-semibold transition-colors mb-3">
                Proceed to Checkout
              </button>
              <button @click="clearCart" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors">
                Clear Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>