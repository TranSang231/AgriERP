<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="NamespaceService"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
       <el-table-column prop="logo" :label="t('Logo')" min-width="100">
        <template #default="scope">
          <el-image
            v-if="scope.row.logo"
            :src="scope.row.logo"
            :alt="t('Logo')"
            style="width: 60px; height: 60px"
          />
        </template>
      </el-table-column> 
      <el-table-column prop="name" :label="t('Name')" min-width="150" />
      <el-table-column prop="slug" :label="t('Slug')" min-width="180" />
      <el-table-column prop="description" :label="t('Description')" min-width="180" />
      <el-table-column prop="access" :label="t('Access_mode')">
            <template v-if="constantsStore && constantsStore.accessModes" #default="scope">
              {{ constantsStore.accessMode(scope.row.access).description }}
            </template>
          </el-table-column>
      <el-table-column prop="owner" label="Owner" min-width="150">
        <template #default="scope">
            {{ scope.row.owner ? `${scope.row.owner.first_name} ${scope.row.owner.last_name}` : 'N/A' }}
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

<script setup lang="ts">
import NamespaceService from "@/services/knowledge/namespace";
import ConstantsService from "@/services/constants";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
import { useI18n } from 'vue-i18n';
import { computed, onMounted } from 'vue';
import { useConstantsStore } from '@/stores/constants';
definePageMeta({
    layout: 'knowledge'
})

const { t } = useI18n();
const constantsStore = useConstantsStore();

const fetchData = () => {
  ConstantsService.fetch("access_modes");
};
onMounted(() => {
  fetchData();
});
</script>