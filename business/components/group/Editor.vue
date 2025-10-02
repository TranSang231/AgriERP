<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <el-button :icon="Back" class="self-start" @click="back()">{{ $t('back') }}</el-button>
        <ModelForm v-if="canEdit || (!defaultData && canView)" :title="$t('group_title')" :collapsible="true"
            :service="GroupService" :rules="rules" :default="defaultData" :editable="canEdit"
            contentType="multipart/form-data">
            <template #default="scope">
                <div class="flex flex-col gap-2">
                    <el-form-item :label="$t('Name')" prop="name">
                        <el-input v-if="scope.editing" v-model="scope.current.name"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.name }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('Email')" prop="email">
                        <el-input v-if="scope.editing" v-model="scope.current.email"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.email }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('Address')" prop="address">
                        <el-input v-if="scope.editing" v-model="scope.current.address"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.address }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('Phone')" prop="phone">
                        <el-input v-if="scope.editing" v-model="scope.current.phone"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.phone }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('manager')" prop="manager_id">
                        <el-select v-if="scope.editing" collapse-tags value-key="id" v-model="scope.current.manager_id"
                            :placeholder="$t('pick_a_people')">
                            <el-option v-for="item in employeesStore.allEmployees" :key="item.id"
                                :label="item.first_name + ' ' + item.last_name" :value="item.id" />
                        </el-select>
                        <span v-else>{{ scope.current.manager.first_name + ' ' + scope.current.manager.last_name
                            }}</span>
                    </el-form-item>
                </div>
            </template>
        </ModelForm>
        <span v-else class="text-center">{{ $t('dont_have_permission') }}</span>
    </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import { Back } from '@element-plus/icons-vue'
import GroupService from '@/services/group'
import { useEmployeesStore } from '@/stores/business/employee';

// Extract the office_id from the route parameters
const route = useRoute();
const props = defineProps({
    defaultData: {
        type: Object,
        default: null
    },
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const employeesStore = useEmployeesStore();

const canEdit = computed(() => {
    return oauthStore.hasOneOfScopes(['offices:edit']);
});
const canView = computed(() => {
    return oauthStore.hasOneOfScopes(['offices:view']);
});

const rules = {
    name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 50, message: t('validate_error_min_max', { min: 1, max: 50 }), trigger: 'blur' },
    ],
    email: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { type: 'email', message: 'Invalid email format', trigger: ['blur', 'change'] },
    ],
    address: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 100, message: t('validate_error_min_max', { min: 1, max: 255 }), trigger: 'blur' },
    ],
    phone: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 20, message: t('validate_error_min_max', { min: 1, max: 11 }), trigger: 'blur' },
    ]
};

onMounted(async () => {
    GroupService.fetch()

})

const back = () => {
    navigateTo('/hrm/offices')
}
</script>
<style scoped>
.work-session-container {
    display: flex;
    flex-direction: row;
    gap: 20px;
    /* Space between rows */
}
</style>