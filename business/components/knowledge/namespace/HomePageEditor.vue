<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <ModelForm
      :collapsible="false"
      :headerNoBackground="true"
      :service="HomePageService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
      contentType="multipart/form-data"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col">
          <input v-model="scope.current.namespace_id" type="hidden" />

          <el-form-item
            v-if="scope.editing"
            prop="content"
            class="flex flex-row min-h-screen"
          >
            <HTMLEditor
              v-model="scope.current.content"
              :placeholder="$t('Start_writing')"
              :enable="scope.editing"
              :readOnly="!scope.editing"
              @change="onContentChange"
              class="min-h-full border"
            />
          </el-form-item>
          <div v-else class="min-h-[200px] p-3" v-html="scope.current.content" />
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import HomePageService from '@/services/knowledge/home-page';
import { useOauthStore } from "@/stores/oauth";
import NamespaceService from '@/services/knowledge/namespace';
import HTMLEditor from '@/components/HTMLEditor.vue';
import { useI18n } from 'vue-i18n';
import { computed, ref, onMounted } from 'vue';

const props = defineProps({
  defaultData: {
    type: Object,
    default: null
  }
});

const { t } = useI18n();
const route = useRoute();

const oauthStore = useOauthStore();
const modelForm = ref(null);

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["knowledge:pages:edit"]);
});

// Validation rules
const rules = {
  namespace_id: [
    { required: true, message: t('validate_error_required'), trigger: 'change' }
  ],
  content: [
    {
      validator: (rule, value, callback) => {
        const max_content_size = 83886080; // 80MB
        if (value) {
          const size = new Blob([value]).size;
          if (size > max_content_size) {
            callback(new Error(t('validate_error_content_max', {max: max_content_size})));
            return;
          }
        }
        callback();
      },
      trigger: 'blur'
    }
  ]
};

const onContentChange = () => {
  if (modelForm.value && modelForm.value.formRef) {
    modelForm.value.formRef.validateField('content');
  }
};

// Lifecycle
onMounted(async () => {
  NamespaceService.fetch();

});
</script>

<style scoped>
.el-card {
  border: none;
  box-shadow: none
}

:deep(.el-card__header) {
    background-color: white;
    border-bottom: none
}
</style>