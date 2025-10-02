<template>
  <div class="flex flex-row gap-2 items-center">
    <NuxtLink
      :to="`/knowledge/namespaces/${namespaceId}/pages/${data.id}`"
      class="flex flex-row"
    >
        <span>{{ data.title ? data.title : t('No_title') }}</span>
    </NuxtLink>
    <el-dropdown
      v-if="canEdit"
      placement="bottom-start"
      @command="handleCommand"
    >
      <el-button
        circle
        :icon="MoreFilled"
        size="small"
        class="bg-primary text-white hover:bg-white hover:text-primary"
        />
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="add">{{t('Add_page')}}</el-dropdown-item>
          <el-dropdown-item command="move">{{t('Move_page')}}</el-dropdown-item>
          <el-dropdown-item command="delete">{{t('Delete_page')}}</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { MoreFilled } from '@element-plus/icons-vue';
import { useOauthStore } from "@/stores/oauth";

const props = defineProps({
  node: {
    type: Object,
    required: true
  },
  data: {
    type: Object,
    required: true
  }
});
const emit = defineEmits(['onRemoveItem']);

const { t } = useI18n();
const route = useRoute();

const oauthStore = useOauthStore();
const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["knowledge:pages:edit"]);
});

const isCurrentPage = computed(() => {
  const { id } = route.params
  return id && id === props.data.id;
});

const namespaceId = computed(() => {
  if (!props.data) {
    const { namespaceId } = route.params
    return namespaceId;
  }
  const { namespace, namespace_id } = props.data;
  return namespace_id 
    ? namespace_id
    : namespace
      ? namespace.id
      : null;

});

const handleCommand = (command: String, ...args: any[]) => {
  const { id } = props.data;
  if (!id) {
    return;
  }

  if (command === "add") {
    navigateTo(`/knowledge/namespaces/${namespaceId.value}/pages/new?parentId=${id}`);
    return;
  }

  if (command === "delete") {
    emit('onRemoveItem', props.data, props.node);
    return;
  }
};

</script>