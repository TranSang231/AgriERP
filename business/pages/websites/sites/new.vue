<template>
  <WebsiteSiteEditor
    :defaultData="{
        domain_name: null,
        title: null,
        description: null,
        keywords: null,
        icon: null,
        template: null,
        template_settings: null,
        status: null
      }"
  />
</template>

<script setup lang="ts">
definePageMeta({
layout: 'websites'
})
</script>
