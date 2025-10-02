<template>
  <WebsiteArticleCategoryEditor
    :defaultData="{
      name: {origin: null},
      slug: null,
      description: null
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
layout: 'websites'
})
</script>
