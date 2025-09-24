<template>
  <div class="bg-white rounded-lg shadow-sm border">
    <div class="px-4 py-3 border-b border-gray-200">
      <h3 class="text-lg font-semibold text-gray-800">Categories</h3>
    </div>

    <div class="p-4">
      <!-- All Products -->
      <button
        @click="selectCategory(null)"
        :class="[
          'block w-full text-left px-3 py-2 rounded-md transition-colors mb-2',
          selectedCategoryId === null
            ? 'bg-orange-100 text-orange-700 font-medium'
            : 'hover:bg-gray-100 text-gray-700',
        ]"
      >
        All Products
      </button>

      <!-- Categories -->
      <button
        v-for="category in categories"
        :key="category.id"
        @click="selectCategory(category.id)"
        :class="[
          'block w-full text-left px-3 py-2 rounded-md transition-colors mb-2',
          selectedCategoryId === category.id
            ? 'bg-orange-100 text-orange-700 font-medium'
            : 'hover:bg-gray-100 text-gray-700',
        ]"
      >
        {{ category.name.origin }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductCategory } from "~/services/products";

interface Props {
  categories: ProductCategory[];
  selectedCategoryId?: string | null;
}

const props = withDefaults(defineProps<Props>(), {
  selectedCategoryId: null,
});

const emit = defineEmits<{
  selectCategory: [categoryId: string | null];
}>();

const selectCategory = (categoryId: string | number | null) => {
  if (categoryId === null) return emit("selectCategory", null);
  emit("selectCategory", String(categoryId));
};
</script>
