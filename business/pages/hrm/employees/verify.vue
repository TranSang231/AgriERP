<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
    
        <span v-if="!tokenPayload">
            {{ $t('invalid_token') }}
        </span>
        <div v-if="tokenPayload">
            <p class="self-center text-center font-bold mb-6">{{ $t('welcome_to_amoz') }}</p>
            <span class="italic">{{ $t('confirm_employee_explain') }}</span>
        </div>
        <p v-if="error" class="self-center text-red-800">{{error}}</p>
        <el-form v-if="tokenPayload"
            ref="formRef"
            label-width="auto"
            label-position="right"
            label-suffix=":"
            :model="formData"
            :rules="user_id ? [] :rules"
            class="self-center"
        >
            <el-form-item :label="$t('Email')" prop="email">
                <span>{{formData.email}}</span>
            </el-form-item>
            <el-form-item :label="$t('first_name')" prop="first_name">
                <span v-if="user_id">{{formData.first_name}}</span>
                <el-input
                    v-else
                    v-model="formData.first_name"
                    :placeholder="$t('default_place_holder')"
                />
                
            </el-form-item>
            <el-form-item  :label="$t('last_name')" prop="last_name">
                <span v-if="user_id">{{formData.last_name}}</span>
                <el-input v-else
                    v-model="formData.last_name"
                    :placeholder="$t('default_place_holder')"
                />
            </el-form-item>
            <el-form-item v-if="!user_id" :label="$t('password')" prop="password">
                <el-input
                    type="password"
                    show-password
                    v-model="formData.password"
                    :placeholder="$t('default_place_holder')"
                />
            </el-form-item>
            <el-form-item v-if="!user_id" :label="$t('retype_password')" prop="retype_password">
                <el-input
                    type="password"
                    show-password
                    v-model="formData.retype_password"
                    :placeholder="$t('default_place_holder')"
                />
            </el-form-item>
        </el-form>
        <el-button class="self-center mb-6" @click="submit()">Confirm</el-button>
    </div>
</template>

<script setup lang="ts">
import jwtDecode from "jwt-decode";
import { useOauthStore } from '@/stores/oauth';
import EmployeeService from '@/services/hrm/employees'
import { getErrorMessage } from '@/utils/error';

definePageMeta({
  layout: 'anonymous'
})

const oauthStore = useOauthStore();
const route = useRoute();
const { t } = useI18n();
const formRef = ref(null);
const { token } = route.query;
const tokenPayload = token ? jwtDecode (token) : null;
const email = tokenPayload ? tokenPayload.email : null;
const first_name = tokenPayload ? tokenPayload.first_name : null;
const last_name = tokenPayload ? tokenPayload.last_name : null;
const employee_id = tokenPayload ? tokenPayload.employee_id : null;
const user_id = tokenPayload ? tokenPayload.user_id : null;

const formData = ref({
    token,
    email,
    first_name,
    last_name,
    employee_id,
    password: null,
    retype_password: null,
});
const error = ref(null);

const submit = () => {
    if (!formRef.value) {
        return;
    }

    formRef.value.validate(async (valid, fields) => {
        if(!valid) {
            return;
        }
        let { password, retype_password, ...data } = formData.value;
        if (user_id) {
            data = { ...data, user_id };
        } else {
            data = { ...data, password };
        }
        error.value = null;
        EmployeeService.verify(data)
            .then((response) => {
                oauthStore.setFirstLogin(true);
                navigateTo(`/`);
            })
            .catch ((e) => {
                error.value = getErrorMessage(e, t('an_error_occurred'));
            });
    });
};

const validateReTypePassword = (rule, value, callback) => {
    if (formData.value.password && formData.value.password.length > 0 && formData.value.password !== value) {
        callback(new Error(t('password_not_same')));
    } else {
        callback();
    }
};

const rules = {
    first_name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 20, message: t('validate_error_min_max', {min: 1, max: 20}), trigger: 'blur' },
    ],
    last_name: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 1, max: 30, message: t('validate_error_min_max', {min: 1, max: 30}), trigger: 'blur' },
    ],
    password: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { min: 6, max: 20, message: t('validate_error_min_max', {min: 1, max: 20}), trigger: 'blur' },
    ],
    retype_password: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { validator: validateReTypePassword, trigger: 'blur'},
    ],
};

onMounted(() => {
    oauthStore.$reset();
})
</script>