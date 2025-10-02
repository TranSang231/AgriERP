<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="ArticleService"
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
      <el-table-column prop="name" :label="t('Title')" min-width="150">
        <template #default="scope">
          {{ scope.row.title?.origin }}
        </template>
      </el-table-column>
      <el-table-column prop="slug" :label="t('Slug')" min-width="180" />
      <el-table-column prop="description" :label="$t('Description')" min-width="180">
        <template #default="scope">
          {{ scope.row.description?.origin }}
        </template>
      </el-table-column>
      <el-table-column
        prop="status"
        :label="t('Status')"
      >
        <template
          v-if="constantsStore && constantsStore.publishingStatuses"
          #default="scope"
        >
          {{ constantsStore.publishingStatus(scope.row.status).description }}
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
import ArticleService from "@/services/websites/article";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useConstantsStore } from '@/stores/constants';
import { useOauthStore } from "@/stores/oauth";
import ConstantsService from '@/services/constants';
definePageMeta({
  layout: "websites",
});

const { t } = useI18n();
const constantsStore = useConstantsStore();

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["websites:articles:edit"]))

onMounted(() => {
    ConstantsService.fetch("publishing_statuses");
});
</script>
