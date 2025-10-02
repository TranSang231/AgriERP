<template>
  <div v-if="loading" class="flex flex-col pt-20 w-full items-center content-center">
    <el-icon class="is-loading text-gray-400" :size="24">
      <Loading />
    </el-icon>
    <span>{{ t('Loading_data')}}</span>
  </div>
  <KnowledgeNamespaceHomePageEditor v-else
    :defaultData=homePage
  />
</template>

<script setup lang="ts">
import { 
  Setting,
  Document,
  Loading,
  Check,
  InfoFilled,
} from '@element-plus/icons-vue';
import { ref, computed, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import NamespaceService from '@/services/knowledge/namespace';
import HomePageService from '@/services/knowledge/home-page' ;
import { useOauthStore } from "@/stores/oauth";

definePageMeta({
  layout: 'namespace'
})

const { t } = useI18n()
const route = useRoute()

const homePage = ref<any>(null)
const loading = ref(false)

const fetchData = () => {
  const { namespaceId } = route.params;
  console.log(namespaceId);
  if (!namespaceId) {
    return;
  }
  loading.value = true;
  HomePageService.getByNamespace(namespaceId)
    .then((response: any) => {
      homePage.value = response;
    })
    .catch((e:any) => {
      if (e.status && e.status == 404) {
        homePage.value = {
          namespace_id: namespaceId,
          content: null
        }
      }
    })
    .finally(() => {
      loading.value = false;
    })
};

onMounted(() => {
  fetchData();
});

</script>