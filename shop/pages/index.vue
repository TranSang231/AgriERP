<script setup lang="ts">
const config = useRuntimeConfig()
const { data: products } = await useFetch(() => `${config.public.apiBase}/products/summary-list`)
const { data: categories } = await useFetch(() => `${config.public.apiBase}/product-categories`)
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <aside class="md:col-span-1">
        <h2 class="font-semibold mb-3">Categories</h2>
        <ul class="space-y-2">
          <li v-for="c in categories?.results || []" :key="c.id">
            <NuxtLink :to="`/?category=${c.id}`" class="hover:underline">{{ c.name }}</NuxtLink>
          </li>
        </ul>
      </aside>
      <section class="md:col-span-3">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <NuxtLink v-for="p in products?.results || []" :key="p.id" :to="`/products/${p.id}`" class="border rounded p-3 hover:shadow">
            <div class="font-medium line-clamp-2 min-h-[3rem]">{{ p.name }}</div>
            <div class="text-primary-600 font-semibold mt-2">{{ p.price | currency }}</div>
          </NuxtLink>
        </div>
      </section>
    </div>
  </div>
</template>


