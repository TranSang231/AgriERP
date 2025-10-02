<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
      <NuxtLink to="/" class="hover:text-orange-600">Home</NuxtLink>
      <span>/</span>
      <span class="text-gray-900">Products</span>
    </nav>

    <!-- Page Header -->
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Products</h1>
      <div class="text-sm text-gray-600">
        {{ productsStore.pagination.count }} products found
      </div>
    </div>

    <div class="flex gap-8">
      <!-- Sidebar -->
      <aside class="w-64 flex-shrink-0">
        <!-- Categories -->
        <CategoryMenu
          :categories="categories"
          :selectedCategoryId="selectedCategoryId"
          @selectCategory="handleCategorySelect"
        />

        <!-- Filters -->
        <div class="mt-6">
          <ProductFilters
            :categories="categories"
            :filters="productsStore.filters"
            @updateFilters="handleFiltersUpdate"
            @clearFilters="handleClearFilters"
          />
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1">
        <!-- Mobile Filter Toggle -->
        <div class="lg:hidden mb-4">
          <button
            @click="showMobileFilters = !showMobileFilters"
            class="flex items-center space-x-2 bg-white border border-gray-300 px-4 py-2 rounded-md"
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
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
              ></path>
            </svg>
            <span>Filters</span>
          </button>
        </div>

        <!-- Mobile Filters Modal -->
        <div
          v-if="showMobileFilters"
          class="fixed inset-0 bg-black bg-opacity-50 z-50 lg:hidden"
          @click="showMobileFilters = false"
        >
          <div
            class="fixed right-0 top-0 h-full w-80 bg-white p-6 overflow-y-auto"
            @click.stop
          >
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold">Filters</h3>
              <button @click="showMobileFilters = false">
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  ></path>
                </svg>
              </button>
            </div>

            <CategoryMenu
              :categories="categories"
              :selectedCategoryId="selectedCategoryId"
              @selectCategory="handleCategorySelect"
            />

            <div class="mt-6">
              <ProductFilters
                :categories="categories"
                :filters="productsStore.filters"
                @updateFilters="handleFiltersUpdate"
                @clearFilters="handleClearFilters"
              />
            </div>
          </div>
        </div>

        <!-- Sort Options -->
        <div class="flex items-center justify-between mb-6">
          <div class="text-sm text-gray-600">
            Showing {{ productsStore.products.length }} of
            {{ productsStore.pagination.count }} products
          </div>

          <div class="flex items-center space-x-4">
            <label class="text-sm text-gray-600">Sort by:</label>
            <select
              v-model="sortOption"
              @change="handleSort"
              class="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="">Default</option>
              <option value="name">Name (A-Z)</option>
              <option value="-name">Name (Z-A)</option>
              <option value="price">Price (Low to High)</option>
              <option value="-price">Price (High to Low)</option>
              <option value="-created_at">Newest</option>
            </select>
          </div>
        </div>

        <!-- Products Grid -->
        <ProductGrid
          :products="productsStore.products"
          :loading="productsStore.loading"
          :loadingMore="loadingMore"
          :hasMore="productsStore.hasNextPage"
          @loadMore="loadMore"
        />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useProductsStore } from "~/stores/products";
import { useProductsService } from "~/services/products";

// Components
import ProductGrid from "~/components/ProductGrid.vue";
import ProductFilters from "~/components/ProductFilters.vue";
import CategoryMenu from "~/components/CategoryMenu.vue";

const route = useRoute();
const router = useRouter();
const productsStore = useProductsStore();
const { getCategories } = useProductsService();

// Reactive data
const categories = ref([]);
const selectedCategoryId = ref<string | null>(null);
const showMobileFilters = ref(false);
const sortOption = ref("");
const loadingMore = ref(false);

// Load initial data
onMounted(async () => {
  // Load categories
  const { data } = await getCategories();
  if (data.value) {
    categories.value = data.value as any;
  }

  // Set initial filters from URL
  const initialFilters = {
    search: (route.query.search as string) || "",
    category: (route.query.category as string) || undefined,
    min_price: route.query.min_price
      ? parseInt(route.query.min_price as string)
      : undefined,
    max_price: route.query.max_price
      ? parseInt(route.query.max_price as string)
      : undefined,
    ordering: (route.query.ordering as string) || "",
    page: 1,
    page_size: 20,
  };

  selectedCategoryId.value = initialFilters.category || null;
  sortOption.value = initialFilters.ordering;

  // Set filters and fetch products
  productsStore.setFilters(initialFilters);
  await productsStore.fetchProducts();
});

// Watch route changes
watch(
  () => route.query,
  async (newQuery) => {
  const filters = {
      search: (newQuery.search as string) || "",
      category: (newQuery.category as string) || undefined,
      min_price: newQuery.min_price
        ? parseInt(newQuery.min_price as string)
        : undefined,
      max_price: newQuery.max_price
        ? parseInt(newQuery.max_price as string)
        : undefined,
      ordering: (newQuery.ordering as string) || "",
      page: 1,
      page_size: 20,
    };

    selectedCategoryId.value = filters.category || null;
    sortOption.value = filters.ordering;

    productsStore.setFilters(filters);
    await productsStore.fetchProducts();
  }
);

// Event handlers
const handleCategorySelect = async (categoryId: string | null) => {
  selectedCategoryId.value = categoryId;
  showMobileFilters.value = false;

  const query = { ...route.query };
  if (categoryId) {
    query.category = categoryId;
  } else {
    delete query.category;
  }

  router.push({ query });
};

const handleFiltersUpdate = async (filters: any) => {
  const query: any = { ...route.query };

  if (filters.search) query.search = filters.search;
  else delete query.search;

  if (filters.min_price) query.min_price = filters.min_price.toString();
  else delete query.min_price;

  if (filters.max_price) query.max_price = filters.max_price.toString();
  else delete query.max_price;

  if (filters.ordering) query.ordering = filters.ordering;
  else delete query.ordering;

  router.push({ query });
  showMobileFilters.value = false;
};

const handleClearFilters = () => {
  selectedCategoryId.value = null;
  sortOption.value = "";
  router.push({ query: {} });
  showMobileFilters.value = false;
};

const handleSort = () => {
  const query = { ...route.query };
  if (sortOption.value) {
    query.ordering = sortOption.value;
  } else {
    delete query.ordering;
  }
  router.push({ query });
};

const loadMore = async () => {
  if (!productsStore.hasNextPage || loadingMore.value) return;

  loadingMore.value = true;
  try {
    await productsStore.loadMore();
  } finally {
    loadingMore.value = false;
  }
};

// SEO
useHead({
  title: "Products - AgriShop",
  meta: [
    {
      name: "description",
      content:
        "Browse our wide selection of agricultural products and farming supplies.",
    },
  ],
});
</script>
