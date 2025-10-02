<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" :historyBack="historyBack"/>
    <ModelForm
      :title="t('Name')" 
      :collapsible="true"
      :service="IntentService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="t('Variable_name_placeholder')"
            />
            <span v-else>{{ scope.current.name }}</span>
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup lang="ts">
import IntentService from "@/services/va/intent";
import { useOauthStore } from "@/stores/oauth";
import { useI18n } from "vue-i18n";
import { computed } from "vue";

const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	},
  pathPrefix: {
    type: String,
    default: null,
  },
  historyBack: {
    type: Boolean,
    default: false
  }
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
});
</script>