<template>
  <div>
    <!-- Hero Section -->
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
            <div class="flex flex-col sm:flex-row gap-4">
              <NuxtLink
                to="/products"
                class="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors text-center"
              >
                Shop Now
              </NuxtLink>
              <NuxtLink
                to="/categories"
                class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-colors text-center"
              >
                Browse Categories
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

        <div
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
          v-if="displayedCategories?.length > 0"
        >
          <NuxtLink
            v-for="category in displayedCategories"
            :key="category.id"
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
              {{ category.name.origin }}
            </h3>
          </NuxtLink>
        </div>

        <div class="text-center mt-8">
          <NuxtLink
            to="/categories"
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

        <div
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
          v-if="displayedProducts?.length > 0"
        >
          <ProductCard
            v-for="product in displayedProducts"
            :key="product.id"
            :product="product"
          />
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
import { ref, computed, reactive, onMounted } from "vue";
import { useProductsService } from "~/services/products";
import type { Product, ProductCategory } from "~/services/products";

import ProductCard from "@/components/ProductCard.vue";

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

// Services
const { getCategories, getProductsSummary } = useProductsService();

// Reactive state
const featuredProducts = ref<Product[]>([]);
const categories = ref<ProductCategory[]>([]);
const loading = ref(true);

// Computed
const displayedProducts = computed(() =>
  featuredProducts.value.filter(p => !!p).slice(0, 8)
);
const displayedCategories = computed(() => categories.value.slice(0, 8));

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

// Lifecycle
onMounted(async () => {
  loading.value = true;

  try {
    // Load featured products and categories in parallel
    const [productsResult, categoriesResult] = await Promise.allSettled([
      getProductsSummary(),
      getCategories(),
    ]);

    if (
      productsResult.status === "fulfilled" &&
      productsResult.value.data.value
    ) {
      const summary = productsResult.value.data.value as any[];
      featuredProducts.value = summary.map((p) => ({
        ...p,
        image: p.image || p.thumbnail,
      })) as Product[];
      // console.log("Featured Product", featuredProducts.value);
    }

    if (
      categoriesResult.status === "fulfilled" &&
      categoriesResult.value.data.value
    ) {
      categories.value = categoriesResult.value.data.value as ProductCategory[];
    }
  } catch (error) {
    console.error("Failed to load data:", error);
  } finally {
    loading.value = false;
  }
});
</script>
