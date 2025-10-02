<template>
  <EcommerceProductEditor 
    :defaultData="productData"
    v-if="productData"
  />
  <div v-else class="flex justify-center items-center h-64">
    <el-loading v-loading="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import productService from '@/services/e-commerce/product'

const route = useRoute()
const productData = ref(null)
const loading = ref(true)

const loadProduct = async () => {
  try {
    loading.value = true
    const productId = route.params.id
    if (productId && productId !== 'new') {
      const response = await productService.get(productId)
      // Ensure category_ids is populated so the select shows current categories
      const categoryIds = Array.isArray(response?.categories)
        ? response.categories.map((c: any) => c?.id).filter(Boolean).map((id: any) => String(id))
        : []
      productData.value = { ...response, category_ids: categoryIds }
      console.log(productData.value)
    } else {
      // For new product, use default data
      productData.value = {
        name: { origin: null },
        unit: { origin: null },
        price: 0.0,
        in_stock: 0.0,
        categories: [],
        category_ids: [],
        description: { origin: null },
        thumbnail: null,
        images: [],
        weight: 0.0,
        length: 0.0,
        width: 0.0,
        height: 0.0,
        tax_rate: 0.0
      }
    }
  } catch (error) {
    console.error('Error loading product:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProduct()
})

definePageMeta({
  layout: 'ecommerce'
})
</script>