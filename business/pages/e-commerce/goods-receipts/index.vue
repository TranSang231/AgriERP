<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="GoodsReceiptService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
      :hasAddonButtons="true"
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
        <el-button 
          v-if="canEdit && !row.is_applied" 
          size="small" 
          type="primary" 
          @click.stop="onApply(row)"
        >
          {{ t('Apply') }}
        </el-button>
        <el-button 
          v-if="canEdit && row.is_applied" 
          size="small" 
          type="warning" 
          @click.stop="onUnapply(row)"
        >
          {{ t('Unapply') }}
        </el-button>
      </template>
    </PaginationTable>
  </div>
</template>

<script setup>
import GoodsReceiptService from "@/services/e-commerce/goods_receipt";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime, utcToLocalDate } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
import { ElMessageBox } from "element-plus";

definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const canEdit = computed(() => oauthStore.hasOneOfScopes(["ecommerce:goods-receipts:edit", "ecommerce:orders:edit"]));

const onApply = async (row) => {
  try {
    await GoodsReceiptService.apply(row.id);
    location.reload();
  } catch (e) {
    // noop: PaginationTable shows error
  }
};

const onUnapply = async (row) => {
  try {
    await ElMessageBox.confirm(
      t('Unapply_goods_receipt_confirm_message', 'This will reverse all stock changes made by this receipt. Are you sure you want to continue?'),
      t('Confirm_unapply', 'Confirm Unapply'),
      {
        confirmButtonText: t('Yes'),
        cancelButtonText: t('No'),
        type: 'warning',
      }
    );
    
    await GoodsReceiptService.unapply(row.id);
    location.reload();
  } catch (e) {
    if (e === 'cancel') {
      // User cancelled
      return;
    }
    // noop: PaginationTable shows error
  }
};
</script>


