<template>
  <div class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Breadcrumb -->
      <nav class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
        <NuxtLink to="/" class="hover:text-orange-600 transition-colors"
          >Home</NuxtLink
        >
        <span>/</span>
        <span class="text-gray-900 font-medium">Products</span>
      </nav>

      <!-- Page Header with Stats -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div
          class="flex flex-col lg:flex-row lg:items-center lg:justify-between"
        >
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Products</h1>
            <p class="text-gray-600">
              Discover our wide range of agricultural products and supplies
            </p>
          </div>
          <div class="mt-4 lg:mt-0">
            <div class="flex items-center space-x-6 text-sm">
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">
                  {{ pagination.count }}
                </div>
                <div class="text-gray-500">Total Products</div>
              </div>
              <div class="text-center" v-if="shopStats">
                <div class="text-2xl font-bold text-orange-600">
                  {{ shopStats.products_on_sale }}
                </div>
                <div class="text-gray-500">On Sale</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar Filters -->
        <aside class="lg:w-80 xl:w-96">
          <div class="bg-white rounded-lg shadow-sm p-6 sticky top-4">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-lg font-semibold text-gray-900">Filters</h2>
              <button
                @click="clearAllFilters"
                class="text-sm text-gray-500 hover:text-red-600 transition-colors"
              >
                Clear All
              </button>
            </div>

            <!-- Search -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2"
                >Search</label
              >
              <div class="relative">
                <input
                  v-model="searchQuery"
                  @input="debouncedSearch"
                  type="text"
                  placeholder="Search products..."
                  class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <div
                  class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                >
                  <svg
                    class="h-5 w-5 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    ></path>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Categories -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3">Categories</h3>
              <div class="space-y-2">
                <label class="flex items-center">
                  <input
                    type="radio"
                    name="category"
                    :value="null"
                    v-model="selectedCategoryId"
                    @change="handleCategoryChange"
                    class="text-green-600 focus:ring-green-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">All Categories</span>
                </label>
                <label
                  v-for="category in activeCategories"
                  :key="category.id"
                  class="flex items-center justify-between"
                >
                  <div class="flex items-center">
                    <input
                      type="radio"
                      name="category"
                      :value="category.id"
                      v-model="selectedCategoryId"
                      @change="handleCategoryChange"
                      class="text-green-600 focus:ring-green-500"
                    />
                    <span class="ml-2 text-sm text-gray-700">
                      {{
                        category.name?.origin ||
                        category.name ||
                        category.description ||
                        "Danh mục"
                      }}
                    </span>
                  </div>
                  <span
                    class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full"
                  >
                    {{ category.active_product_count }}
                  </span>
                </label>
              </div>
            </div>

            <!-- Price Range -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3">
                Price Range
              </h3>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs text-gray-500 mb-1"
                    >Min Price</label
                  >
                  <input
                    v-model.number="priceFilters.min"
                    @change="handlePriceChange"
                    type="number"
                    :min="priceRange.min"
                    :max="priceRange.max"
                    :placeholder="priceRange.min.toString()"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1"
                    >Max Price</label
                  >
                  <input
                    v-model.number="priceFilters.max"
                    @change="handlePriceChange"
                    type="number"
                    :min="priceRange.min"
                    :max="priceRange.max"
                    :placeholder="priceRange.max.toString()"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
              </div>
              <div class="mt-2 text-xs text-gray-500">
                Range: ${{ priceRange.min }} - ${{ priceRange.max }}
              </div>
            </div>

            <!-- Stock Status -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3">
                Availability
              </h3>
              <div class="space-y-2">
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    v-model="stockFilters.inStock"
                    @change="handleStockChange"
                    class="text-green-600 focus:ring-green-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">In Stock</span>
                </label>
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    v-model="stockFilters.onSale"
                    @change="handlePromotionChange"
                    class="text-green-600 focus:ring-green-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">On Sale</span>
                </label>
              </div>
            </div>

            <!-- Sorting -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-900 mb-3">Sort By</h3>
              <select
                v-model="sortOption"
                @change="handleSortChange"
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="price-asc">Price (Low to High)</option>
                <option value="price-desc">Price (High to Low)</option>
                <option value="created_at-desc">Newest First</option>
                <option value="created_at-asc">Oldest First</option>
              </select>
            </div>
          </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1">
          <!-- Mobile Filter Button -->
          <div class="lg:hidden mb-4">
            <button
              @click="showMobileFilters = !showMobileFilters"
              class="flex items-center space-x-2 bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200"
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
                  d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                ></path>
              </svg>
              <span>Filters</span>
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="flex justify-center items-center py-12">
            <div
              class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"
            ></div>
          </div>

          <!-- Error State -->
          <div
            v-else-if="error"
            class="bg-red-50 border border-red-200 rounded-lg p-6 text-center"
          >
            <div class="text-red-600 mb-2">
              <svg
                class="w-12 h-12 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              <h3 class="text-lg font-semibold">Error Loading Products</h3>
              <p class="text-sm mt-1">{{ error }}</p>
            </div>
            <button
              @click="refetchProducts"
              class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>

          <!-- Products Grid -->
          <div v-else>
            <!-- Results Header -->
            <div class="flex items-center justify-between mb-6">
              <div class="text-sm text-gray-600">
                Showing {{ products.length }} of {{ pagination.count }} products
              </div>
              <div class="flex items-center space-x-4">
                <!-- View Toggle -->
                <div class="flex bg-gray-100 rounded-md p-1">
                  <button
                    @click="viewMode = 'grid'"
                    :class="[
                      'px-3 py-1 rounded text-sm transition-colors',
                      viewMode === 'grid'
                        ? 'bg-white shadow-sm text-gray-900'
                        : 'text-gray-600 hover:text-gray-900',
                    ]"
                  >
                    Grid
                  </button>
                  <button
                    @click="viewMode = 'list'"
                    :class="[
                      'px-3 py-1 rounded text-sm transition-colors',
                      viewMode === 'list'
                        ? 'bg-white shadow-sm text-gray-900'
                        : 'text-gray-600 hover:text-gray-900',
                    ]"
                  >
                    List
                  </button>
                </div>
              </div>
            </div>

            <!-- No Results -->
            <div v-if="products.length === 0" class="text-center py-12">
              <div class="text-gray-400 mb-4">
                <svg
                  class="w-16 h-16 mx-auto"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h2m0 0V6a2 2 0 012-2h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 01.293.707V9"
                  ></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                No products found
              </h3>
              <p class="text-gray-600 mb-4">
                Try adjusting your filters or search terms
              </p>
              <button
                @click="clearAllFilters"
                class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 transition-colors"
              >
                Clear Filters
              </button>
            </div>

            <!-- Products Grid -->
            <div v-else>
              <div
                :class="[
                  viewMode === 'grid'
                    ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
                    : 'space-y-4',
                ]"
              >
                <ProductCard
                  v-for="product in products"
                  :key="product.id"
                  :product="product"
                  :view-mode="viewMode"
                  class="transition-transform hover:scale-105"
                />
              </div>

              <!-- Pagination -->
              <div v-if="totalPages > 1" class="mt-12 flex justify-center">
                <nav class="flex items-center space-x-2">
                  <button
                    @click="goToPage(pagination.currentPage - 1)"
                    :disabled="!hasPreviousPage"
                    class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>

                  <template v-for="page in visiblePages" :key="page">
                    <button
                      v-if="page !== '...'"
                      @click="goToPage(page as number)"
                      :class="[
                        'px-3 py-2 text-sm font-medium rounded-md',
                        page === pagination.currentPage
                          ? 'text-white bg-green-600 border border-green-600'
                          : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50',
                      ]"
                    >
                      {{ page }}
                    </button>
                    <span
                      v-else
                      class="px-3 py-2 text-sm font-medium text-gray-500"
                      >...</span
                    >
                  </template>

                  <button
                    @click="goToPage(pagination.currentPage + 1)"
                    :disabled="!hasNextPage"
                    class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ProductCard from "~/components/ProductCard.vue";
