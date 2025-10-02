<template>
  <div class="w-full">
    <el-menu-item
      v-if="route.params && route.params.namespaceId"
      :index="`/knowledge/namespaces/${route.params.namespaceId}`"
    >
        <House class="el-icon" />
        <span>{{ t('Home_page') }}</span>
    </el-menu-item>
    <div
      v-if="fetching"
      class="flex flex-col w-full items-center mt-5 gap-5 justify-center content-center text-white"
    >
      <div v-loading="true" />
      <div><span>{{ t('Fetching_data') }}</span></div>
    </div>
    <el-tree
      v-else
      ref="tree"
      :allow-drop="allowDrop"
      :allow-drag="allowDrag"
      :data="pages"
      label="local_id"
      :draggable="canEdit"
      default-expand-all
      node-key="local_id"
      class="overflow-scroll text-white bg-transparent"
    >
      <template #default="{ node, data }">
        <PageTreeNode
          :node="node"
          :data="data"
          @onRemoveItem="removeItem"
        />
      </template>
    </el-tree>
  </div>
</template>

<script setup>
import { House } from '@element-plus/icons-vue';
import PageTreeNode from './PageTreeNode.vue';
import { useOauthStore } from "@/stores/oauth";
import PageService from '@/services/knowledge/page';
import { ref, onMounted, watch, computed } from 'vue';

const { t } = useI18n();
const route = useRoute();

const tree = ref(null);
const pages = ref([]);
const fetching = ref(true);

const oauthStore = useOauthStore();
const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["knowledge:pages:edit"]);
});

const allowDrop = (draggingNode, dropNode, type) => {
  if (type === 'inner') {
    const drop_id = dropNode.data && dropNode.data.id ? dropNode.data.id : null;
    if (!drop_id) {
      return false;
    }
    return true;
  }
  return true;
}
const allowDrag = (draggingNode) => {
  return true;
}

const fetchData = () => {
  const { namespaceId } = route.params;
  if (!namespaceId) {
    return;
  }

  fetching.value = true;
  PageService.gets({ namespace_id: namespaceId })
    .then((response) => {
      const results = response.results || response || [];
      const localData = nestedObjects(results.map((o) => ({...o, local_id: o.id})));
      pages.value = localData;
    })
    .catch((error) => {
      console.error('Error loading pages:', err);
      pages.value = [];
    })
    .finally(() => {
      fetching.value = false;
    });
};

const createPage = () => {
  const { namespaceId } = route.params;
  navigateTo(`/knowledge/namespaces/${namespaceId}/pages/new`);
};

const removeItem = (item, node) => {
  console.log('removeItem:', item)
  if (!tree.value) {
    return;
  }
  if (!item.id) {
    tree.value.remove(node);
    return;
  }
  PageService.delete(item.id)
    .then(() => {
      tree.value.remove(node);
    })
    .catch((error) => {
      console.error(error);
    })
}

watch(() => route.params.namespaceId, (newValue) => {
  if (newValue) {
    fetchData();
  }
}, { immediate: true });

defineExpose({
  refresh: fetchData
});

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
:deep(.el-tree) {
  --el-tree-node-hover-bg-color: #FFFFFF66
}
</style>