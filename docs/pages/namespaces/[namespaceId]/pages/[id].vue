<template>
    <KnowledgePageViewer :data="page" />
</template>
  
<script setup lang="ts">
import PageService from '@/services/knowledge/page';
definePageMeta({
layout: 'namespace'
})

const route = useRoute();
const page = ref<any>(null)

onMounted(() => {
    const { id } = route.params;
    if (!id) {
        return;
    }
    PageService.get(id)
        .then((response) => {
            page.value = response
        })
        .catch((e: any) => {
            console.error(e);
        });

});
</script>