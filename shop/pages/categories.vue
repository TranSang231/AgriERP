<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProductsService, type ProductCategory } from '~/services/products'

const { getCategories } = useProductsService()
const { t } = useI18n()

const categories = ref<ProductCategory[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    loading.value = true
    const data = await getCategories()
    categories.value = (data as any) || []
  } catch (e: any) {
    error.value = e?.message || t('categories.error.loadFailed')
  } finally {
    loading.value = false
  }
})

const getName = (cat: any) => {
  if (!cat) return t('categories.defaultName')
  // Support both plain string and ShortContent object
  return cat.name?.origin || cat.name || t('categories.defaultName')
}

// SEO Meta
useHead({
  title: t('categories.meta.title'),
  meta: [
    { name: 'description', content: t('categories.meta.description') }
  ]
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ $t('categories.title') }}</h1>
      <p class="text-gray-600">{{ $t('categories.subtitle') }}</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">{{ $t('categories.loading') }}</p>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('categories.error.title') }}</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <button @click="() => { onMounted() }" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        {{ $t('categories.error.retryButton') }}
      </button>
    </div>

    <div v-else-if="categories.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">📂</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('categories.empty.title') }}</h2>
      <NuxtLink to="/products" class="text-orange-600 hover:text-orange-700 font-medium">{{ $t('categories.empty.viewAllProducts') }}</NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <NuxtLink
        v-for="cat in categories"
        :key="cat.id"
        :to="`/products?category=${cat.id}`"
        class="block bg-white rounded-lg border shadow-sm p-6 hover:shadow-md hover:border-orange-300 transition"
      >
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">{{ getName(cat) }}</h3>
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
        <p v-if="cat.description?.origin || cat.description" class="text-sm text-gray-500 mt-2 line-clamp-2">
          {{ cat.description?.origin || cat.description }}
        </p>
      </NuxtLink>
    </div>
  </div>
</template>