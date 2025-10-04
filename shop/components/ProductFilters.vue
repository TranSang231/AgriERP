<template>
  <div class="bg-white rounded-lg shadow-sm border p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Filters</h3>

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

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Category</label
      >
      <select
        v-model="localFilters.category"
        @change="applyFilters"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="">All Categories</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name.origin }}
        </option>
      </select>
    </div>

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

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2"
        >Sort By</label
      >
      <select
        v-model="localFilters.ordering"
        @change="applyFilters"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="">Default</option>
        <option value="name">Name (A-Z)</option>
        <option value="-name">Name (Z-A)</option>
        <option value="price">Price (Low to High)</option>
        <option value="-price">Price (High to Low)</option>
        <option value="-created_at">Newest</option>
        <option value="created_at">Oldest</option>
      </select>
    </div>

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
import { debounce } from "lodash";

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

const debouncedSearch = debounce(() => {
  applyFilters();
}, 500);

const debouncedPriceFilter = debounce(() => {
  applyFilters();
}, 1000);

const clearFilters = () => {
  localFilters.value = { page: 1, page_size: 20 };
  emit("clearFilters");
};
</script>
