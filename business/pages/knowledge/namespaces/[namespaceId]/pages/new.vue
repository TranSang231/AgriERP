<template>
    <KnowledgePageEditor
      :defaultData="pageDefaultData"
    />
  </template>
  
<script setup lang="ts">
definePageMeta({
layout: 'namespace'
});
const route = useRoute();

const pageDefaultData = computed(() => {
const { namespaceId } = route.params;
const { parentId } = route.query;

return {
    title: null,
    slug: null,
    content: '',
    namespace_id: namespaceId,
    parent_id: parentId,
    created_by: null,
    updated_by: null
};
});

  
</script>