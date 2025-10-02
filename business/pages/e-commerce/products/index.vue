<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="ProductService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
      <el-table-column prop="thumbnail" :label="t('Thumbnail')" min-width="86">
        <template #default="scope">
          <el-image
            v-if="scope.row.thumbnail"
            :src="scope.row.thumbnail"
            fit="fill"
            style="width: 60px; height: 60px"
          />
        </template>
      </el-table-column>
      <el-table-column prop="name" :label="t('Name')" min-width="150">
        <template #default="scope">
          {{ scope.row.name?.origin }}
        </template>
      </el-table-column>
      <el-table-column prop="unit" :label="$t('Unit')" min-width="180">
        <template #default="scope">
          {{ scope.row.unit?.origin }}
        </template>
      </el-table-column>
      <el-table-column prop="price" :label="$t('Price')" min-width="180" />
      <el-table-column prop="categories" :label="$t('Categories')" min-width="180">
        <template #default="scope">
          <el-tag
            type="primary"
            v-for="category in scope.row.categories"
          >
            {{ category.name? category.name.origin : '' }}
          </el-tag>
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
import ProductService from "@/services/e-commerce/product";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:products:edit"]));
</script>
