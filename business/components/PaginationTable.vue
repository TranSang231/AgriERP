<template>
  <client-only>
    <div class="w-full">
      <!-- Vùng hiển thị lỗi tập trung -->
      <el-alert v-if="error" :title="t('Error')" type="error" :description="error" show-icon class="mb-4" />

      <!-- Các nút chức năng chính (export, xóa hàng loạt) -->
      <div class="flex flex-wrap items-center justify-end gap-2 my-2">
        <slot name="buttons">
          <el-button v-if="allowExportToExcel" :icon="Excel" @click="exportToExcel">{{ t("to_excel") }}</el-button>
          <el-button v-if="allowExportToJson" :icon="Json" @click="exportToJson">{{ t("to_json") }}</el-button>
          <el-button
            v-if="multipleSelect && selectedItems.length > 0"
            type="danger"
            :icon="Delete"
            @click="onMultipleDelete()"
          >
            {{ t('delete_selected_items', { count: selectedItems.length }) }}
          </el-button>
        </slot>
      </div>

      <!-- Bảng dữ liệu chính -->
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
        <slot /> <!-- Các cột dữ liệu được định nghĩa từ component cha -->
        <el-table-column
          v-if="canDeleteItems || canEditItems || hasAddonButtons"
          :label="t('Operations')"
          fixed="right"
          :min-width="160"
          align="center"
        >
          <template #default="scope">
            <div class="flex items-center justify-center gap-2">
              <el-button v-if="canEditItems" :icon="Edit" size="small" @click.stop="editItem(scope.row.id)" />
              <el-button v-if="canDeleteItems" :icon="Delete" size="small" @click.stop="onDeleteItem(scope.row)" />
              <slot name="addonButtons" :row="scope.row" />
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- Footer: Phân trang và Nút Thêm mới -->
      <div class="flex flex-wrap items-center justify-between mt-4 gap-4">
        <el-button
          v-if="canAddItems"
          type="primary"
          :icon="Plus"
          @click="onAdd()"
        >
          {{ t("add_new") }}
        </el-button>
        
        <div v-else></div> <!-- Placeholder để giữ phân trang luôn ở bên phải -->

        <el-pagination
          v-if="data.count > 0"
          background
          :page-size="data.page_size"
          :total="data.count"
          :current-page="data.page"
          layout="total, prev, pager, next, jumper"
          @current-change="onCurrentPageChange"
        />
      </div>

      <!-- Dialogs xác nhận -->
      <el-dialog v-model="confirmDeleteDialog" :title="t('confirm_deleting')" width="30%" center>
        <span>{{ confirmDeletingMessage || t("deleting_item_confirm_default_message") }}</span>
        <template #footer>
          <el-button @click="cancelDeletingItem">{{ t("cancel") }}</el-button>
          <el-button type="primary" @click="deleteItem">{{t("yes")}}</el-button>
        </template>
      </el-dialog>
      <el-dialog v-model="confirmMultipleDeleteDialog" :title="t('confirm_deleting')" width="30%" center>
        <span>{{ confirmMultipleDeletingMessage || t("deleting_items_confirm_default_message") }}</span>
        <template #footer>
          <el-button @click="cancelMultipleDeleting">{{ t("cancel") }}</el-button>
          <el-button type="primary" @click="multipleDelete">{{ t("yes") }}</el-button>
        </template>
      </el-dialog>
      <slot name="addon-confirm-dialog" />
    </div>
  </client-only>
</template>

<script setup lang="ts" generic="S extends BaseService">
import { Plus, Delete, Edit } from "@element-plus/icons-vue";
import Excel from "@/assets/icons/excel.svg";
import Json from "@/assets/icons/json.svg";
import { ref, watch, computed, onMounted } from "vue";
import BaseService from "@/services/base";
import { ElNotification } from "element-plus";
import { toExcel } from "@/exporters/xls/xlsx";
import { toJson } from "@/exporters/json/json";
import { getErrorMessage } from "@/utils/error";

// --- PROPS DEFINITION ---
const props = defineProps<{
  service: S;
  pageSize?: number;
  multipleSelect?: boolean;
  canDeleteItems?: boolean;
  canEditItems?: boolean;
  canAddItems?: boolean;
  confirmDeletingMessage?: string;
  confirmMultipleDeletingMessage?: string;
  allowExportToExcel?: boolean;
  excelSheetName?: string;
  excelFileName?: string;
  exportFields?: object;
  allowExportToJson?: boolean;
  jsonFileName?: string;
  disableRowClick?: boolean;
  service_params?: Record<string, any>;
  hasAddonButtons?: boolean;
  params?: object; // Prop quan trọng nhất để nhận bộ lọc
  prefix?: string;
  onItemDeleted?: Function;
  onItemsDeleted?: Function;
}>();

