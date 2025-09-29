<template>
  <client-only>
    <div class="flex flex-col items-center">
      <!-- error message -->
      <p v-if="error" class="self-center text-red-800">{{ error }}</p>

      <!-- search + buttons -->
      <div class="flex flex-row self-end gap-2 my-2">
        <slot name="filter">
          <el-input
            v-if="searchable"
            v-model="keyword"
            style="max-width: 500px"
            :placeholder="t('Keyword')"
            clearable
          >
            <template #append>
              <el-button :icon="Search" @click="applySearch" />
            </template>
          </el-input>
        </slot>
        <slot name="buttons">
          <el-button
            v-if="allowExportToExcel"
            :icon="Excel"
            @click="exportToExcel"
          >
            {{ t("to_excel") }}
          </el-button>
          <el-button
            v-if="allowExportToJson"
            :icon="Json"
            @click="exportToJson"
          >
            {{ t("to_json") }}
          </el-button>
          <el-button
            v-if="selectedItems.length > 0"
            :icon="Delete"
            @click="onMultipleDelete"
          >
            {{ t("delete") }}
          </el-button>
        </slot>
      </div>

      <!-- table -->
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
            <el-button
              v-if="canEditItems"
              :icon="Edit"
              size="small"
              @click="editItem(scope.row.id)"
            />
            <el-button
              v-if="canDeleteItems"
              :icon="Delete"
              size="small"
              @click="onDeleteItem(scope.row)"
            />
            <slot name="addonButtons" :row="scope.row" />
          </template>
        </el-table-column>
      </el-table>

      <!-- pagination -->
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

      <!-- add button -->
      <el-button
        v-if="canAddItems"
        type="primary"
        :icon="Plus"
        @click="onAdd"
        class="self-end px-2 mb-2"
      >
        {{ t("add_new") }}
      </el-button>

      <!-- confirm delete dialog -->
      <el-dialog
        v-model="confirmDeleteDialog"
        :title="t('confirm_deleting')"
        center
      >
        <span class="flex justify-center">
          {{ confirmDeletingMessage || t("deleting_item_confirm_default_message") }}
        </span>
        <template #footer>
          <div class="dialog-footer">
            <el-button type="primary" @click="deleteItem">{{ t("yes") }}</el-button>
            <el-button plain @click="cancelDeletingItem">{{ t("cancel") }}</el-button>
          </div>
        </template>
      </el-dialog>

      <!-- confirm multiple delete dialog -->
      <el-dialog
        v-model="confirmMultipleDeleteDialog"
        :title="t('confirm_deleting')"
        center
      >
        <span class="flex justify-center">
          {{ confirmMultipleDeletingMessage || t("deleting_items_confirm_default_message") }}
        </span>
        <template #footer>
          <div class="dialog-footer">
            <el-button type="primary" @click="multipleDelete">{{ t("yes") }}</el-button>
            <el-button plain @click="cancelMultipleDeleting">{{ t("cancel") }}</el-button>
          </div>
        </template>
      </el-dialog>

      <!-- extra addon dialogs -->
      <slot name="addon-confirm-dialog" />
    </div>
  </client-only>
</template>
<script setup lang="ts" generic="S extends BaseService">
import { Plus, Delete, Edit, Search } from "@element-plus/icons-vue";
import Excel from "@/assets/icons/excel.svg";
import Json from "@/assets/icons/json.svg";
import { ref, watch, computed, onMounted } from "vue";
import { useRoute, navigateTo } from "#app";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";
import { useOauthStore } from "@/stores/oauth";

import BaseService from "@/services/base";
import { toExcel } from "@/exporters/xls/xlsx";
import { toJson } from "@/exporters/json/json";
import { getErrorMessage } from "@/utils/error";

const props = defineProps<{
  service: S;
  pageSize?: number;
  searchable: boolean;
  multipleSelect?: boolean;
  canDeleteItems?: boolean;
  canEditItems?: boolean;
  canAddItems?: boolean;
  confirmDeletingMessage?: string;
  confirmMultipleDeletingMessage?: string;
  allowExportToExcel: boolean;
  excelSheetName?: string;
  excelFileName?: string;
  exportFields?: Record<string, any>;
  allowExportToJson: boolean;
  jsonFileName?: string;
  disableRowClick?: boolean;
  hasAddonButtons?: boolean;
  prefix?: string;
  onItemDeleted?: (item: any) => void;
  onItemsDeleted?: (items: any[]) => void;
  
  // Prop quan trọng để nhận bộ lọc từ component cha (index.vue)
  queryParams?: Record<string, any>;
}>();

const { t } = useI18n();
const route = useRoute();

const loading = ref(false);
const keyword = ref(""); // Dành cho ô tìm kiếm nội bộ của bảng
const selectedItems = ref<any[]>([]);
const data = ref({
  page: 1,
  page_size: props.pageSize || 10,
  num_pages: 0,
  count: 0,
  results: [] as any[],
});
const error = ref<string | null>(null);
const deletingItem = ref<any>(null);
const confirmDeleteDialog = ref(false);
const confirmMultipleDeleteDialog = ref(false);

