<template>
  <div>
    <!-- Hero Section with Shop Stats -->
    <section class="bg-gradient-to-r from-green-600 to-orange-500 text-white">
      <div class="container mx-auto px-4 py-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 class="text-4xl md:text-6xl font-bold mb-6">
              Quality Agricultural Products
            </h1>
            <p class="text-xl mb-8 opacity-90">
              Discover premium farming supplies, seeds, tools, and equipment for
              modern agriculture.
            </p>

            <!-- Shop Statistics -->
            <div
              v-if="shopStats"
              class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
            >
              <div
                class="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center"
              >
                <div class="text-2xl font-bold">
                  {{ shopStats.total_products }}
                </div>
                <div class="text-sm opacity-80">Products</div>
              </div>
              <div
                class="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center"
              >
                <div class="text-2xl font-bold">
                  {{ shopStats.total_categories }}
                </div>
                <div class="text-sm opacity-80">Categories</div>
              </div>
              <div
                class="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center"
              >
                <div class="text-2xl font-bold">
                  {{ shopStats.products_on_sale }}
                </div>
                <div class="text-sm opacity-80">On Sale</div>
              </div>
              <div
                class="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center"
                v-if="shopStats?.price_range"
              >
                <div class="text-2xl font-bold">
                  ${{ shopStats.price_range.min }}-${{
                    shopStats.price_range.max
                  }}
                </div>
                <div class="text-sm opacity-80">Price Range</div>
              </div>
            </div>

            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink
                to="/products"
                class="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors text-center"
              >
                Shop Now
              </NuxtLink>
              <NuxtLink
                to="/products?on_sale=true"
                class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-colors text-center"
              >
                View Sale Items
              </NuxtLink>
            </div>
          </div>
          <div class="hidden lg:block">
            <div
              class="w-full h-80 bg-gradient-to-br from-green-400 to-orange-400 rounded-lg shadow-xl flex items-center justify-center text-white"
            >
              <div class="text-center">
                <div class="text-6xl mb-4">🌾</div>
                <div class="text-xl font-semibold">Premium Agriculture</div>
                <div class="text-sm opacity-80">
                  Quality Products & Equipment
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Why Choose AgriShop?
          </h2>
          <p class="text-gray-600 max-w-2xl mx-auto">
            We provide everything you need for successful farming with quality
            products and expert support.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div
              class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-8 h-8 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Quality Guaranteed</h3>
            <p class="text-gray-600">
              Premium products tested and verified for optimal performance in
              agricultural applications.
            </p>
          </div>

          <div class="text-center">
            <div
              class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-8 h-8 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                ></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Fast Delivery</h3>
            <p class="text-gray-600">
              Quick and reliable shipping to get your agricultural supplies when
              you need them most.
            </p>
          </div>

          <div class="text-center">
            <div
              class="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-8 h-8 text-orange-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Expert Support</h3>
            <p class="text-gray-600">
              Professional guidance from agricultural experts to help you make
              the right choices.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories Section -->
    <section class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Shop by Category
          </h2>
          <p class="text-gray-600">
            Find exactly what you need for your farming operation
          </p>
        </div>

        <!-- Categories Grid - Always show 8 items -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Real categories -->
          <NuxtLink
            v-for="category in displayedCategories.slice(0, 8)"
            :key="`real-${category.id}`"
            :to="`/products?category=${category.id}`"
            class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 text-center group"
          >
            <div
              class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-200 transition-colors"
            >
              <svg
                class="w-8 h-8 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                ></path>
              </svg>
            </div>
            <h3
              class="font-semibold text-gray-900 group-hover:text-green-600 transition-colors"
            >
              {{ category.name?.origin || category.description || "Danh mục" }}
            </h3>
          </NuxtLink>

          <!-- Static placeholder categories to fill remaining slots -->
          <div
            v-for="(categoryName, index) in placeholderCategories.slice(
              0,
              Math.max(0, 8 - displayedCategories.length)
            )"
            :key="`placeholder-${index}`"
            class="bg-white rounded-lg shadow-md p-6 text-center opacity-50"
          >
            <div
              class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-8 h-8 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                ></path>
              </svg>
            </div>
            <div class="flex flex-col items-center">
              <div
                class="w-8 h-8 rounded border-2 border-dashed border-gray-300 flex items-center justify-center mb-2"
              >
                <svg
                  class="w-4 h-4 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v16m8-8H4"
                  ></path>
                </svg>
              </div>
              <span class="text-xs text-gray-300">Chưa có dữ liệu</span>
            </div>
          </div>
        </div>

        <div class="text-center mt-8">
          <NuxtLink
            to="/products"
            class="inline-flex items-center text-green-600 hover:text-green-700 font-semibold"
          >
            View All Categories
            <svg
              class="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 8l4 4m0 0l-4 4m4-4H3"
              ></path>
            </svg>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Featured Products Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Featured Products
          </h2>
          <p class="text-gray-600">
            Popular items trusted by farmers worldwide
          </p>
        </div>

        <!-- Products Grid - Always show 8 items -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Real products -->
          <ProductCard
            v-for="product in displayedProducts.slice(0, 8)"
            :key="`real-${product.id}`"
            :product="product"
          />

          <!-- Static placeholder products to fill remaining slots -->
          <div
            v-for="(productName, index) in [
              'Premium Seeds',
              'Organic Fertilizer',
              'Irrigation System',
              'Garden Tools',
              'Plant Protection',
              'Soil Treatment',
              'Harvesting Kit',
              'Storage Solution',
            ].slice(0, Math.max(0, 8 - displayedProducts.length))"
            :key="`placeholder-${index}`"
            class="bg-white rounded-lg shadow-sm overflow-hidden opacity-50"
          >
            <!-- Product Image Placeholder -->
            <div
              class="aspect-square bg-gray-100 flex items-center justify-center"
            >
              <div
                class="w-16 h-16 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center"
              >
                <svg
                  class="w-8 h-8 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  ></path>
                </svg>
              </div>
            </div>

            <!-- Product Info -->
            <div class="p-4">
              <div class="flex flex-col items-center text-center">
                <div
                  class="w-8 h-8 rounded border-2 border-dashed border-gray-300 flex items-center justify-center mb-2"
                >
                  <svg
                    class="w-4 h-4 text-gray-300"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                    ></path>
                  </svg>
                </div>
                <span class="text-xs text-gray-300 mb-2">Chưa có sản phẩm</span>
                <div class="w-full h-8 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center mt-12">
          <NuxtLink
            to="/products"
            class="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            View All Products
          </NuxtLink>
        </div>
      </div>
    </section>
    <!-- Newsletter Section -->
    <section class="py-16 bg-green-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-4">Stay Updated</h2>
        <p class="text-xl mb-8 opacity-90">
          Get the latest news about agricultural products and farming tips
        </p>
        <div class="max-w-md mx-auto flex gap-2">
          <input
            v-model="newsletterForm.email"
            type="email"
            placeholder="Enter your email"
            class="flex-1 px-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-white"
            :disabled="newsletterForm.loading"
          />
          <button
            @click="subscribeNewsletter"
            :disabled="newsletterForm.loading || !newsletterForm.email"
            class="bg-orange-500 hover:bg-orange-600 px-6 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="newsletterForm.loading">...</span>
            <span v-else>Subscribe</span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, computed } from "vue";
