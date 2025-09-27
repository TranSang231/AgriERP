<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCurrency } from '~/composables/useCurrency'
import { useCartStore } from '~/stores/cart'
import { useApi } from '~/services/api'

const cart = useCartStore()
const { format } = useCurrency()
const route = useRoute()
const { request } = useApi()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const quantity = ref(1)

onMounted(async () => {
  const productId = route.params.id as string
  
  try {
    loading.value = true
    const { data, error: productError } = await request(`/products/${productId}`)
    
    if (productError?.value) {
      throw productError.value
    }
    
    if (data?.value) {
      product.value = data.value
    } else {
      throw new Error('Không tìm thấy sản phẩm')
    }
  } catch (e: any) {
    console.error('Lỗi khi tải sản phẩm:', e)
    error.value = e?.message || 'Không thể tải thông tin sản phẩm'
  } finally {
    loading.value = false
  }
})

const productName = computed(() => {
  if (!product.value?.name) return 'Không có tên'
  return typeof product.value.name === 'string' 
    ? product.value.name 
    : product.value.name.origin || 'Không có tên'
})

const productDescription = computed(() => {
  if (!product.value?.description) return null
  return typeof product.value.description === 'string' 
    ? product.value.description 
    : product.value.description.origin || null
})

const productUnit = computed(() => {
  if (!product.value?.unit) return 'Cái'
  return typeof product.value.unit === 'string' 
    ? product.value.unit 
    : product.value.unit.origin || 'Cái'
})

const productImages = computed(() => {
  if (!product.value?.images || !Array.isArray(product.value.images)) {
    return product.value?.thumbnail ? [product.value.thumbnail] : ['/placeholder-product.jpg']
  }
  return product.value.images.map(img => img.image || img.thumbnail).filter(Boolean)
})

const productCategories = computed(() => {
  if (!product.value?.categories || !Array.isArray(product.value.categories)) {
    return []
  }
  return product.value.categories.map(cat => 
    typeof cat === 'string' ? cat : cat.name?.origin || cat.name || 'Không xác định'
  )
})

const isInStock = computed(() => {
  return (product.value?.in_stock || 0) > 0
})

const stockStatus = computed(() => {
  const stock = product.value?.in_stock || 0
  if (stock === 0) return { text: 'Hết hàng', color: 'text-red-600' }
  if (stock < 10) return { text: `Còn ${stock} ${productUnit.value}`, color: 'text-orange-600' }
  return { text: `Còn ${stock} ${productUnit.value}`, color: 'text-green-600' }
})

function addToCart() {
  if (!product.value || !isInStock.value) return
  
  cart.add({
    productId: product.value.id,
    name: productName.value,
    price: product.value.price || 0,
    qty: quantity.value,
    image: productImages.value[0]
  })
  
  alert(`Đã thêm ${quantity.value} ${productUnit.value} vào giỏ hàng!`)
}

const increaseQuantity = () => {
  const maxStock = product.value?.in_stock || 0
  if (quantity.value < maxStock) {
    quantity.value++
  }
}

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">Đang tải thông tin sản phẩm...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Có lỗi xảy ra</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <button @click="$router.back()" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        Quay lại
      </button>
    </div>

    <!-- Product Details -->
    <div v-else-if="product" class="max-w-6xl mx-auto">
      <!-- Breadcrumb -->
      <nav class="mb-6">
        <div class="flex items-center space-x-2 text-sm text-gray-500">
          <NuxtLink to="/" class="hover:text-orange-600">Trang chủ</NuxtLink>
          <span>›</span>
          <span>{{ productName }}</span>
        </div>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Product Images -->
        <div class="space-y-4">
          <!-- Main Image -->
          <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            <img 
              :src="productImages[0]" 
              :alt="productName"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

        <!-- Product Info -->
        <div class="space-y-6">
          <!-- Product Name & Status -->
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ productName }}</h1>
            <div class="flex items-center space-x-4">
              <span :class="['text-sm font-medium', stockStatus.color]">
                {{ stockStatus.text }}
              </span>
              <span class="text-sm text-gray-500">Đơn vị: {{ productUnit }}</span>
            </div>
          </div>

          <!-- Price -->
          <div class="flex items-center space-x-4">
            <span class="text-3xl font-bold text-orange-600">
              {{ format(product.price || 0) }}
            </span>
            <span class="text-sm text-gray-500">/ {{ productUnit }}</span>
          </div>

          <!-- Categories -->
          <div v-if="productCategories.length > 0">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Danh mục:</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="category in productCategories" 
                :key="category"
                class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
              >
                {{ category }}
              </span>
            </div>
          </div>

          <!-- Quantity Selector -->
          <div v-if="isInStock">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Số lượng:</h3>
            <div class="flex items-center space-x-3">
              <button 
                @click="decreaseQuantity"
                :disabled="quantity <= 1"
                class="w-10 h-10 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
              >
                -
              </button>
              <span class="text-lg font-medium w-12 text-center">{{ quantity }}</span>
              <button 
                @click="increaseQuantity"
                :disabled="quantity >= (product.in_stock || 0)"
                class="w-10 h-10 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
              >
                +
              </button>
            </div>
          </div>

          <!-- Add to Cart Button -->
          <div class="space-y-3">
            <button 
              @click="addToCart"
              :disabled="!isInStock"
              :class="[
                'w-full py-3 px-6 rounded-lg font-semibold text-lg transition-colors',
                isInStock 
                  ? 'bg-orange-500 hover:bg-orange-600 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
            >
              {{ isInStock ? 'Thêm vào giỏ hàng' : 'Hết hàng' }}
            </button>
          </div>

          <!-- Product Description -->
          <div v-if="productDescription">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Mô tả sản phẩm</h3>
            <div class="prose max-w-none">
              <p class="text-gray-700 leading-relaxed">{{ productDescription }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Product Specifications -->
      <div class="mt-16">
        <h2 class="text-2xl font-bold text-gray-900 mb-8">Thông số kỹ thuật</h2>
        <div class="bg-white rounded-lg border p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Giá bán</h3>
              <p class="text-lg font-semibold text-gray-900">{{ format(product.price || 0) }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Đơn vị</h3>
              <p class="text-lg font-semibold text-gray-900">{{ productUnit }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Tồn kho</h3>
              <p class="text-lg font-semibold text-gray-900">{{ product.in_stock || 0 }} {{ productUnit }}</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Kích thước</h3>
              <p class="text-lg font-semibold text-gray-900">
                {{ product.length || 0 }} × {{ product.width || 0 }} × {{ product.height || 0 }} cm
              </p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Trọng lượng</h3>
              <p class="text-lg font-semibold text-gray-900">{{ product.weight || 0 }} kg</p>
            </div>
            
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-1">Thuế VAT</h3>
              <p class="text-lg font-semibold text-gray-900">{{ product.tax_rate || 0 }}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


