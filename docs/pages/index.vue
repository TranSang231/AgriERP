<template>
    <div class="flex flex-col w-full justify-center pt-20 gap-2">
      <span class="w-full text-center">{{t('Thank_for_visiting')}}</span>
      <div
        v-if="namespacesStore.allNamespaces"
        class="flex flex-row w-full, items-start justify-start text-primary px-5"
      >
        <NuxtLink
          v-for="namespace in namespacesStore.allNamespaces"
          :to="`/namespaces/${namespace.id}`"
        >
          <span>{{ namespace.name }}</span>
        </NuxtLink>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import NamespaceService from "@/services/knowledge/namespace";
  import ConstantsService from "@/services/constants";
  import { formatDateTime } from "~/utils/time";
  import { useNamespacesStore } from "@/stores/knowledge/namespaces";
  import { useI18n } from 'vue-i18n';
  definePageMeta({
      layout: 'default'
  })
  
  const { t } = useI18n();
  const route =  useRoute();
  const namespacesStore = useNamespacesStore();
  
  const fetchData = () => {
    ConstantsService.fetch("access_modes");
    NamespaceService.fetch();
  };
  onMounted(() => {
    fetchData();
  });
  </script>