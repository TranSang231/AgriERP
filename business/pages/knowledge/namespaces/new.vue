<template>
  <KnowledgeNamespaceEditor
    :defaultData="{
      logo: null,
      name: null,
      slug: null,
      description: null,
      access: 0,
      member_ids: [],
      owner_id: oauthStore.userId
    }"
  />
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
definePageMeta({
  layout: 'knowledge'
});

const oauthStore = useOauthStore();
</script>