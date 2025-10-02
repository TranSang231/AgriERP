<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <BackButton />
        <ModelForm v-if="canEdit || (!defaultData && canView)" :title="t('unit_title')" :collapsible="true"
            :service="UnitService" :default="defaultData" :editable="canEdit" :rules="rules">
            <template #default="scope">
                <div class="flex flex-col gap-2">
                    <el-form-item :label="t('Name')" prop="name">
                        <el-input v-if="scope.editing" v-model="scope.current.name"
                            :placeholder="t('default_place_holder')" />
                        <span v-else>{{ scope.current.name }}</span>
                    </el-form-item>
                    <el-form-item prop="type_id" class="col-12 col-md-3 mt-1" :label="t('unit_type_title')">
                        <el-select v-if="scope.editing" v-model="scope.current.type_id" filterable
                            placeholder="Unit type" value-key="name">
                            <el-option v-for="t in allUnitTypes" :key="t.id" :label="t.name" :value="t.id" />
                        </el-select>
                        <span v-else>{{ scope.current.type.name }}</span>
                    </el-form-item>
                    <el-form-item :label="t('manager')" prop="manager_id">
                        <el-select v-if="scope.editing" collapse-tags value-key="id" v-model="scope.current.manager_id"
                            :placeholder="t('pick_a_people')">
                            <el-option v-for="item in employeesStore.allEmployees" :key="item.id"
                                :label="item.first_name + ' ' + item.last_name" :value="item.id" />
                        </el-select>
                        <span v-else>{{ scope.current.manager.first_name + ' ' + scope.current.manager.last_name
                            }}</span>
                    </el-form-item>

                    <el-form-item :label="t('members')" prop="members">
                        <el-table :data="scope.current.members">
                            <el-table-column prop="first_name" :label="t('first_name')" min-width="120" sortable />
                            <el-table-column prop="last_name" :label="t('last_name')" min-width="120" sortable />
                            <el-table-column prop="work_mail" :label="t('work_mail')"
                                min-width="180"></el-table-column>
                            <el-table-column prop="date_of_birth" :label="t('date_of_birth')" min-width="180" sortable>
                                <template #default="scope">
                                    {{ formatDate(scope.row.date_of_birth) }}
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-form-item>
                </div>
            </template>
        </ModelForm>
    </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import UnitService from '~/services/organization/units';
import { useUnitTypesStore } from "@/stores/organization/unit-types";
import UnitTypesService from '~/services/organization/unit-types';
import EmployeeService from '@/services/hrm/employees';
import { useEmployeesStore } from '@/stores/business/employee';

const props = defineProps({
    defaultData: {
        type: Object,
        default: null
    },
});
const { t } = useI18n();
const oauthStore = useOauthStore();
const unitTypeStore = useUnitTypesStore();
const employeesStore = useEmployeesStore();

const canEdit = computed(() => {
    return oauthStore.hasOneOfScopes(['organization:edit-business']);
});
const canView = computed(() => {
    return oauthStore.hasOneOfScopes(['organization:view-business']);
});

const overrideEmptyData = computed(() => {
    const scopes = oauthStore.defaultScopes;
    if (scopes && scopes.length > 0) {
        return {
            scope: scopes.join(" ")
        }
    }
    return null;
});

const allUnitTypes = computed(() => {
    return unitTypeStore.allUnitTypes;
})


onMounted(() => {
    UnitTypesService.fetch();
    EmployeeService.fetch();
})

const rules = {
    name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 120, message: t('validate_error_min_max', { min: 1, max: 120 }), trigger: 'blur' },
    ],
    description: [
        { max: 200, message: t('validate_error_max', { max: 200 }), trigger: 'blur' },
    ]
};

</script>
