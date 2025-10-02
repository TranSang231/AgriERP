<template>
  <WebsiteArticleEditor
    :defaultData="{
      title: {origin: null},
      slug: null,
      categories: [],
      description: {origin: null},
      sites: [],
      sections: [],
      thumbnail: null,
      content: null,
      status: null
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
layout: 'websites'
})
</script>
