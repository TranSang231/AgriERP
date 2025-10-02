<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2 md:flex-1">
        <PaginationTable 
            :pageSize="5"
            :service=UnitTypesService
            :canDeleteItems="true"
            :canEditItems="true"
            :canAddItems="true"
            :multipleSelect="true"
            :allowExportToExcel="true"
            :allowExportToJson="true"
            :confirmDeletingMessage="$t('deleting_unit_type_confirm_message')"
            :confirmMultipleDeletingMessage="$t('deleting_unit_types_confirm_message')"
            :searchable="true"
        >
            <el-table-column prop="name" :label="$t('Name')" min-width="150" />
            <el-table-column prop="description" :label="$t('Description')" min-width="120" />
            <el-table-column prop="updated_at" :label="$t('Updated_at')" min-width="180" >
                <template #default="scope">
                {{ formatDate(scope.row.updated_at) }}
                </template>
            </el-table-column>
        </PaginationTable>
    </div>
</template>

<script setup lang="ts">
import UnitTypesService from '~/services/organization/unit-types'
import { formatDate } from '@/utils/time'
definePageMeta({
  layout: 'hrm'
})

</script>