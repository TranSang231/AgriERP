<template>
  <client-only>
    <div class="flex flex-col items-center">
      <div class="flex flex-row self-end gap-2 my-2">
        <el-input
          v-if="searchable"
          v-model="keyword"
          style="max-width: 500px"
          :placeholder="t('Keyword')"
        >
          <template #append>
            <el-button :icon="Search" />
          </template>
        </el-input>
        <el-button v-if="allowExportToExcel" :icon="Excel">{{
          t("to_excel")
        }}</el-button>
        <el-button v-if="allowExportToJson" :icon="Json">{{
          t("to_json")
        }}</el-button>
        <el-button v-if="changed" :icon="Save" @click="save()">{{
          t("Save")
        }}</el-button>
        <el-button
          v-if="selectedItems && selectedItems.length > 0"
          :icon="Delete"
          @click="onMultipleDelete()"
        >
          Delete
        </el-button>
      </div>
      <el-table
        v-loading="loading"
        :data="filtered"
        stripe
        border
        style="width: 100%"
        @selection-change="onSelectionChange"
      >
        <el-table-column v-if="multipleSelect" type="selection" width="55" />
        <slot />
        <el-table-column
          v-if="canDeleteItems || canEditItems"
          :label="t('Operations')"
          min-width="120"
        >
          <template #default="scope">
            <el-button
              v-if="canDeleteItems"
              :icon="Delete"
              size="small"
              @click="deleteItem(scope.row.local_id)"
            />
          </template>
        </el-table-column>
      </el-table>
      <el-button v-if="canAddItems" :icon="Plus" @click="onAdd()" class="self-end px-2"> {{ t("add_new") }} </el-button>
    </div>
  </client-only>
</template>

<script setup lang="ts" generic="S extends BaseService">
import { Plus, Delete, Edit, Search } from "@element-plus/icons-vue";
import Excel from "@/assets/icons/excel.svg";
import Json from "@/assets/icons/json.svg";
import Save from "@/assets/icons/save.svg";
import { ref, watch } from "vue";
import BaseService from "@/services/base";
import { diff, toLocal, toWriteObjetc } from "@/utils/obj";

const props = defineProps<{
  service: S;
  searchable: Boolean;
  multipleSelect?: Boolean;
  canDeleteItems?: Boolean;
  canEditItems?: Boolean;
  canAddItems?: Boolean;
  allowExportToExcel?: Boolean;
  allowExportToJson?: Boolean;
  itemTemplate: any | null;
  filter: Function | null;
}>();

const { t } = useI18n();
const route = useRoute();

const loading = ref(false);
const keyword = ref("");
const selectedItems = ref([]);
const origin:any = ref([]);
const current:any = ref([]);

const filtered = computed(() => {
  if (props.filter) {
    const _keyword = keyword.value;
    return current.value.filter((o: any) => props.filter(o, _keyword));
  }
  return current.value;
});

const changes = computed(() => {
  const o = origin.value;
  const c = current.value;
  const diff1 = _differenceWith(c, o, _isEqual);
  const diff2 = _differenceWith(o, c, _isEqual);
  const diff1_local_ids = diff1.map((o) => o.local_id);
  const subtract = diff2.filter((o) => !diff1_local_ids.includes(o.local_id));
  return [...diff1, ...subtract];
});

const changed = computed(() => {
  const c = changes.value;
  if (!c) {
    return false;
  }
  return c.length > 0;
});
const onSelectionChange = (val: any) => {
  selectedItems.value = val;
};

const onMultipleDelete = async () => {
  const items:any = selectedItems.value;
  if (!items || items.length == 0) {
    return;
  }
  const local_ids = items.map((item: any) => item.local_id);
  // server-side ids
  const ids = items.map((item: any) => item.id).filter((id: any) => !!id);
  try {
    if (ids.length > 0) {
      await props.service.multipleDelete(ids);
      // remove from origin as well to avoid showing as changed
      origin.value = origin.value.filter((o: any) => !ids.includes(o.id));
    }
  } catch (error) {
    console.error(error);
  } finally {
    current.value = current.value.filter((o: any) => !local_ids.includes(o.local_id));
  }
};

const fetchData = async () => {
  loading.value = true;
  props.service
    .gets()
    .then((resposnse: any) => {
      const items = resposnse.map((i: any) => toLocal(i));
      origin.value = _cloneDeep(items);
      current.value = _cloneDeep(items);
    })
    .catch((error: any) => {
      console.log(error);
    })
    .finally(() => {
      loading.value = false;
    });
};

const deleteItem = async (local_id: any) => {
  const item:any = current.value.find((i: any) => i.local_id === local_id);
  const id = item ? item.id : null;
  try {
    if (id) {
      await props.service.delete(id);
      origin.value = origin.value.filter((o: any) => o.id !== id);
    }
  } catch (error) {
    console.error(error);
  } finally {
    current.value = current.value.filter((i: any) => i.local_id !== local_id);
  }
};

const onAdd = () => {
  if (props.itemTemplate) {
    current.value = [...current.value, toLocal(_cloneDeep(props.itemTemplate))];
  }
};

const save = async () => {
  const items = current.value;
  if (!items) {
    return;
  }
  const data = items.map((i: any) => toWriteObjetc(i));

  props.service
    .sync(data)
    .then((response: any) => {
      const items = response.map((i: any) => toLocal(i));
      origin.value = _cloneDeep(items);
      current.value = _cloneDeep(items);
    })
    .catch((error: any) => {
      console.error(error);
    });
};

onMounted(() => {
  fetchData();
});
</script>
