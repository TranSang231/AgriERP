<template>
  <client-only>
    <div class="flex flex-col items-center">
      <p v-if="error" class="self-center text-red-800">{{ error }}</p>
      <div class="flex flex-row self-end gap-2 my-2">
        <slot name="filter">
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
        </slot>
        <slot name="buttons">
          <el-button v-if="allowExportToExcel" :icon="Excel" @click="exportToExcel">{{ t("to_excel") }}</el-button>
          <el-button v-if="allowExportToJson" :icon="Json" @click="exportToJson">{{ t("to_json") }}</el-button>
          <el-button
            v-if="selectedItems && selectedItems.length > 0"
            :icon="Delete"
            @click="onMultipleDelete()"
          >
            Delete
          </el-button>
        </slot>
      </div>
      <el-table
        v-loading="loading"
        :data="data.results"
        stripe
        border
        style="width: 100%"
        @selection-change="onSelectionChange"
        @row-click="onRowClick"
      >
        <el-table-column v-if="multipleSelect" type="selection" width="55" />
        <slot />
        <el-table-column
          v-if="canDeleteItems || canEditItems || hasAddonButtons"
          :label="t('Operations')"
          :min-width="160"
        >
          <template #default="scope">
            <el-button v-if="canEditItems" :icon="Edit" size="small" @click="editItem(scope.row.id)" />
            <el-button v-if="canDeleteItems" :icon="Delete" size="small" @click="onDeleteItem(scope.row)" />
            <slot name="addonButtons" :row="scope.row" />
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-if="pageSize && pageSize.valueOf() > 0"
        :page-size="data.page_size.valueOf()"
        :page-count="data.num_pages"
        :total="data.count"
        :current-page="data.page"
        layout="prev, pager, next"
        class="mt-6"
        @current-change="onCurrentPageChange"
      />
      <el-button
        v-if="canAddItems"
        type="primary"
        :icon="Plus"
        @click="onAdd()"
        class="self-end px-2 mb-2"
      >
        {{ t("add_new") }}
      </el-button>
      <el-dialog
        v-model="confirmDeleteDialog"
        :title="t('confirm_deleting')"
        center
        align-center
      >
        <span class="flex justify-center">
          {{
            confirmDeletingMessage
              ? confirmDeletingMessage
              : t("deleting_item_confirm_default_message")
          }}
        </span>
        <template #footer>
          <div class="dialog-footer">
            <el-button type="primary" @click="deleteItem">{{t("yes")}}</el-button>
            <el-button plain @click="cancelDeletingItem">
              {{ t("cancel") }}
            </el-button>
          </div>
        </template>
      </el-dialog>
      <el-dialog
        v-model="confirmMultipleDeleteDialog"
        :title="t('confirm_deleting')"
        center
        align-center
      >
        <span class="flex justify-center">
          {{
            confirmMultipleDeletingMessage
              ? confirmMultipleDeletingMessage
              : t("deleting_items_confirm_default_message")
          }}
        </span>
        <template #footer>
          <div class="dialog-footer">
            <el-button type="primary" @click="multipleDelete">{{
              t("yes")
            }}</el-button>
            <el-button plain @click="cancelMultipleDeleting">
              {{ t("cancel") }}
            </el-button>
          </div>
        </template>
      </el-dialog>
      <slot name="addon-confirm-dialog" />
    </div>
  </client-only>
</template>

<script setup lang="ts" generic="S extends BaseService">
import {
  Plus,
  Delete,
  Edit,
  Search,
} from "@element-plus/icons-vue";
import Excel from "@/assets/icons/excel.svg";
import Json from "@/assets/icons/json.svg";
import { ref, watch } from "vue";
import BaseService from "@/services/base";
import { diff } from "@/utils/obj";
import { toExcel } from "@/exporters/xls/xlsx";
import { toJson } from "@/exporters/json/json";
import { getErrorMessage } from "@/utils/error";

const props = defineProps<{
  service: S;
  pageSize?: Number;
  searchable: Boolean;
  multipleSelect?: Boolean;
  canDeleteItems?: Boolean;
  canEditItems?: Boolean;
  canAddItems?: Boolean;
  confirmDeletingMessage?: String;
  confirmMultipleDeletingMessage?: String;
  allowExportToExcel: Boolean;
  excelSheetName?: String;
  excelFileName?: String;
  exportFields?: Object;
  allowExportToJson: Boolean;
  jsonFileName?: String;
  disableRowClick?: Boolean;
  service_params?: Record<string, any>;
  hasAddonButtons?: Boolean;
  filter?: Object;
  prefix?: String;
  onItemDeleted?: Function;
  onItemsDeleted?: Function;
}>();

const { t } = useI18n();
const route = useRoute();

const loading = ref(false);
const keyword = ref("");
const debouncedKeyword = ref<string>("");
let timeout: number | undefined = undefined;
const selectedItems = ref([]);
const data = ref({
  page: 1,
  page_size: props.pageSize ? props.pageSize : 0,
  num_pages: 0,
  count: 0,
  results: [],
});
const error = ref(null);
const deletingItem = ref(null);
const confirmDeleteDialog = ref(false);
const confirmMultipleDeleteDialog = ref(false);

