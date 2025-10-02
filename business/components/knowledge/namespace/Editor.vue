<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="t('Namespace')"
      :collapsible="true"
      :service="NamespaceService"
      lookupField="namespaceId"
      :nestedFields="['member_ids']"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
      contentType="multipart/form-data"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Logo')" prop="logo">
            <ImagePicker
              v-model="scope.current.logo"
              :editable="scope.editing"
              :size="120"
            />
          </el-form-item>
          <el-form-item :label="t('Name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="t('Name')"
            />
            <span v-else>{{ scope.current.name || 'N/A' }}</span>
          </el-form-item>
          <el-form-item :label="t('Slug')" prop="slug">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.slug"
              :placeholder="t('Slug')"
            />
            <span v-else>{{ scope.current.slug || 'N/A' }}</span>
          </el-form-item>
          <el-form-item :label="t('Description')" prop="description">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.description"
              :placeholder="t('Description')"
              type="textarea"
            />
            <span v-else>{{ scope.current.description || 'N/A' }}</span>
          </el-form-item>
          <el-form-item
            v-if="constantsStore && constantsStore.accessModes"
            :label="t('Access')"
            prop="access"
          >
            <el-select
              v-if="scope.editing"
              v-model="scope.current.access"
              :placeholder="t('pick_access')"
            >
              <el-option
                v-for="mode in constantsStore.accessModes"
                :key="mode.value"
                :label="mode.description"
                :value="mode.value"
              />
            </el-select>
            <span v-else>
              {{ constantsStore.assesModeDescription(scope.current.access) }}
            </span>
          </el-form-item>
          <el-form-item 
            v-if="scope.current.access === 0 && employeeStore.allEmployees"
            :label="t('Members')"
            prop="members"
          >
            <el-select
              v-model="scope.current.member_ids"
              multiple
              :placeholder="$t('Select members')"
              :disabled="!scope.editing"
            >
              <el-option
                v-for="employee in employeeStore.allEmployees"
                :key="employee.id"
                :label="employee.first_name && employee.last_name ? `${employee.first_name} ${employee.last_name}` : 'No name'"
                :value="employee.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item
            v-if="users"
            :label="t('Owner')"
            prop="owner_id"
          >
            <el-select
              v-model="scope.current.owner_id"
              :placeholder="t('pick_a_people')"
              :disabled="!scope.editing"
            >
              <el-option
                v-for="user in users"
                :key="user.id"
                :label="user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : 'No name'"
                :value="user.id"
              />
            </el-select>
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { useOauthStore } from "@/stores/oauth";
import { useConstantsStore } from '@/stores/constants';
import ConstantsService from "@/services/constants";
import NamespaceService from '@/services/knowledge/namespace';
import { useI18n } from 'vue-i18n';
import { computed, ref, onMounted } from 'vue';
import EmployeeService from '@/services/hrm/employees'; 

const props = defineProps({
  defaultData: {
    type: Object,
    default: null
  }
});

const { t } = useI18n();
const modelForm = ref(null);
const oauthStore = useOauthStore();
const constantsStore = useConstantsStore();
const employeeStore = useEmployeesStore();


const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["knowledge:namespaces:edit"]);
});

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  slug: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};


const users = computed(() => {
  if(!employeeStore || !employeeStore.allEmployees)
  {
    return [];
  }
  return employeeStore.allEmployees.map((o) => o.user);
})

onMounted(async () => {
  ConstantsService.fetch("access_modes");
  EmployeeService.fetch();
});

</script>