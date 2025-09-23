<script setup lang="ts">
// TODO(shop-home): Replace mock with API calls
// - GET /product-categories -> categories
// - GET /products/summary-list -> products
// See backend routes at backend/ecommerce/urls.py
// Use useApi().request if you need auth headers
// const { request } = useApi()
// const { data: categories } = await request('/product-categories')
// const { data: products } = await request('/products/summary-list')

// Mock data for initial static UI
const categories = ref([
  { id: 1, name: 'Rau củ' },
  { id: 2, name: 'Trái cây' },
  { id: 3, name: 'Ngũ cốc' },
  { id: 4, name: 'Đồ uống' },
])
const products = ref([
  { id: 1, name: 'Gạo đen Hoa Sữa', price: 50000 },
  { id: 2, name: 'Organic Goji Berries 100gr', price: 200000 },
  { id: 3, name: 'Kiwi', price: 90000 },
  { id: 4, name: 'Táo Úc', price: 70000 },
  { id: 5, name: 'Cam Mỹ', price: 150000 },
])
const { format } = useCurrency()
</script>

<template>
  <div>
    <section class="bg-gradient-to-r from-primary-600 to-primary-700 text-white">
      <div class="container mx-auto px-4 py-10 md:py-16 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        <div>
          <h1 class="text-3xl md:text-4xl font-semibold">Organic Food</h1>
          <p class="mt-3 text-white/90">Sản phẩm nông sản sạch, tốt cho sức khỏe.</p>
          <NuxtLink to="/" class="btn-primary mt-6 inline-block">Mua ngay</NuxtLink>
        </div>
        <div class="hidden md:block">
          <div class="rounded-xl bg-white/10 aspect-video"></div>
        </div>
      </div>
    </section>

    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <aside class="md:col-span-1">
          <h2 class="font-semibold mb-3">Danh mục</h2>
          <ul class="space-y-2">
            <li v-for="c in categories" :key="c.id">
              <a href="#" class="hover:underline">{{ c.name }}</a>
            </li>
          </ul>
        </aside>
        <section class="md:col-span-3">
          <div class="flex items-center justify-between mb-3">
            <h2 class="font-semibold text-lg">Sản phẩm nổi bật</h2>
            <NuxtLink to="/" class="link-primary">Xem tất cả</NuxtLink>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <NuxtLink v-for="p in products" :key="p.id" :to="`/products/${p.id}`" class="border rounded p-3 hover:shadow-sm">
              <div class="bg-gray-100 aspect-square rounded" />
              <div class="font-medium line-clamp-2 min-h-[3rem] mt-2">{{ p.name }}</div>
              <div class="text-primary-600 font-semibold mt-1">{{ format(p.price) }}</div>
              <span class="text-xs text-gray-500">Còn hàng</span>
            </NuxtLink>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>


