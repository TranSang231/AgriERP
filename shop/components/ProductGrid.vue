<template>
  <div class="container mx-auto px-4">
    <div
      v-if="loading"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <div
        v-for="n in 8"
        :key="n"
        class="bg-white rounded-lg shadow-md overflow-hidden animate-pulse"
      >
        <div class="aspect-square bg-gray-300"></div>
        <div class="p-4">
          <div class="h-4 bg-gray-300 rounded mb-2"></div>
          <div class="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
          <div class="h-6 bg-gray-300 rounded w-1/2"></div>
        </div>
      </div>
    </div>

    <div
      v-else-if="products.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>

    <div v-else class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">📦</div>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">
        No Products Found
      </h3>
      <p class="text-gray-500">Try adjusting your search or filter criteria</p>
    </div>

    <div v-if="hasMore && !loading" class="text-center mt-8">
      <button
        @click="loadMore"
        :disabled="loadingMore"
        class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loadingMore" class="flex items-center">
          <svg
            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Loading...
        </span>
        <span v-else>Load More Products</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from "~/services/products";
import ProductCard from "./ProductCard.vue";

interface Props {
  products: Product[];
  loading?: boolean;
  loadingMore?: boolean;
  hasMore?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  loadingMore: false,
  hasMore: false,
});

const emit = defineEmits<{
  loadMore: [];
}>();

const loadMore = () => {
  emit("loadMore");
};
</script>

<style scoped>
.aspect-square {
  aspect-ratio: 1 / 1;
}
</style>