import { useProducts } from "~/composables/useProducts";

// Simple debounce function
const debounce = (fn: Function, delay: number) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(null, args), delay);
  };
};

// SEO
// useHead({
//   title: "Products - AgriShop",
//   meta: [
//     {
//       name: "description",
//       content:
//         "Browse our wide selection of agricultural products and supplies.",
//     },
//   ],
// });

// Composables
const route = useRoute();
const router = useRouter();
const {
  products,
  activeCategories,
  shopStats,
  loading,
  error,
  pagination,
  priceRange,
  totalPages,
  hasNextPage,
  hasPreviousPage,
  fetchProducts,
  fetchProductsWithFilters,
  searchProducts,
  fetchProductsByCategory,
  fetchCategoriesWithProducts,
  fetchShopStats,
  goToPage,
  clearFilters,
} = useProducts();

// Local state
const showMobileFilters = ref(false);
const viewMode = ref<"grid" | "list">("grid");
const searchQuery = ref("");
const selectedCategoryId = ref<number | null>(null);
const sortOption = ref("name-asc");

const priceFilters = ref({
  min: null as number | null,
  max: null as number | null,
});

const stockFilters = ref({
  inStock: false,
  onSale: false,
});

// Computed
const visiblePages = computed(() => {
  const current = pagination.value.currentPage;
  const total = totalPages.value;
  const pages = [];

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push("...");
      pages.push(total);
    } else if (current >= total - 3) {
      pages.push(1);
      pages.push("...");
      for (let i = total - 4; i <= total; i++) pages.push(i);
    } else {
      pages.push(1);
      pages.push("...");
      for (let i = current - 1; i <= current + 1; i++) pages.push(i);
      pages.push("...");
      pages.push(total);
    }
  }

  return pages;
});

