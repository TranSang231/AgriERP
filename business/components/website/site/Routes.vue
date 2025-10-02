<template>
    <div class="flex flex-col justify-start">
        <div v-if="fetching" class="flex flex-col w-full items-center mt-5 gap-5 justify-center content-center">
            <div v-loading="true"/>
            <div class="ps-10"><span>{{ t('Fetching_data') }}</span></div>
        </div>
        <div class="flex flex-col w-full gap-2">
            <draggable
                :list="current"
                :disabled="!canEdit"
                item-key="route"
                class="flex flex-col gap-2"
                :move="checkMove"
            >
                <template #item="{ element, index }">
                    <WebsiteSiteRoute
                        v-model="current[index]"
                        :editable="canEdit"
                        class="flex flex-col w-full h-full p-2 gap-2 border border-primary"
                    />
                </template>
            </draggable>
            <el-button v-if="canEdit" :icon="Plus" @click="insertItem" class="self-end px-2"> {{ t("add_new") }} </el-button>
        </div>
    </div>
  </template>
  
  <script setup>
  import { v4 as uuidv4 } from 'uuid';
  import draggable from 'vuedraggable'
  import RouteService from '@/services/websites/route';
  import { CirclePlus, Plus, Delete } from '@element-plus/icons-vue';
  import { useLocaleStore } from '@/stores/locale';
  import { useOauthStore } from "@/stores/oauth";
  import ConstantsService from '@/services/constants';
  
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
  const newPathCount = ref(0);
  const origin = ref([]);
  const current = ref([]);
  const fetching = ref(true);
  const itemTemplate = {
    path: null,
    title: null,
    description: null,
    keyword: null,
    content: null,
    status: 0,
    site_id: props.siteId
  }
  
  const fetchData = () => {
    ConstantsService.fetch("publishing_statuses");
    if (props.siteId) {
      // Fetch sections
      fetching.value = true;
      RouteService.getSiteRoutes(props.siteId)
        .then((response) => {
            const localItems = response.map((o) => ({...o, local_id: o.id}));
            origin.value = _cloneDeep(localItems);
            current.value = _cloneDeep(localItems);
        })
        .catch(() => {
            origin.value = [];
            current.value = [];
        })
        .finally(() => {
            fetching.value = false;
        });
    }
  };
  
  const insertItem = (type, node) => {
    newPathCount.value = newPathCount.value + 1
    let item = {
        ..._cloneDeep(itemTemplate),
        local_id: uuidv4(),
        path: `${t('Path').replace(' ', '-')}-${newPathCount.value}`
    };
    current.value =  [...current.value, item];
  }
  
  const onItemSaved = (data) => {
    console.log(data);
  };
  
  const removeItem = (data) => {
    console.log(data);
  }

  const checkMove = (e) => {
    console.log(e);
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
  