import ProductCard from "~/components/ProductCard.vue";
import { useProducts } from "~/composables/useProducts";
import { useHead } from "nuxt/app";

// SEO Meta
useHead({
  title: "AgriShop - Quality Agricultural Products",
  meta: [
    {
      name: "description",
      content:
        "Discover premium farming supplies, seeds, tools, and equipment for modern agriculture at AgriShop.",
    },
  ],
});

// Use products composable
const {
  featuredProducts,
  categoriesWithProducts,
  newArrivals,
  onSaleProducts,
  shopStats,
  loading,
  initializeShop,
} = useProducts();

// Static placeholder data
const placeholderCategories = [
  "Seeds & Plants",
  "Fertilizers",
  "Tools & Equipment",
  "Pest Control",
  "Irrigation",
  "Livestock Feed",
  "Harvesting",
  "Storage",
];

const placeholderProducts = Array(8).fill(null);

// Computed
const displayedProducts = computed(() => featuredProducts.value.slice(0, 8));
const displayedCategories = computed(() =>
  categoriesWithProducts.value.slice(0, 8)
);

// Newsletter form
const newsletterForm = reactive({
  email: "",
  loading: false,
});

// Methods
const subscribeNewsletter = async () => {
  if (!newsletterForm.email.trim()) return;

  newsletterForm.loading = true;
  try {
    // TODO: Implement newsletter API
    console.log("Subscribing:", newsletterForm.email);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate API call

    newsletterForm.email = "";
    // TODO: Show success notification
  } catch (error) {
    console.error("Newsletter subscription failed:", error);
    // TODO: Show error notification
  } finally {
    newsletterForm.loading = false;
  }
};

// Initialize shop data on mount
onMounted(async () => {
  await initializeShop();
});
</script>
