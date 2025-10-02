<template>
  <div class="flex flex-col justify-start">
    <div v-if="fetching" class="flex flex-col w-full items-center mt-5 gap-5 justify-center content-center">
      <div v-loading="true"/>
      <div class="ps-10"><span>{{ t('Fetching_data') }}</span></div>
    </div>
    <el-tree
      v-else
      ref="tree"
      :allow-drop="allowDrop"
      :allow-drag="allowDrag"
      :data="menus"
      label="local_id"
      :draggable="canEdit"
      default-expand-all
      node-key="local_id"
      class="w-full"
    >
      <template #default="{ node, data }">
        <TreeNodeModelForm
          :collapsible="false"
          :forceShowHeader="true"
          :fullWidth="true"
          :editable="canEdit"
          :service="MenuService"
          v-model="node.data"
          :nestedFields="['title']"
          :rules="rules"
          ref="modelForm"
          :parentId="node.parent ? node.parent.data.id : null"
        >
          <template #title="{current, editing}">
            <div class="flex flex-row">
              <el-form-item :label="t('Title')" prop="title">
                <ShortContentEditor
                  v-if="localeStore"
                  :editable="editing"
                  v-model="current.title"
                  :languages="localeStore.supportedLanguages"
                  :placeholder="t('default_place_holder')"
                />
              </el-form-item>
              <el-form-item :label="t('Url')" prop="url">
                <el-input v-if="editing"
                    v-model="current.url"
                    :placeholder="t('url_placeholder')"
                    style="min-width: 200px"
                />
                <span v-else>{{current.url}}</span>
              </el-form-item>
            </div>
          </template>
          <template #buttons="{current}">
            <el-popover
              v-if="canEdit &&  current.id"
              placement="left-start"
            >
              <template #reference>
                <el-button circle :icon="CirclePlus" class="text-primary  hover:text-on-primary hover:bg-primary"/>
              </template>
              <template #default>
                <div class="flex flex-col items-start content-start gap-2">
                  <el-button @click="() => insertItem('prev', node)">{{t('Insert_above')}}</el-button>
                  <el-button @click="() => insertItem('inner', node)">{{t('Insert_inside')}}</el-button>
                  <el-button @click="() => insertItem('next', node)">{{t('Insert_below')}}</el-button>
                </div>
              </template>
            </el-popover>
            <el-button
              v-if="canEdit"
              circle
              :icon="Delete"
              class="text-primary  hover:text-on-primary hover:bg-primary"
              @click="() => removeItem(node.data, node)"
            />
          </template>
        </TreeNodeModelForm>
      </template>
      <template #empty>
        <div class="flex flex-col w-full items-center mt-5 gap-5 justify-center">
          <span>{{ t('No_data_available') }}</span>
          <el-button type="primary" :icon="Plus" size="small" @click="addFirstItem">
            {{ $t('add_new') }}
          </el-button>
        </div>
      </template>
    </el-tree>
  </div>
</template>

<script setup>
import { v4 as uuidv4 } from 'uuid';
import MenuService from '@/services/websites/menu';
import { CirclePlus, Plus, Delete } from '@element-plus/icons-vue';
import { useLocaleStore } from '@/stores/locale';
import { useOauthStore } from "@/stores/oauth";
import ConstantsService from '@/services/constants';
import { nestedObjects } from "@/utils/obj";

const props = defineProps({
	siteId: {
		type: [String,null],
		default: null
	},
});

const { t } = useI18n();
const localeStore = useLocaleStore();
const oauthStore = useOauthStore();
const { tokenInfo } = storeToRefs(oauthStore);
const tree = ref(null);
const menus = ref([]);
const flatMenus = ref([]);
const fetching = ref(true);
const itemTemplate = {
  title: null,
  url: null,
  site_id: props.siteId
}

const fetchData = () => {
  ConstantsService.fetch("publishing_statuses");
  if (props.siteId) {
    // Fetch sections
    fetching.value = true;
    MenuService.getSiteMenus(props.siteId)
      .then((response) => {
        const localObjects = response.map((o) => ({...o, local_id: o.id}));
        flatMenus.value = _cloneDeep(localObjects)
        const localData = nestedObjects(localObjects);
        menus.value = localData;
      })
      .catch(() => {
        menus.value = [];
      })
      .finally(() => {
        fetching.value = false;
      });
  }
};

const insertItem = (type, node) => {
  if (!tree.value) {
    return;
  }
  const parent = node.parent;
  let item = {..._cloneDeep(itemTemplate), local_id: uuidv4(), parent_id: parent ? parent.data.id : null };
  if (type === 'prev') {
    tree.value.insertBefore(item, node);
    return;
  }
  if (type === 'next') {
    tree.value.insertAfter(item, node);
    return;
  }
  if (type === 'inner') {
    item = { ...item, parent_id: node.data? node.data.id : null };
    tree.value.append(item, node);
    return;
  }
}

const onItemSaved = (id, data) => {
  if (!tree.value) {
    return;
  }
  console.log(id, '\n', data);
  tree.value.updateKeyChildren(id, data)
};

const removeItem = (item, node) => {
  if (!tree.value) {
    return;
  }
  if (!item.id) {
    tree.value.remove(node);
    return;
  }
  MenuService.delete(item.id)
    .then(() => {
      tree.value.remove(node);
    })
    .catch((error) => {
      console.error(error);
    })
}

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

const addFirstItem = () => {
  const item = {..._cloneDeep(itemTemplate), local_id: uuidv4()};
  menus.value = [...menus.value, item];
};

const canEdit = computed(() => oauthStore.hasOneOfScopes(["websites:sites:edit"]))

onMounted(() => {
  fetchData();
});

watch(tokenInfo, () => {
    fetchData();
});

const rules = {
  title: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  url: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};
</script>