// Methods
const debouncedSearch = debounce(() => {
  if (searchQuery.value.trim()) {
    searchProducts(searchQuery.value.trim());
  } else {
    fetchProducts();
  }
}, 500);

const handleCategoryChange = () => {
  if (selectedCategoryId.value) {
    fetchProductsByCategory(selectedCategoryId.value);
  } else {
    fetchProducts();
  }
  updateURL();
};

const handlePriceChange = () => {
  const filters: any = {};
  if (priceFilters.value.min) filters.min_price = priceFilters.value.min;
  if (priceFilters.value.max) filters.max_price = priceFilters.value.max;
  fetchProductsWithFilters(filters);
  updateURL();
};

const handleStockChange = () => {
  const filters: any = {};
  if (stockFilters.value.inStock) filters.in_stock = true;
  fetchProductsWithFilters(filters);
  updateURL();
};

const handlePromotionChange = () => {
  const filters: any = {};
  if (stockFilters.value.onSale) filters.has_promotion = true;
  fetchProductsWithFilters(filters);
  updateURL();
};

const handleSortChange = () => {
  const [sortBy, sortOrder] = sortOption.value.split("-");
  const filters = {
    sort_by: sortBy as any,
    sort_order: sortOrder as any,
  };
  fetchProductsWithFilters(filters);
  updateURL();
};

const clearAllFilters = () => {
  searchQuery.value = "";
  selectedCategoryId.value = null;
  priceFilters.value = { min: null, max: null };
  stockFilters.value = { inStock: false, onSale: false };
  sortOption.value = "name-asc";
  clearFilters();
  updateURL();
};

const refetchProducts = () => {
  fetchProducts();
};

const updateURL = () => {
  const query: any = {};

  if (searchQuery.value) query.search = searchQuery.value;
  if (selectedCategoryId.value) query.category = selectedCategoryId.value;
  if (priceFilters.value.min) query.min_price = priceFilters.value.min;
  if (priceFilters.value.max) query.max_price = priceFilters.value.max;
  if (stockFilters.value.inStock) query.in_stock = "true";
  if (stockFilters.value.onSale) query.on_sale = "true";
  if (sortOption.value !== "name-asc") query.sort = sortOption.value;

  router.push({ query });
};

const initializeFromURL = () => {
  const query = route.query;

  if (query.search) searchQuery.value = query.search as string;
  if (query.category) selectedCategoryId.value = Number(query.category);
  if (query.min_price) priceFilters.value.min = Number(query.min_price);
  if (query.max_price) priceFilters.value.max = Number(query.max_price);
  if (query.in_stock === "true") stockFilters.value.inStock = true;
  if (query.on_sale === "true") stockFilters.value.onSale = true;
  if (query.sort) sortOption.value = query.sort as string;
};

// Lifecycle
onMounted(async () => {
  // Initialize data
  await Promise.all([fetchCategoriesWithProducts(), fetchShopStats()]);

  // Initialize from URL parameters
  initializeFromURL();

  // Load products based on URL parameters
  if (searchQuery.value) {
    searchProducts(searchQuery.value);
  } else if (selectedCategoryId.value) {
    fetchProductsByCategory(selectedCategoryId.value);
  } else {
    fetchProducts();
  }
});

// Watch for route changes
watch(
  () => route.query,
  () => {
    initializeFromURL();
  },
  { deep: true }
);
</script>
