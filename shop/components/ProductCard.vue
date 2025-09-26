<template>
  <div
    class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden group"
  >
    <!-- Product Image -->
    <div class="relative overflow-hidden aspect-square">
      <img
        :src="primaryImage"
        :alt="product?.name?.origin || product?.name || 'Product'"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
      />

      <!-- Sale Badge -->
      <div
        v-if="product.sale_price && product.sale_price < product.price"
        class="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 text-xs font-semibold rounded"
      >
        -{{ discountPercentage }}%
      </div>

      <!-- Quick Action Buttons -->
      <div
        class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      >
        <button
          @click="addToCart"
          class="bg-white text-gray-700 hover:bg-orange-500 hover:text-white p-2 rounded-full shadow-md transition-colors duration-200 mb-2 block"
          :disabled="product.stock !== undefined && product.stock !== null && product.stock === 0"
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
              d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 6M7 13l-1.5-6m0 0h.01M16 19h.01m0 0c.55 0 1 .45 1 1s-.45 1-1 1-.99-.45-.99-1 .44-1 .99-1zm-5.99 0h.01m0 0c.55 0 1 .45 1 1s-.45 1-1 1-.99-.45-.99-1 .44-1 .99-1z"
            ></path>
          </svg>
        </button>

        <button
          @click="toggleWishlist"
          class="bg-white text-gray-700 hover:bg-red-500 hover:text-white p-2 rounded-full shadow-md transition-colors duration-200 block"
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
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            ></path>
          </svg>
        </button>
      </div>

      <!-- Out of Stock Overlay -->
      <div
        v-if="product.stock === 0"
        class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      >
        <span class="text-white font-semibold">Out of Stock</span>
      </div>
    </div>

    <!-- Product Info -->
    <div class="p-4">
      <!-- Category -->
      <div class="text-xs text-gray-500 mb-1">
        {{ product.categories?.[0]?.name?.origin || product.category?.name || '' }}
      </div>

      <!-- Product Name -->
      <h3
        class="font-semibold text-gray-800 mb-2 line-clamp-2 hover:text-orange-500 transition-colors cursor-pointer"
      >
        <NuxtLink :to="`/products/${product.id}`">
          {{ product?.name?.origin || product?.name }}
        </NuxtLink>
      </h3>

      <!-- Rating -->
      <div v-if="product.rating" class="flex items-center mb-2">
        <div class="flex items-center">
          <span
            v-for="n in 5"
            :key="n"
            class="text-yellow-400 text-sm"
            :class="
              n <= Math.floor(product.rating) ? 'fill-current' : 'text-gray-300'
            "
          >
            ★
          </span>
        </div>
        <span class="text-xs text-gray-500 ml-1"
          >({{ product.reviews_count || 0 }})</span
        >
      </div>

      <!-- Price -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span
            v-if="product.sale_price && product.sale_price < product.price"
            class="text-lg font-bold text-orange-500"
          >
            ${{ Number(product.sale_price).toFixed(2) }}
          </span>
          <span
            :class="[
              product.sale_price && product.sale_price < product.price
                ? 'text-sm text-gray-400 line-through'
                : 'text-lg font-bold text-gray-900',
            ]"
          >
            ${{ Number(product.price).toFixed(2) }}
          </span>
        </div>

        <!-- Stock Info -->
        <div class="text-xs text-gray-500">Stock: {{ product.in_stock ?? product.stock }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from "~/services/products";
import { useCartStore } from "~/stores/cart";
import { computed } from "vue";

interface Props {
  product: Product;
}

const props = defineProps<Props>();
const cartStore = useCartStore();
const primaryImage = computed(() => {
  const images = (props.product as any)?.images;
  if (Array.isArray(images) && images.length > 0) {
    const first = images[0] as any;
    if (first && typeof first === "object" && "image" in first) return first.image;
    if (typeof first === "string") return first;
  }
  return (
    (props.product as any)?.image ||
    (props.product as any)?.thumbnail ||
    "/placeholder-product.jpg"
  );
});

onMounted(() => {
  // console.log("[ProductCard] mounted product:", props.product);
});

watch(
  () => props.product,
  (val) => {
    // console.log("[ProductCard] updated product:", val);
  },
  { deep: true, immediate: true }
);

const discountPercentage = computed(() => {
  if (
    props.product.sale_price &&
    props.product.sale_price < props.product.price
  ) {
    return Math.round(
      (1 - props.product.sale_price / props.product.price) * 100
    );
  }
  return 0;
});

const addToCart = () => {
  const hasStockInfo = props.product.stock !== undefined && props.product.stock !== null;
  const canAdd = hasStockInfo ? props.product.stock > 0 : true;
  if (canAdd) {
    cartStore.add({
      productId: props.product.id,
      name: props.product.name,
      price: props.product.sale_price || props.product.price,
      qty: 1,
    });
    // Show success message (you can add toast notification here)
  }
};

const toggleWishlist = () => {
  // Implement wishlist functionality
  console.log("Toggle wishlist for product:", props.product.id);
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.aspect-square {
  aspect-ratio: 1 / 1;
}
</style>
