<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <BackButton />
        <ModelForm v-if="canEdit || (!defaultData && canView)" :title="$t('employee_title')" :collapsible="true"
            :service="EmployeeService" :rules="rules" :default="defaultData" :nestedFields="['additional_information']"
            :editable="canEdit" :overrideIfFieldNullOrEmpty="overrideEmptyData" contentType="multipart/form-data">
            <template #default="scope">
                <div class="flex flex-col gap-2">
                    <el-form-item prop="avatar" class="flex flex-col self-center">
                        <ImagePicker
                            v-model="scope.current.avatar"
                            :editable="scope.editing"
                            :size="80"
                            shape="circle"
                        />
                    </el-form-item>
                    <el-button v-if="scope.current.id && !scope.current.user && !scope.current.user_id"
                        class="self-center mb-5" :icon="Invite" @click="sendInvitation()">
                        {{ $t('resend_invitation') }}
                    </el-button>
                    <el-form-item :label="$t('first_name')" prop="first_name">
                        <el-input v-if="scope.editing" v-model="scope.current.first_name"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.first_name }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('last_name')" prop="last_name">
                        <el-input v-if="scope.editing" v-model="scope.current.last_name"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.last_name }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('Gender')" prop="gender">
                        <el-select v-if="scope.editing" v-model="scope.current.gender"
                            :placeholder="$t('pick_a_gender')">
                            <el-option v-for="item in genders" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                        <span v-else>
                            {{ genders.find(o => o.value === scope.current.gender).label }}
                        </span>
                    </el-form-item>
                    <el-form-item :label="$t('work_mail')" prop="work_mail">
                        <el-input v-if="scope.editing" v-model="scope.current.work_mail"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.work_mail }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('personal_mail')" prop="personal_mail">
                        <el-input v-if="scope.editing" v-model="scope.current.personal_mail"
                            :placeholder="$t('default_place_holder')" />
                        <span v-else>{{ scope.current.personal_mail }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('date_of_birth')" prop="date_of_birth">
                        <el-date-picker v-if="scope.editing" v-model="scope.current.date_of_birth" type="date"
                            placeholder="Pick a day" :format="dateFormat" :value-format="dateFormat" />
                        <span v-else>{{ scope.current.date_of_birth }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('join_date')" prop="join_date">
                        <el-date-picker v-if="scope.editing" v-model="scope.current.join_date" type="date"
                            :placeholder="$t('pick_a_day')" :format="dateFormat" :value-format="dateFormat" />
                        <span v-else>{{ scope.current.join_date }}</span>
                    </el-form-item>
                    <el-form-item :label="$t('Roles')" prop="roles">
                        <el-select v-if="scope.editing" multiple collapse-tags value-key="id"
                            v-model="scope.current.roles" :placeholder="$t('pick_roles')">
                            <el-option v-for="item in rolesStore.allRoles" :key="item.id" :label="item.name"
                                :value="item" />
                        </el-select>
                        <span v-else>
                            {{ scope.current.roles.map(role => role.name).join(', ') }}
                        </span>
                    </el-form-item>
                    <el-form-item :label="$t('Status')" prop="status">
                        <el-select v-if="scope.editing" v-model="scope.current.status"
                            :placeholder="$t('pick_a_status')">
                            <el-option v-for="item in accountStatus" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                        <span v-else>
                            {{ accountStatus.find(o => o.value === scope.current.status).value }}
                        </span>
                    </el-form-item>
                    <el-form-item v-for="item in scope.current.additional_information" :key="item.field.id"
                        :label="item.field.name" prop="additional_information">
                        <CustomFieldInput v-if="scope.editing" v-model="item.value" :dataType="item.field.data_type" />
                        <span v-else>{{ item.value }}</span>
                    </el-form-item>
                </div>
            </template>
        </ModelForm>
        <span v-else class="text-center">{{ $t('dont_have_permission') }}</span>
    </div>
</template>

<script setup lang="ts">
import Invite from '@/assets/icons/invite.svg'
import { FORMAT, formatDate } from '@/utils/time';
import { useOauthStore } from '@/stores/oauth';
import { useRolesStore } from '@/stores/oauth/roles';
import { useCustomFieldsStore } from '@/stores/business/custom-fields';
import EmployeeService from '@/services/hrm/employees'
import EmployeeCustomFieldService from '@/services/hrm/employee-custom-field'
import RoleService from '@/services/roles'
import { ACCOUNT_STATTUS } from '@/constants/account-status'
import { GENDERS } from '@/constants/gender'

const props = defineProps({
    defaultData: {
        type: Object,
        default: null
    },
});

const dateFormat = FORMAT.DATE;
const { t } = useI18n();
const route = useRoute();

const genders = GENDERS.map(i => ({ value: i, label: t(i) }));
const accountStatus = Object.entries(ACCOUNT_STATTUS).map(([k, v]) => ({ value: v, label: t(k) }));

const rolesStore = useRolesStore();
const customFieldStore = useCustomFieldsStore();
const oauthStore = useOauthStore();
const canEdit = computed(() => {
    return oauthStore.hasOneOfScopes(['employees:edit']);
});
const canView = computed(() => {
    return oauthStore.hasOneOfScopes(['employees:view']);
});
const roleOptions = computed(() => {
    const roles = rolesStore.allRoles;
    if (!roles) {
        return [];
    }
    return roles
});

const overrideEmptyData = computed(() => {
    const fields = customFieldStore.allCustomFields;
    let additional_information = [] as any;
    if (fields) {
        fields.forEach((f: any) => {
            let item = {
                field: f,
                value: null
            } as any
            if (route.params.id) {
                item = { ...item, employee_id: route.params.id }
            }
            additional_information = [
                ...additional_information,
                item
            ];
        });
    }
    return {
        additional_information
    };
});

const fetchData = async () => {
    RoleService.fetch();
    EmployeeCustomFieldService.fetch();
};

const sendInvitation = async () => {
    if (route.params.id) {
        EmployeeService.sendInvitation(route.params.id)
    }
}

const rules = {
    first_name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 20, message: t('validate_error_min_max', { min: 1, max: 20 }), trigger: 'blur' },
    ],
    last_name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 30, message: t('validate_error_min_max', { min: 1, max: 30 }), trigger: 'blur' },
    ],
    work_mail: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { type: 'email', message: 'Invalid email format', trigger: ['blur', 'change'] },
    ],
    personal_mail: [
        { type: 'email', message: 'Invalid email format', trigger: ['blur', 'change'] },
    ]
};

onMounted(() => {
    fetchData();
})

</script>
