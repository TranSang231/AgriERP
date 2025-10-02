<template>
  <div class="h-screen flex justify-center pt-20">
    <PaginationTable
      :pageSize="5"
      :canDeleteItems="canEdit"
			:canEditItems="canEdit"	
			:canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
      :service="SiteService"
    >
      <el-table-column
        prop="domain_name"
        :label="t('Domain')"
        min-width="120"
      />
      <el-table-column
        prop="title"
        :label="t('Title')"
        min-width="200"
      >
        <template #default="scope">
          {{ scope.row.title?.origin }}
        </template>
      </el-table-column>
      <el-table-column
        prop="description"
        :label="t('Description')"
      >
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
      <el-table-column prop="updated_at" :label="t('Updated_at')" min-width="180">
        <template #default="scope">
          {{ utcToLocalDateTime(scope.row.updated_at) }}
        </template>
      </el-table-column>
    </PaginationTable>
  </div>
</template>

<script setup lang="ts">
import { utcToLocalDateTime } from "@/utils/time";
import { useOauthStore } from '@/stores/oauth';
import { useConstantsStore } from '@/stores/constants';
import ConstantsService from '@/services/constants';
import SiteService from "@/services/websites/site";
definePageMeta({
  layout: "websites",
});

const { t } = useI18n();

const oauthStore = useOauthStore();
const constantsStore = useConstantsStore();

const canEdit = computed(() => {
	return oauthStore.hasOneOfScopes(["websites:sites:edit"]);
});

onMounted(() => {
    ConstantsService.fetch("publishing_statuses");
});

</script>
