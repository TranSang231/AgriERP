<script setup lang="ts">
import type { CartItem } from "~/stores/cart";
import { useCartStore } from "~/stores/cart";
import { useCurrency } from "~/composables/useCurrency";

const cartStore = useCartStore();
const { format } = useCurrency();

interface Props {
  item: CartItem & { image?: string };
}
const props = defineProps<Props>();

const emit = defineEmits<{
  updateQty: [productId: number, qty: number];
  removeItem: [productId: number];
}>();

const increaseQty = () => {
  emit("updateQty", props.item.productId, props.item.qty + 1);
};
const decreaseQty = () => {
  if (props.item.qty > 1) {
    emit("updateQty", props.item.productId, props.item.qty - 1);
  }
};
const removeItem = () => {
  emit("removeItem", props.item.productId);
};
</script>

<template>
  <div
    class="flex items-center space-x-4 py-4 px-6 border-b border-gray-200 last:border-b-0"
  >
    <input
      type="checkbox"
      :checked="item.selected"
      @change="cartStore.toggleItemSelected(item.productId)"
      class="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 cursor-pointer flex-shrink-0"
    />

    <div class="flex-shrink-0 w-16 h-16 bg-gray-100 rounded-md overflow-hidden">
      <img
        :src="item.image || '/placeholder-product.jpg'"
        :alt="item.name"
        class="w-full h-full object-cover"
      />
    </div>
    -->
    <div class="flex-1 min-w-0">
      <h4 class="text-sm font-medium text-gray-900 truncate">
        {{ item.name }}
      </h4>
      <div class="text-sm">
        <span
          v-if="item.originalPrice && item.originalPrice > item.price"
          class="text-gray-400 line-through mr-2"
          >{{ format(item.originalPrice) }}</span
        >
        <span class="text-gray-900 font-medium">{{ format(item.price) }}</span>
      </div>
    </div>

    <div class="flex items-center space-x-2">
      <button
        @click="decreaseQty"
        :disabled="item.qty <= 1"
        class="w-8 h-8 flex items-center justify-center bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 rounded-full transition-colors"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M20 12H4"
          ></path>
        </svg>
      </button>

      <span class="w-8 text-center text-sm font-medium">{{ item.qty }}</span>

      <button
        @click="increaseQty"
        class="w-8 h-8 flex items-center justify-center bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          ></path>
        </svg>
      </button>
    </div>

    <div class="text-sm font-medium text-gray-900 w-20 text-right">
      {{ format(item.price * item.qty) }}
    </div>

    <button
      @click="removeItem"
      class="text-gray-400 hover:text-red-500 transition-colors"
    >
      <svg
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
        ></path>
      </svg>
    </button>
  </div>
</template>
