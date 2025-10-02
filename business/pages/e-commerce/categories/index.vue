<template>
  <div class="flex flex-row justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="ProductCategoryService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
      <el-table-column prop="name" :label="t('Name')" min-width="150">
        <template #default="scope">
          {{ scope.row.name.origin }}
        </template>
      </el-table-column>
      <el-table-column prop="slug" :label="t('Slug')" min-width="180" />
      <el-table-column
        prop="description"
        :label="$t('Description')"
        min-width="180"
      />
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
import ProductCategoryService from "@/services/e-commerce/category";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:products:edit"]))
</script>
