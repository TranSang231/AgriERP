<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="t('Namespaces')"
      :service="NamespaceService"
      lookupField="namespaceId"
      :nestedFields="['member_ids']"
      :rules="rules"
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
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import NamespaceService from '@/services/knowledge/namespace';
import { useI18n } from 'vue-i18n';
import { computed, ref } from 'vue';

const props = defineProps({
  defaultData: {
    type: Object,
    default: null
  }
});

const { t } = useI18n();
const modelForm = ref(null);
const employeeStore = useEmployeesStore();

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  slug: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

</script>