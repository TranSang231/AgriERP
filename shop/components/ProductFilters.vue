<template>
  <div class="bg-white rounded-lg shadow-sm border p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Filters</h3>

    <!-- Search -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
      <input
        v-model="localFilters.search"
        @input="debouncedSearch"
        type="text"
        placeholder="Search products..."
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      />
    </div>

    <!-- Categories -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Category</label
      >
      <select
        v-model="localFilters.category_id"
        @change="applyFilters"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="">All Categories</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name?.origin || category.description || "Danh mục" }}
        </option>
      </select>
    </div>

    <!-- Price Range -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Price Range</label
      >
      <div class="grid grid-cols-2 gap-2">
        <input
          v-model.number="localFilters.min_price"
          @input="debouncedPriceFilter"
          type="number"
          placeholder="Min"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
        <input
          v-model.number="localFilters.max_price"
          @input="debouncedPriceFilter"
          type="number"
          placeholder="Max"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
      </div>
    </div>

    <!-- Sort -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Sort By</label
      >
      <select
        v-model="localFilters.sort_by"
        @change="applySorting"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="">Default</option>
        <option value="name">Name</option>
        <option value="price">Price</option>
        <option value="created_at">Date Added</option>
        <option value="in_stock">Stock</option>
      </select>
    </div>

    <!-- Sort Order -->
    <div class="mb-6" v-if="localFilters.sort_by">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Sort Order</label
      >
      <select
        v-model="localFilters.sort_order"
        @change="applyFilters"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>

    <!-- Clear Filters -->
    <button
      @click="clearFilters"
      class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-md transition-colors duration-200"
    >
      Clear All Filters
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import type { ProductCategory, ProductFilter } from "~/services/products";

interface Props {
  categories: ProductCategory[];
  filters: ProductFilter;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  updateFilters: [filters: ProductFilter];
  clearFilters: [];
}>();

const localFilters = ref<ProductFilter>({ ...props.filters });

// Watch for external filter changes
watch(
  () => props.filters,
  (newFilters) => {
    localFilters.value = { ...newFilters };
  },
  { deep: true }
);

const applyFilters = () => {
  emit("updateFilters", { ...localFilters.value });
};

const applySorting = () => {
  if (localFilters.value.sort_by && !localFilters.value.sort_order) {
    localFilters.value.sort_order = "asc";
  }
  applyFilters();
};

// Simple debounce implementation
let searchTimeout: NodeJS.Timeout;
const debouncedSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    applyFilters();
  }, 500);
};

let priceTimeout: NodeJS.Timeout;
const debouncedPriceFilter = () => {
  clearTimeout(priceTimeout);
  priceTimeout = setTimeout(() => {
    applyFilters();
  }, 1000);
};

const clearFilters = () => {
  localFilters.value = { page: 1, page_size: 20 };
  emit("clearFilters");
};
</script>
