<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <PaginationTable 
            :service=EmployeeService
            :pageSize="5"

            :canDeleteItems="canEdit"
            :canEditItems="canEdit"
            :canAddItems="canEdit"
            :multipleSelect="canEdit"
            :allowExportToExcel="true"
            :allowExportToJson="true"
            :searchable="true"
        >
            <el-table-column prop="first_name" :label="$t('first_name')" min-width="120" sortable/>
            <el-table-column prop="last_name" :label="$t('last_name')" min-width="120" sortable/>
            <el-table-column prop="work_mail" :label="$t('work_mail')" min-width="180"></el-table-column>
            <el-table-column prop="date_of_birth" :label="$t('date_of_birth')" min-width="180" sortable>
                <template #default="scope">
                {{ formatDate(scope.row.date_of_birth) }}
                </template>
            </el-table-column>
        </PaginationTable>
    </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import EmployeeService from '@/services/hrm/employees'
import { formatDate } from '@/utils/time'
definePageMeta({
  layout: 'hrm'
})

const oauthStore = useOauthStore();

const canEdit = computed(() => {
    return oauthStore.hasOneOfScopes(['employees:edit']);
});

</script>