const oauthStore = useOauthStore();
const { tokenInfo } = storeToRefs(oauthStore);

defineExpose({ data: data, error: error });

const query = computed<any>(() => {
  const filter = props.filter ? props.filter : {};
  const { page, page_size } = data.value;
  let params = {};
  if (page_size && page_size.valueOf() > 0) {
    params = { ...params, page_size };
  }
  if (page && page > 0) {
    params = { ...params, page };
  }
  if (debouncedKeyword.value && debouncedKeyword.value.trim().length > 0) {
    params = { ...params, keyword: debouncedKeyword.value };
  }
  if (props.service_params) {
    params = { ...params, ...props.service_params };
  }
  return {...filter, ...params};
});

const onSelectionChange = (val: any) => {
  selectedItems.value = val;
};

const onRowClick = (row: any, column: any, event: any) => {
  if (props.disableRowClick) {
    return;
  }
  const { id } = row;
  const { property } = column;
  if (!property || !id) {
    return;
  }
  const to = props.prefix
    ? `${route.path}/${props.prefix}/${id}`
    : `${route.path}/${id}`
  navigateTo(to);
};

const onCurrentPageChange = (page: number) => {
  data.value.page = page;
};

const onDeleteItem = async (item: any) => {
  deletingItem.value = item;
  confirmDeleteDialog.value = true;
};

const deleteItem = async () => {
  if (!deletingItem.value) {
    return;
  }
  error.value = null;
  const { id } = deletingItem.value;
  props.service
    .delete(id)
    .then(() => {
      const { page, results } = data.value;
      const newResults = results.filter((i: any) => i.id !== id);
      if (newResults.length === 0 && page > 0) {
        data.value.page = page - 1;
      } else {
        data.value.results = newResults;
      }
    })
    .catch((e: any) => {
      error.value = getErrorMessage(e, t("an_error_occurred"));
    })
    .finally(() => {
      confirmDeleteDialog.value = false;
      if (props.onItemDeleted) {
        props.onItemDeleted(deletingItem.value);
      }
    });
};
const cancelDeletingItem = () => {
  confirmDeleteDialog.value = false;
  deletingItem.value = null;
};

const onMultipleDelete = () => {
  confirmMultipleDeleteDialog.value = true;
};

const multipleDelete = () => {
  const items = selectedItems.value;
  if (!items || items.length == 0) {
    return;
  }
  const ids = items.map((item: any) => item.id);
  error.value = null;
  props.service
    .multipleDelete(ids)
    .then(() => {
      const { page, results } = data.value;
      const newResults = results.filter((i:any) => ids.indexOf(i.id) == -1);
      if (newResults.length === 0 && page > 0) {
        data.value.page = page - 1;
      } else {
        data.value.results = newResults;
      }
    })
    .catch((e: any) => {
      error.value = getErrorMessage(e, t("an_error_occurred"));
    })
    .finally(() => {
      confirmMultipleDeleteDialog.value = false;
      if (props.onItemsDeleted) {
        props.onItemsDeleted(items);
      }
    });
};

const cancelMultipleDeleting = () => {
  confirmMultipleDeleteDialog.value = false;
};

const fetchData = async () => {
  const { page_size } = query.value;
  loading.value = true;
  error.value = null;

  props.service
    .gets(query.value)
    .then((response:any) => {
      if (page_size) {
        const { page, num_pages, count, results } = response;
        data.value = {
          ...data.value,
          page,
          num_pages,
          count,
          results,
        };
      } else {
        data.value = {
          ...data.value,
          results: response,
        };
      }
    })
    .catch((e: any) => {
      error.value = getErrorMessage(e, e.statusCode ? t('an_error_occurred') : t('connection_corrupted'));
    })
    .finally(() => {
      loading.value = false;
    });
};

const editItem = (id: string) => {
  const path = props.prefix
    ? `${route.path}/${props.prefix}/${id}?edit=true`
    : `${route.path}/${id}?edit=true`
  navigateTo(path);
};

const onAdd = () => {
  const path = props.prefix
    ? `${route.path}/${props.prefix}/new`
    : `${route.path}/new`
  navigateTo(path);
};

const exportToExcel = () => {
  const { results } = data.value;
  if (results) {
    toExcel(
      results,
      props.excelSheetName,
      props.excelFileName,
      props.exportFields,
      t
    );
  }
};

const exportToJson = () => {
  const { results } = data.value;
  if (results) {
    toJson(results, props.jsonFileName);
  }
};

onMounted(() => {
  fetchData();
});

watch(keyword, (newKeyword) => {
  if (timeout !== undefined) {
    clearTimeout(timeout);
  }

  timeout = window.setTimeout(() => {
    data.value.page = 1;
    debouncedKeyword.value = newKeyword;
  }, 300);
});

watch(query, async (newValue, oldValue) => {
  const different = diff(newValue, oldValue);
  if (different) {
    fetchData();
  }
});

watch(tokenInfo, () => {
    fetchData();
});
</script>