const { t } = useI18n();
const route = useRoute();

// --- STATE ---
const loading = ref(true);
const error = ref<string | null>(null);
const data = ref({
  page: 1,
  page_size: props.pageSize || 10,
  num_pages: 0,
  count: 0,
  results: [] as any[],
});
const selectedItems = ref<any[]>([]);
const deletingItem = ref<any | null>(null);
const confirmDeleteDialog = ref(false);
const confirmMultipleDeleteDialog = ref(false);

const oauthStore = useOauthStore();
const { tokenInfo } = storeToRefs(oauthStore);

defineExpose({ reloadData: fetchData });

// --- COMPUTED ---
const query = computed(() => {
  const queryParams: Record<string, any> = {
    page: data.value.page,
    page_size: data.value.page_size,
    ...props.service_params,
    ...props.params,
  };
  Object.keys(queryParams).forEach(key => {
    if (queryParams[key] === null || queryParams[key] === undefined || queryParams[key] === '') {
      delete queryParams[key];
    }
  });
  return queryParams;
});

// --- METHODS ---
async function fetchData() {
  if (loading.value && data.value.results.length > 0) return; // Chặn gọi lại khi đang tải, trừ lần đầu
  loading.value = true;
  error.value = null;

  try {
    const response = await props.service.gets(query.value);
    const { page, num_pages, count, results } = response;
    data.value = { ...data.value, page, num_pages, count, results };
  } catch (e: any) {
    error.value = getErrorMessage(e, t('an_error_occurred_while_fetching_data'));
    data.value.results = [];
    data.value.count = 0;
  } finally {
    loading.value = false;
  }
}

function onCurrentPageChange(newPage: number) {
  data.value.page = newPage;
}

// ... các hàm xử lý sự kiện khác giữ nguyên
function onSelectionChange(selection: any[]) { selectedItems.value = selection; }
function onRowClick(row: any, column: any) {
  if (props.disableRowClick || column?.type === 'selection') return;
  const to = props.prefix ? `${route.path}/${props.prefix}/${row.id}` : `${route.path}/${row.id}`;
  navigateTo(to);
}
function editItem(id: string) {
  const path = props.prefix ? `${route.path}/${props.prefix}/${id}?edit=true` : `${route.path}/${id}?edit=true`;
  navigateTo(path);
}
function onAdd() {
  const path = props.prefix ? `${route.path}/${props.prefix}/new` : `${route.path}/new`;
  navigateTo(path);
}
function onDeleteItem(item: any) {
  deletingItem.value = item;
  confirmDeleteDialog.value = true;
}
function cancelDeletingItem() {
  confirmDeleteDialog.value = false;
  deletingItem.value = null;
}
async function deleteItem() {
  if (!deletingItem.value) return;
  try {
    await props.service.delete(deletingItem.value.id);
    ElNotification({ title: t('Success'), message: t('Item_deleted_successfully'), type: 'success' });
    await fetchData();
    props.onItemDeleted?.(deletingItem.value);
  } catch (e: any) {
    ElNotification({ title: t('Error'), message: getErrorMessage(e, t('Failed_to_delete_item')), type: 'error' });
  } finally {
    cancelDeletingItem();
  }
}
//...

// --- STEP 3: SỬA LẠI WATCHERS ĐỂ ĐẢM BẢO HOẠT ĐỘNG ỔN ĐỊNH ---
/**
 * Watcher 1: Theo dõi sự thay đổi của bộ lọc từ bên ngoài (`props.params`).
 * Khi bộ lọc thay đổi, nó sẽ tự động reset về trang 1.
 */
watch(() => props.params, () => {
  if (data.value.page !== 1) {
    // Nếu không ở trang 1, việc set page = 1 sẽ tự động kích hoạt watcher thứ hai
    data.value.page = 1; 
  } else {
    // Nếu đã ở trang 1, phải gọi fetchData thủ công để tải lại dữ liệu với bộ lọc mới
    fetchData();
  }
}, { deep: true }); // `deep` để phát hiện thay đổi bên trong object

/**
 * Watcher 2: Theo dõi sự thay đổi của trang hiện tại (`data.value.page`).
 * Khi người dùng chuyển trang, watcher này sẽ gọi lại API.
 */
watch(() => data.value.page, fetchData);

/**
 * Watcher 3: Khi token thay đổi (đăng nhập/đăng xuất), tải lại dữ liệu.
 */
watch(tokenInfo, () => {
    if (tokenInfo.value) { // Chỉ fetch khi có token
        fetchData();
    }
}, { immediate: false });

// --- LIFECYCLE HOOKS ---
onMounted(() => {
  fetchData();
});
</script>