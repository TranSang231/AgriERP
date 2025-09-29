<template>
  <div
    v-if="isValidProduct"
    :class="[
      'bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden group',
      viewMode === 'list' ? 'flex items-center p-4' : 'flex flex-col',
    ]"
  >
    <!-- Product Image -->
    <div
      :class="[
        'relative overflow-hidden bg-gray-100',
        viewMode === 'list'
          ? 'w-24 h-24 flex-shrink-0 rounded-md mr-4'
          : 'aspect-square',
      ]"
    >
      <NuxtLink :to="`/products/${product?.id}`" class="block">
        <img
          :src="productImage"
          :alt="productName"
          :class="[
            'w-full h-full object-cover group-hover:scale-105 transition-transform duration-300',
            !productImage && 'opacity-50',
          ]"
          loading="lazy"
          @error="handleImageError"
        />
      </NuxtLink>

      <!-- Promotion Badge -->
      <div
        v-if="product?.has_promotion && product?.discount_percentage"
        class="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 text-xs font-bold rounded-md shadow-sm"
      >
        -{{ Math.round(product?.discount_percentage || 0) }}%
      </div>

      <!-- Stock Badge -->
      <div
        v-if="(product?.in_stock || 0) <= 0"
        class="absolute top-2 right-2 bg-gray-800 text-white px-2 py-1 text-xs font-medium rounded-md"
      >
        Out of Stock
      </div>
      <div
        v-else-if="(product?.in_stock || 0) <= 5"
        class="absolute top-2 right-2 bg-orange-500 text-white px-2 py-1 text-xs font-medium rounded-md"
      >
        Low Stock
      </div>

      <!-- Quick Actions (Grid Mode Only) -->
      <div
        v-if="viewMode === 'grid'"
        class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col space-y-2"
      >
        <button
          @click="addToCart"
          :disabled="(product?.in_stock || 0) <= 0"
          class="bg-white text-gray-700 hover:bg-green-600 hover:text-white p-2 rounded-full shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          :title="
            (product?.in_stock || 0) <= 0 ? 'Out of stock' : 'Add to cart'
          "
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
          :class="[
            'bg-white p-2 rounded-full shadow-md transition-all duration-200',
            isInWishlist
              ? 'text-red-500 hover:bg-red-50'
              : 'text-gray-700 hover:bg-red-500 hover:text-white',
          ]"
          title="Add to wishlist"
        >
          <svg
            class="w-4 h-4"
            :fill="isInWishlist ? 'currentColor' : 'none'"
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
    </div>

    <!-- Product Info -->
    <div :class="[viewMode === 'list' ? 'flex-1' : 'p-4']">
      <div
        :class="[
          viewMode === 'list' ? 'flex items-center justify-between' : '',
        ]"
      >
        <div :class="[viewMode === 'list' ? 'flex-1' : '']">
          <!-- Categories -->
          <div
            v-if="product?.categories && product.categories.length > 0"
            class="mb-2"
          >
            <div class="flex flex-wrap gap-1">
              <span
                v-for="category in product.categories.slice(0, 2)"
                :key="category.id"
                class="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full"
              >
                {{
                  category.name?.origin ||
                  category.name ||
                  category.description ||
                  "Danh mục"
                }}
              </span>
              <span
                v-if="product?.categories && product.categories.length > 2"
                class="text-xs text-gray-500 bg-gray-50 px-2 py-1 rounded-full"
              >
                +{{ product.categories.length - 2 }}
              </span>
            </div>
          </div>

          <!-- Product Name -->
          <h3
            :class="[
              'font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition-colors',
              viewMode === 'list' ? 'text-lg' : 'text-base',
            ]"
          >
            <NuxtLink :to="`/products/${product?.id}`" class="hover:underline">
              {{ productName }}
            </NuxtLink>
          </h3>

          <!-- Product Description (List Mode Only) -->
          <p
            v-if="viewMode === 'list' && product?.description"
            class="text-sm text-gray-600 mb-2 line-clamp-2"
          >
            {{ product?.description }}
          </p>

          <!-- Price and Stock Info -->
          <div
            :class="[
              viewMode === 'list' ? 'flex items-center space-x-4' : 'mb-3',
            ]"
          >
            <!-- Price -->
            <div class="flex items-center space-x-2">
              <span
                v-if="product?.has_promotion && product?.sale_price"
                class="text-lg font-bold text-green-600"
              >
                ${{ formatPrice(product?.sale_price || 0) }}
              </span>
              <span
                :class="[
                  'font-semibold',
                  product?.has_promotion && product?.sale_price
                    ? 'text-sm text-gray-500 line-through'
                    : 'text-lg text-gray-900',
                ]"
              >
                ${{ formatPrice(product?.price || 0) }}
              </span>
            </div>

            <!-- Stock Info -->
            <div v-if="viewMode === 'list'" class="text-sm">
              <span
                :class="[
                  'font-medium',
                  product.in_stock <= 0
                    ? 'text-red-600'
                    : product.in_stock <= 5
                    ? 'text-orange-600'
                    : 'text-green-600',
                ]"
              >
                {{ stockStatus }}
              </span>
            </div>
          </div>

          <!-- Product Meta (Grid Mode) -->
          <div
            v-if="viewMode === 'grid'"
            class="text-xs text-gray-500 space-y-1"
          >
            <div v-if="product.weight">Weight: {{ product.weight }}kg</div>
            <div class="flex items-center justify-between">
              <span
                :class="[
                  'font-medium',
                  product.in_stock <= 0
                    ? 'text-red-600'
                    : product.in_stock <= 5
                    ? 'text-orange-600'
                    : 'text-green-600',
                ]"
              >
                {{ stockStatus }}
              </span>
              <span v-if="product.created_at" class="text-gray-400">
                {{ formatDate(product.created_at) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Actions (List Mode) -->
        <div
          v-if="viewMode === 'list'"
          class="flex items-center space-x-3 ml-4"
        >
          <button
            @click="toggleWishlist"
            :class="[
              'p-2 rounded-full transition-all duration-200',
              isInWishlist
                ? 'text-red-500 bg-red-50 hover:bg-red-100'
                : 'text-gray-400 hover:text-red-500 hover:bg-red-50',
            ]"
            title="Add to wishlist"
          >
            <svg
              class="w-5 h-5"
              :fill="isInWishlist ? 'currentColor' : 'none'"
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

          <button
            @click="addToCart"
            :disabled="product.in_stock <= 0"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md transition-colors duration-200 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-green-600"
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
            <span>{{
              (product?.in_stock || 0) <= 0 ? "Out of Stock" : "Add to Cart"
            }}</span>
          </button>
        </div>
      </div>

      <!-- Add to Cart Button (Grid Mode) -->
      <button
        v-if="viewMode === 'grid'"
        @click="addToCart"
        :disabled="(product?.in_stock || 0) <= 0"
        class="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md transition-colors duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-green-600"
      >
        {{ (product?.in_stock || 0) <= 0 ? "Out of Stock" : "Add to Cart" }}
      </button>
    </div>
  </div>

  <!-- Fallback for invalid products -->
  <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden opacity-75">
    <!-- Product Image Placeholder -->
    <div class="aspect-square bg-gray-100 flex items-center justify-center">
      <svg
        class="w-12 h-12 text-gray-400"
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

    <!-- Product Info -->
    <div class="p-4">
      <h3 class="font-semibold text-gray-500 mb-2">Loading Product...</h3>
      <div class="flex items-center justify-between">
        <span class="text-lg font-bold text-gray-400">---</span>
        <button
          disabled
          class="bg-gray-300 text-gray-500 px-4 py-2 rounded-md text-sm cursor-not-allowed"
        >
          Loading...
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Product } from "~/services/products";

