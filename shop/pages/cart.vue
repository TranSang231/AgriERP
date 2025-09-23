<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
      <NuxtLink to="/" class="hover:text-orange-600">Home</NuxtLink>
      <span>/</span>
      <span class="text-gray-900">Shopping Cart</span>
    </nav>

    <h1 class="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

    <!-- Empty Cart -->
    <div v-if="cart.items.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">🛒</div>
      <h2 class="text-xl font-semibold text-gray-700 mb-2">
        Your cart is empty
      </h2>
      <p class="text-gray-500 mb-6">Add some products to get started</p>
      <NuxtLink
        to="/products"
        class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
      >
        Continue Shopping
      </NuxtLink>
    </div>

    <!-- Cart Items -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Cart Items List -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow-sm border">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">
              Cart Items ({{ cart.count }})
            </h2>
          </div>

          <div class="divide-y divide-gray-200">
            <CartItem
              v-for="item in cartItemsWithImages"
              :key="item.productId"
              :item="item"
              @updateQty="updateQuantity"
              @removeItem="removeItem"
            />
          </div>
        </div>

        <!-- Continue Shopping -->
        <div class="mt-6">
          <NuxtLink
            to="/products"
            class="inline-flex items-center text-orange-600 hover:text-orange-700 font-medium"
          >
            <svg
              class="mr-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 19l-7-7 7-7"
              ></path>
            </svg>
            Continue Shopping
          </NuxtLink>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow-sm border sticky top-4">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Order Summary</h2>
          </div>

          <div class="px-6 py-4 space-y-4">
            <!-- Subtotal -->
            <div class="flex justify-between">
              <span class="text-gray-600"
                >Subtotal ({{ cart.count }} items)</span
              >
              <span class="font-medium">${{ cart.total.toFixed(2) }}</span>
            </div>

            <!-- Shipping -->
            <div class="flex justify-between">
              <span class="text-gray-600">Shipping</span>
              <span class="font-medium text-green-600">Free</span>
            </div>

            <!-- Tax -->
            <div class="flex justify-between">
              <span class="text-gray-600">Tax</span>
              <span class="font-medium">${{ tax.toFixed(2) }}</span>
            </div>

            <div class="border-t border-gray-200 pt-4">
              <div class="flex justify-between text-lg font-bold">
                <span>Total</span>
                <span class="text-orange-600"
                  >${{ totalWithTax.toFixed(2) }}</span
                >
              </div>
            </div>
          </div>

          <div class="px-6 pb-6">
            <button
              @click="proceedToCheckout"
              class="w-full bg-orange-500 hover:bg-orange-600 text-white py-3 px-4 rounded-lg font-semibold transition-colors mb-3"
            >
              Proceed to Checkout
            </button>

            <button
              @click="clearCart"
              class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium transition-colors"
            >
              Clear Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "~/stores/cart";
import CartItem from "~/components/CartItem.vue";

const cart = useCartStore();
const router = useRouter();

// Add image property to cart items (you can enhance this with actual product data)
const cartItemsWithImages = computed(() => {
  return cart.items.map((item) => ({
    ...item,
    image: "/placeholder-product.jpg", // You can fetch actual product images here
  }));
});

// Tax calculation (8% tax rate)
const tax = computed(() => cart.total * 0.08);
const totalWithTax = computed(() => cart.total + tax.value);

const updateQuantity = (productId: number, quantity: number) => {
  cart.setQty(productId, quantity);
};

const removeItem = (productId: number) => {
  cart.remove(productId);
};

const clearCart = () => {
  if (confirm("Are you sure you want to clear your cart?")) {
    cart.clear();
  }
};

const proceedToCheckout = () => {
  router.push("/checkout");
};

// SEO
useHead({
  title: "Shopping Cart - AgriShop",
  meta: [
    {
      name: "description",
      content:
        "Review your cart and proceed to checkout for your agricultural supplies.",
    },
  ],
});
</script>
