<template>
  <div class="bg-white rounded-lg shadow-sm border p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Filters</h3>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
      <input
        v-model="localFilters.search"
        @input="onSearchInput"
        @compositionstart="onCompositionStart"
        @compositionend="onCompositionEnd"
        type="text"
        placeholder="Search products..."
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      />
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
      <select
        v-model="localFilters.category"
        @change="applyFilters"
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
      >
        <option value="">All Categories</option>
        <option
          v-for="category in propsCategories"
          :key="getCategoryId(category) || getCategoryLabel(category)"
          :value="getCategoryId(category)"
        >
          {{ getCategoryLabel(category) }}
        </option>
      </select>
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
      <div class="grid grid-cols-2 gap-2">
        <input
          v-model.number="localFilters.min_price"
          @input="debouncedPriceFilterHandler"
          type="number"
          placeholder="Min"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
        <input
          v-model.number="localFilters.max_price"
          @input="debouncedPriceFilterHandler"
          type="number"
          placeholder="Max"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
      </div>
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
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
import { ref, watch, onUnmounted, computed } from "vue";
import type { ProductCategory, ProductFilter } from "~/services/products";
import { debounce } from "lodash";

// Props & emits
interface Props {
  categories?: ProductCategory[] | any[];
  filters?: Partial<ProductFilter>;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  updateFilters: [filters: ProductFilter];
  clearFilters: [];
}>();

// Default filter values to ensure consistent shape
const defaultFilters = {
  page: 1,
  page_size: 20,
  search: "",
  category: "",
  min_price: null,
  max_price: null,
  ordering: "",
} as unknown as ProductFilter;

// Initialize localFilters merging defaults + incoming props.filters (if any)
const localFilters = ref<ProductFilter>({ ...defaultFilters, ...(props.filters || {}) });

// Keep localFilters in sync when parent updates filters, but preserve defaults
watch(
  () => props.filters,
  (newFilters) => {
    localFilters.value = { ...defaultFilters, ...(newFilters || {}) } as ProductFilter;
  },
  { deep: true }
);

// Make a safe copy of categories so template can iterate even if undefined
const propsCategories = computed(() => props.categories || []);

// Helper to extract a stable id for a category (supports different shapes)
function getCategoryId(category: any): string {
  if (!category) return "";
  if (typeof category === "string") return category;
  return category.id ?? category._id ?? category.uuid ?? category.key ?? "";
}

// Helper to get a human-readable label for a category
function getCategoryLabel(category: any): string {
  if (!category) return "";
  if (typeof category === "string") return category;
  // if name is nested object like { origin: '...' }
  const name = category.name ?? category.title ?? category.label;
  if (!name) {
    // fallback to JSON preview of id (rare)
    return String(getCategoryId(category)) || "";
  }
  if (typeof name === "string") return name;
  if (typeof name === "object" && name.origin) return name.origin;
  // if it's an array or other nested shape, try first string
  if (Array.isArray(name) && name.length) {
    return typeof name[0] === "string" ? name[0] : JSON.stringify(name[0]);
  }
  return String(name);
}

// Helper: sanitize numeric fields (convert empty/NaN to null) - fix bug: don't convert null -> 0
function coerceNumberToNullable(value: any): number | null {
  if (value === null || value === undefined || value === "") return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function sanitizeFilters(f: ProductFilter): ProductFilter {
  const res: any = { ...f };
  res.min_price = coerceNumberToNullable(res.min_price);
  res.max_price = coerceNumberToNullable(res.max_price);
  res.category = res.category ?? "";
  res.ordering = res.ordering ?? "";
  res.page = Number(res.page) || defaultFilters.page;
  res.page_size = Number(res.page_size) || defaultFilters.page_size;
  // Ensure search is a trimmed string
  res.search = typeof res.search === "string" ? res.search.trim() : (res.search ?? "");
  return res as ProductFilter;
}

const applyFilters = () => {
  // Reset page to 1 when applying filters from UI
  localFilters.value.page = 1;
  const payload = sanitizeFilters(localFilters.value as ProductFilter);
  emit("updateFilters", { ...payload });
};

// Debounced handlers for search and price inputs
const debouncedSearch = debounce(() => {
  applyFilters();
}, 500);

const debouncedPriceFilter = debounce(() => {
  localFilters.value.page = 1;
  applyFilters();
}, 1000);

// We will call this wrapper from template input (handles composition)
const isComposing = ref(false);

function onCompositionStart() {
  isComposing.value = true;
}

function onCompositionEnd() {
  // end composition -> update and trigger debounced search immediately
  isComposing.value = false;
  // call debounced search once composition ends
  localFilters.value.page = 1;
  debouncedSearch();
}

// Called on every input event; only trigger debouncedSearch if not composing
function onSearchInput() {
  // localFilters.search is already updated via v-model
  if (!isComposing.value) {
    localFilters.value.page = 1;
    debouncedSearch();
  }
}

// Separate wrapper for price inputs so we can cancel safely
function debouncedPriceFilterHandler() {
  localFilters.value.page = 1;
  debouncedPriceFilter();
}

// Ensure we cancel debounced timers on unmount to avoid memory leaks
onUnmounted(() => {
  debouncedSearch.cancel?.();
  debouncedPriceFilter.cancel?.();
});

const clearFilters = () => {
  localFilters.value = { ...defaultFilters } as ProductFilter;
  // notify parent with cleared/default filters
  emit("updateFilters", { ...localFilters.value });
  // keep legacy event for backward compatibility
  emit("clearFilters");
};
</script>