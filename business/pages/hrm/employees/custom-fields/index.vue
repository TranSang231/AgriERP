<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <EditableTable 
            :service=EmployeeCustomFieldService
            :canDeleteItems="true"
            :canEditItems="true"
            :canAddItems="true"
            :multipleSelect="true"
            :allowExportToExcel="true"
            :allowExportToJson="true"
            :searchable="true"
            :itemTemplate="{
                name: null,
                data_type: 'CharField',
                max_length: 20
            }"
            :filter="filter"
        >
            <el-table-column prop="name" :label="t('Name')" min-width="120" sortable>
                <template #default="scope">
                    <el-input
                        v-model="scope.row.name"
                        placeholder="Name"
                    />
                </template>
            </el-table-column>
            <el-table-column prop="data_type" :label="$t('data_type')" min-width="120" sortable>
                <template #default="scope">
                    <el-select v-model="scope.row.data_type" :placeholder="$t('select_data_type')">
                        <el-option
                            v-for="item in dataTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="max_length" :label="t('max_length')" min-width="178">
                <template #default="scope">
                    <el-input-number
                        v-if="scope.row.data_type == 'CharField'"
                        v-model="scope.row.max_length"
                        :min="1"
                        :max="256"
                    />
                    <span v-else></span>
                </template>
            </el-table-column>
            <el-table-column prop="updated_at" :label="t('Updated_at')" min-width="180" sortable>
                <template #default="scope">
                {{ formatDateTime(scope.row.updated_at) }}
                </template>
            </el-table-column>
        </EditableTable>
    </div>
</template>

<script setup lang="ts">
import EmployeeCustomFieldService from '@/services/hrm/employee-custom-field'
import { formatDateTime } from '@/utils/time'
import { DATA_TYPES } from '@/constants/data-type'
const { t } = useI18n();

const dataTypes = DATA_TYPES.map(i => ({ value: i, label: t(i) }));
const filter = (o: any, keyword: string) => {
    if (!keyword || keyword.trim().length === 0) {
        return true;
    }
    const keywordLowerCase = keyword.trim().toLowerCase()
    return o.name.trim().toLowerCase().includes(keywordLowerCase);

}

definePageMeta({
  layout: 'hrm'
})
</script>