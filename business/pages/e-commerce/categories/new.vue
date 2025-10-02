<template>
  <EcommerceProductCategoryEditor
    :defaultData="{
      name: {origin: null},
      description: null
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'ecommerce'
})
</script>