// Props
interface Props {
  product: Product;
  viewMode?: "grid" | "list";
}

const props = withDefaults(defineProps<Props>(), {
  viewMode: "grid",
});

// Local state
const imageError = ref(false);
const isInWishlist = ref(false); // TODO: Integrate with wishlist store

// Computed
const productName = computed(() => {
  if (typeof props.product === "string" || !props.product) {
    // Silent fallback for invalid product data
    return "Loading Product...";
  }
  return props.product?.name || "Unnamed Product";
});

const isValidProduct = computed(() => {
  return props.product && typeof props.product === "object" && props.product.id;
});

const productImage = computed(() => {
  if (imageError.value) return "/images/placeholder-product.jpg";

  if (typeof props.product === "string" || !props.product) {
    return "/images/placeholder-product.jpg";
  }

  if (props.product?.images && props.product.images.length > 0) {
    return props.product.images[0].image;
  }

  return "/images/placeholder-product.jpg";
});

const stockStatus = computed(() => {
  if (props.product.in_stock <= 0) return "Out of Stock";
  if (props.product.in_stock <= 5)
    return `Low Stock (${props.product.in_stock})`;
  return `In Stock (${props.product.in_stock})`;
});

// Methods
const formatPrice = (price: number | string) => {
  const numPrice = typeof price === "string" ? parseFloat(price) : price;
  return numPrice.toFixed(2);
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

const handleImageError = () => {
  imageError.value = true;
};

const addToCart = async () => {
  if (props.product.in_stock <= 0) return;

  try {
    // TODO: Integrate with cart store
    console.log("Adding to cart:", props.product.id);

    // Show success notification
    // TODO: Add toast notification
  } catch (error) {
    console.error("Failed to add to cart:", error);
    // TODO: Show error notification
  }
};

const toggleWishlist = async () => {
  try {
    isInWishlist.value = !isInWishlist.value;
    // TODO: Integrate with wishlist store/API
    console.log("Toggle wishlist:", props.product.id, isInWishlist.value);
  } catch (error) {
    console.error("Failed to toggle wishlist:", error);
    isInWishlist.value = !isInWishlist.value; // Revert on error
  }
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
</style>
