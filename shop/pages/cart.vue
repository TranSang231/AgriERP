<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useCartStore } from '~/stores/cart'
import { useCurrency } from '~/composables/useCurrency'
const cart = useCartStore()
const { format } = useCurrency()
const router = useRouter()

// TODO(cart-sync): When adding items, verify latest price/in_stock from /products/{id}
// Consider server-side cart via /carts if needed for multi-device sync
// TODO(cart-ui): Add remove confirmation and empty-state CTA to continue shopping
// TODO(cart-tax-shipping): Display shipping fee and tax breakdown when backend is ready

</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-semibold mb-4">Cart</h1>
    <div v-if="cart.items.length === 0" class="text-gray-500">Your cart is empty.</div>
    <div v-else class="space-y-4">
      <div v-for="i in cart.items" :key="i.productId" class="flex items-center justify-between border p-3 rounded">
        <div>
          <div class="font-medium">{{ i.name }}</div>
          <div class="text-sm text-gray-500">{{ format(i.price) }}</div>
        </div>
        <div class="flex items-center gap-2">
          <input type="number" min="1" v-model.number="i.qty" class="border rounded w-20 p-1" />
          <button @click="cart.remove(i.productId)" class="text-red-600">Remove</button>
        </div>
      </div>
      <div class="flex items-center justify-between mt-6">
        <div class="text-lg">Total: <span class="font-semibold">{{ format(cart.total) }}</span></div>
        <button @click="router.push('/checkout')" class="btn-primary">Thanh toán</button>
      </div>
    </div>
  </div>
</template>


