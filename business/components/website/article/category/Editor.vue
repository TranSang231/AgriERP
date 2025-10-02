<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="$t('Category')" 
      :collapsible="true"
      :service="CategoryService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
			:nestedFields="nestedFields"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Name')" prop="name">
            <ShortContentEditor
              v-if="localeStore"
              :editable="scope.editing"
              v-model="scope.current.name"
              :languages="localeStore.supportedLanguages"
              :placeholder="$t('default_place_holder')"
            />
          </el-form-item>
          <el-form-item :label="t('Slug')" prop="slug">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.slug"
              :placeholder="$t('Slug')"
            />
            <span v-else>{{ scope.current.slug }}</span>
          </el-form-item>
          <el-form-item :label="t('Description')" prop="description">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.description"
              :placeholder="t('Description')"
              type="textarea"
              autosize
            />
            <span v-else>{{ scope.current.description }}</span>
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { useLocaleStore } from '@/stores/locale';
import CategoryService from "@/services/websites/category";
import { useOauthStore } from "@/stores/oauth";
import { useI18n } from "vue-i18n";
import { computed } from "vue";

const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	},
});

const { t } = useI18n();
const nestedFields = ['name', "name.translates"];
const localeStore = useLocaleStore();
const oauthStore = useOauthStore();
const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["websites:sites:edit"]);
});
</script>