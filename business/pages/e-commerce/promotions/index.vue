<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="PromotionService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
      <el-table-column prop="name" :label="t('Name')" min-width="150"/>
      <el-table-column prop="type" :label="t('Type')" min-width="120"/>
      <!-- <el-table-column prop="discount" :label="t('Discount')" min-width="120">
        <template #default="scope">
          <span v-if="scope.row.type === 'voucher'">{{ scope.row.discount }}</span>
          <span v-else>-</span>
        </template>
      </el-table-column> -->
      <el-table-column
        prop="start"
        :label="t('Start')"
        min-width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.start) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="end"
        :label="t('End')"
        min-width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.end) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="created_at"
        :label="t('Created_at')"
        min-width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="updated_at"
        :label="t('Updated_at')"
        min-width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.updated_at) }}
        </template>
      </el-table-column>
    </PaginationTable>
  </div>
</template>

<script setup>
import PromotionService from "@/services/e-commerce/promotion";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:promotions:edit"]));
</script>