const oauthStore = useOauthStore();
const { tokenInfo } = storeToRefs(oauthStore);

// Computed "query" là bộ não trung tâm, gộp tất cả tham số lại với nhau
const query = computed(() => {
  const params: Record<string, any> = {
    page: data.value.page,
    page_size: data.value.page_size,
    ...props.queryParams, // Gộp bộ lọc từ bên ngoài vào
  };
  
  // Gộp từ khóa tìm kiếm nội bộ của bảng (nếu có)
  if (keyword.value.trim().length > 0) {
    params.keyword = keyword.value.trim();
  }

   Object.keys(params).forEach(
    key => (params[key] === null || params[key] === '') && delete params[key]
  );

  return params;
});

// Hàm gọi API chính
const fetchData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await props.service.gets(query.value); 
    if (query.value.page_size) {
      const { page, num_pages, count, results } = response;
      data.value = { ...data.value, page, num_pages, count, results };
    } else {
      data.value.results = response;
    }
  } catch (e: any) {
    error.value = getErrorMessage(
      e,
      e.statusCode ? t("an_error_occurred") : t("connection_corrupted")
    );
  } finally {
    loading.value = false;
  }
};

// =============================================================
// PHẦN QUAN TRỌNG NHẤT: CƠ CHẾ PHẢN ỨNG VỚI THAY ĐỔI
// =============================================================

// 1. Khi bộ lọc từ bên ngoài thay đổi, quay về trang 1 và tải lại
watch(() => props.queryParams, () => {
  data.value.page = 1;
  fetchData();
}, { deep: true });

// 2. Khi người dùng chuyển trang
const onCurrentPageChange = (page: number) => {
  data.value.page = page;
  fetchData();
};

// 3. Khi người dùng bấm nút tìm kiếm nội bộ của bảng
const applySearch = () => {
  data.value.page = 1;
  fetchData();
};

// =============================================================

// Các hàm điều khiển để component cha có thể gọi nếu cần
const loadData = () => {
  fetchData();
};
const resetPageAndLoadData = () => {
  data.value.page = 1;
  fetchData();
};
defineExpose({ data, error, loadData, resetPageAndLoadData });


// Lifecycle
onMounted(fetchData);
watch(tokenInfo, (newToken) => {
  if (newToken) {
    fetchData();
  }
}, { immediate: false });

/* Các hàm còn lại giữ nguyên chức năng */
const onSelectionChange = (val: any[]) => { selectedItems.value = val; };
const onRowClick = (row: any, column: any) => {
  if (props.disableRowClick) return;
  if (!row.id || !column.property) return;
  const to = props.prefix
    ? `${route.path}/${props.prefix}/${row.id}`
    : `${route.path}/${row.id}`;
  navigateTo(to);
};
const onDeleteItem = (item: any) => {
  deletingItem.value = item;
  confirmDeleteDialog.value = true;
};
const deleteItem = async () => {
  if (!deletingItem.value) return;
  error.value = null;
  const { id } = deletingItem.value;
  try {
    await props.service.delete(id);
    data.value.results = data.value.results.filter((i) => i.id !== id);
    if (data.value.results.length === 0 && data.value.page > 1) {
      data.value.page--;
    }
    props.onItemDeleted?.(deletingItem.value);
  } catch (e: any) {
    error.value = getErrorMessage(e, t("an_error_occurred"));
  } finally {
    confirmDeleteDialog.value = false;
    deletingItem.value = null;
  }
};
const cancelDeletingItem = () => {
  confirmDeleteDialog.value = false;
  deletingItem.value = null;
};
const onMultipleDelete = () => { confirmMultipleDeleteDialog.value = true; };
const multipleDelete = async () => {
  const items = selectedItems.value;
  if (!items.length) return;
  const ids = items.map((i) => i.id);
  error.value = null;
  try {
    await props.service.multipleDelete(ids);
    data.value.results = data.value.results.filter((i) => !ids.includes(i.id));
    if (data.value.results.length === 0 && data.value.page > 1) {
      data.value.page--;
    }
    props.onItemsDeleted?.(items);
  } catch (e: any) {
    error.value = getErrorMessage(e, t("an_error_occurred"));
  } finally {
    confirmMultipleDeleteDialog.value = false;
  }
};
const cancelMultipleDeleting = () => { confirmMultipleDeleteDialog.value = false; };
const editItem = (id: string) => {
  const path = props.prefix
    ? `${route.path}/${props.prefix}/${id}?edit=true`
    : `${route.path}/${id}?edit=true`;
  navigateTo(path);
};
const onAdd = () => {
  const path = props.prefix
    ? `${route.path}/${props.prefix}/new`
    : `${route.path}/new`;
  navigateTo(path);
};
const exportToExcel = () => {
  if (data.value.results.length) {
    toExcel(data.value.results, props.excelSheetName, props.excelFileName, props.exportFields, t);
  }
};
const exportToJson = () => {
  if (data.value.results.length) {
    toJson(data.value.results, props.jsonFileName);
  }
};
</script>