<template>
  <EcommerceProductEditor
    :defaultData="{
      name: {origin: null},
      unit: {origin: null},
      price: 0.0,
      in_stock: 0.0,
      categories: [],
      category_ids: [],
      description: {origin: null},
      thumbnail: null,
      images: [],
      weight: 0.0,
      length: 0.0,
      width: 0.0,
      height: 0.0,
      tax_rate: 0.0
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'ecommerce'
})
</script>
