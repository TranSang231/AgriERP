<template>
    <div class="flex flex-col justify-center pt-20 px-5 gap-2">
        <BackButton />
        <ModelForm
            v-if="canEdit || (!defaultData && canView)"
            :title="t('role_title')" 
            :collapsible="true"
            :service="RoleService"
            :default="defaultData"
            :editable="canEdit"
            :rules="rules"
        >
            <template #default="scope">
                <div class="flex flex-col gap-2">
                    <el-form-item :label="t('Name')" prop="name">
                        <el-input v-if="scope.editing"
                            v-model="scope.current.name"
                            :placeholder="t('default_place_holder')"
                        />
                        <span v-else>{{scope.current.name}}</span>
                    </el-form-item>
                    <el-form-item :label="t('Description')" prop="description">
                        <el-input v-if="scope.editing"
                            v-model="scope.current.description"
                            :placeholder="t('default_place_holder')"
                        />
                        <span v-else>{{scope.current.description}}</span>
                    </el-form-item>
                    <div class="flex flex-col gap-2">
                        <span class="font-bold">{{t('Permissions')}}:</span>
                        <ScopeSelector v-if="scope.current"
                            v-model="scope.current.scope"
                            :scopes="oauthStore.peopleGrantableScopes"
                            :defaultScopes="oauthStore.defaultScopes"
                            :editable="scope.editing"
                        />
                    </div>
                </div>
            </template>
        </ModelForm>     
    </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import RoleService from '@/services/roles';
import OAuthService from '@/services/oauth';
const props = defineProps({
    defaultData: {
        type: Object,
        default: null
    }
});
const { t } = useI18n();
const oauthStore = useOauthStore();

const canEdit = computed(() => {
    return oauthStore.hasOneOfScopes(['roles:edit']);
});
const canView = computed(() => {
    return oauthStore.hasOneOfScopes(['roles:view']);
});

const overrideEmptyData = computed (() => {
    const scopes = oauthStore.defaultScopes;
    if (scopes && scopes.length > 0) {
        return {
            scope: scopes.join(" ")
        }
    }
    return null;
});

const fetchData = async () => {
    OAuthService.fetchScopes();
}

onMounted(() => {
    fetchData();
})

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' },
    { min: 1, max: 120, message: t('validate_error_min_max', {min: 1, max: 120}), trigger: 'blur' },
  ],
  description: [
    { max: 200, message: t('validate_error_max', {max: 200}), trigger: 'blur' },
  ]
};

</script>
