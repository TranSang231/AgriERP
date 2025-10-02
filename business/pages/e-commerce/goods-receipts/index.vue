<template>
  <div class="flex flex-col w-full justify-center pt-20 px-4">
    <!-- Filter Section -->
    <div class="mb-4 p-4 border rounded-md shadow-sm bg-white">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-6 gap-y-2 items-end">

        <!-- SỬA LỖI TẠI ĐÂY: Filter by Supplier -->
        <el-form-item>
          <template #label>
            <label for="supplier-input">{{ t('Supplier') }}</label>
          </template>
          <el-input
            id="supplier-input"
            :model-value="filterData.supplier_name"
            @input="value => filterData.supplier_name = value"
            :placeholder="t('Enter_supplier_name')"
            clearable
            @keyup.enter="applyFilters"
          />
        </el-form-item>

        <!-- Filter by Reference Code -->
        <el-form-item :label="t('Reference_code')">
          <el-input
            v-model.trim="filterData.reference_code"
            :placeholder="t('Enter_reference_code')"
            clearable
            @keyup.enter="applyFilters"
          />
        </el-form-item>

        <!-- Filter by Status -->
        <el-form-item :label="t('Status')">
          <el-select
            v-model="filterData.is_applied"
            :placeholder="t('Select_status')"
            clearable
            class="w-full"
          >
            <el-option :label="t('Applied')" :value="true" />
            <el-option :label="t('Not_applied')" :value="false" />
          </el-select>
        </el-form-item>

        <!-- Filter by Date Range -->
        <el-form-item :label="t('Date_range')">
           <el-date-picker
              v-model="filterData.date_range"
              type="daterange"
              class="w-full"
              range-separator="-"
              :start-placeholder="t('start_date')"
              :end-placeholder="t('end_date')"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
        </el-form-item>
      </div>

      <!-- Filter Buttons -->
      <div class="flex justify-end mt-4 gap-2">
        <el-button @click="clearFilters">{{ t('Clear_filter') }}</el-button>
        <el-button type="primary" @click="applyFilters" :icon="Search">{{ t('Filter') }}</el-button>
      </div>
    </div>

    <!-- Data Table -->
    <PaginationTable
      :page-size="5"
      :service="GoodsReceiptService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :hasAddonButtons="true"
      :params="filterParams"
    >
      <el-table-column prop="supplier_name" :label="t('Supplier')" min-width="180" />
      <el-table-column prop="reference_code" :label="t('Reference_code')" min-width="160" />
      <el-table-column prop="date" :label="t('Date')" min-width="140">
        <template #default="scope">
          {{ utcToLocalDate(scope.row.date) }}
        </template>
      </el-table-column>
      <el-table-column prop="is_applied" :label="t('Status')" min-width="120">
        <template #default="scope">
          <el-tag :type="scope.row.is_applied ? 'success' : 'warning'">
            {{ scope.row.is_applied ? t('Applied') : t('Not_applied') }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" :label="t('Updated_at')" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.updated_at) }}
        </template>
      </el-table-column>

      <template #addonButtons="{ row }">
        <el-button v-if="canEdit && !row.is_applied" size="small" type="primary" @click.stop="onApply(row)">{{ t('Apply') }}</el-button>
      </template>
    </PaginationTable>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Search } from '@element-plus/icons-vue';
import GoodsReceiptService from "@/services/e-commerce/goods_receipt";
// Chắc chắn rằng bạn import đúng đường dẫn tới PaginationTable
import PaginationTable from "@/components/PaginationTable.vue"; 
import { formatDateTime, utcToLocalDate } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";

definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const canEdit = computed(() => oauthStore.hasOneOfScopes(["ecommerce:goods-receipts:edit", "ecommerce:orders:edit"]));

const filterData = reactive({
  supplier_name: '',
  reference_code: '',
  is_applied: null,
  date_range: [],
});

const filterParams = ref({});

const applyFilters = () => {
  const params = {};
  if (filterData.supplier_name && filterData.supplier_name.trim()) {
    params.supplier_name = filterData.supplier_name.trim();
  }
  if (filterData.reference_code && filterData.reference_code.trim()) {
    params.reference_code = filterData.reference_code.trim();
  }
  if (filterData.is_applied !== null && filterData.is_applied !== undefined) {
    params.is_applied = filterData.is_applied;
  }
  if (filterData.date_range && filterData.date_range.length === 2) {
    params.date_after = filterData.date_range[0];
    params.date_before = filterData.date_range[1];
  }
  filterParams.value = params;
};

const clearFilters = () => {
  filterData.supplier_name = '';
  filterData.reference_code = '';
  filterData.is_applied = null;
  filterData.date_range = [];
  filterParams.value = {};
};

const onApply = async (row) => {
  try {
    await GoodsReceiptService.apply(row.id);
    // Thay vì reload, chúng ta nên gọi lại hàm fetchData từ PaginationTable
    // Tuy nhiên, để đơn giản, reload tạm chấp nhận được
    location.reload();
  } catch (e) {
    // Lỗi sẽ được hiển thị bởi component con
  }
};
</script> 