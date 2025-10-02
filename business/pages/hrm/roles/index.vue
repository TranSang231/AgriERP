<template>
    <div class="flex flex-col justify-center pt-20 px-5">
        <PaginationTable 
            :pageSize="5"
            :service=RoleService
            :canDeleteItems="true"
            :canEditItems="true"
            :canAddItems="true"
            :multipleSelect="true"
            :allowExportToExcel="true"
            :allowExportToJson="true"
            :confirmDeletingMessage="t('deleting_role_confirm_message')"
            :confirmMultipleDeletingMessage="t('deleting_roles_confirm_message')"
            :searchable="true"
        >
            <el-table-column prop="name" label="Name" min-width="150"/>
            <el-table-column prop="description" :label="t('Description')" min-width="180" />
            <el-table-column prop="updated_at" :label="t('Updated_at')" min-width="180">
                <template #default="scope">
                {{ formatDateTime(scope.row.updated_at) }}
                </template>
            </el-table-column>
        </PaginationTable>
    </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import RoleService from '@/services/roles'
import { formatDateTime } from '@/utils/time'

const { t } = useI18n();
definePageMeta({
  layout: 'hrm'
})

const oauthStore = useOauthStore();

const canEdit = computed(() => {
	return oauthStore.hasOneOfScopes(['roles:edit']);
});
</script>