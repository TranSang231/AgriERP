<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <ModelForm
      :collapsible="false"
      :headerNoBackground="true"
      :service="PageService"
      title=" "
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
      contentType="multipart/form-data"
      ref="modelForm"
      :customCreateResponseParser="customCreateResponseParser"
    >
      <template #title="scope">
        <el-form-item prop="title" class="w-full" v-if="scope.editing">
          <el-input
            v-model="scope.current.title"
            :placeholder="t('Title')"
            class="text-lg font-bold"
            @input="onTitleChange(scope.current)"
          />
        </el-form-item>
        <span v-else class="text-lg font-bold">
          {{ scope.current ? scope.current.title: '' }}
        </span>
      </template>
      <template #default="scope">
        <div class="flex flex-col">
          <input v-model="scope.current.slug" type="hidden" />
          <input v-model="scope.current.namespace_id" type="hidden" />
          <input v-model="scope.current.parent_id" type="hidden" />

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
import { isValidSlug } from '@/utils/validator';
import PageService from '@/services/knowledge/page';
import { useOauthStore } from "@/stores/oauth";
import { useNamespacesStore } from '@/stores/knowledge/namespaces';
import NamespaceService from '@/services/knowledge/namespace';
import HTMLEditor from '@/components/HTMLEditor.vue';
import { useI18n } from 'vue-i18n';
import { computed, ref, onMounted } from 'vue';
import { inject } from 'vue';

const props = defineProps({
  defaultData: {
    type: Object,
    default: null
  }
});

const { t } = useI18n();
const route = useRoute();

const oauthStore = useOauthStore();
const namespacesStore = useNamespacesStore();
const modelForm = ref(null);

// Inject refresh pageTreeRef from the layout
const pageTreeRef = inject('pageTreeRef');

// Get URL parameters
const getUrlParams = () => {
  const namespace = route.query.namespace || route.params.namespaceId;
  const parent = route.query.parent;
  return { namespace, parent };
};

// Computed properties
const currentNamespace = computed(() => {
  let namespaceId = route.params.namespaceId || route.query.namespace;
  if (namespaceId && namespacesStore?.allNamespaces) {
    return namespacesStore.allNamespaces.find(ns => ns.id === namespaceId);
  }
  return null;
});

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["knowledge:pages:edit"]);
});


const customCreateResponseParser = (response) => {
  if (response) {
    const { namespaceId } = route.params
    const { id } = response;
    if (pageTreeRef) {
      console.log(pageTreeRef.value);
      pageTreeRef.value.refresh();
    }
    navigateTo(`/knowledge/namespaces/${namespaceId}/pages/${id}`);
  }
  
  return response;
};

// Validation rules
const rules = {
  title: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  slug: [
    {
      validator: (rule, value, callback) => {
        if (value && !isValidSlug(value)) {
          callback(new Error(t('validate_error_invalid_slug')));
          return;
        }
        callback();
      },
      trigger: 'blur'
    }
  ],
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

// Function to convert Vietnamese text to slug
const vietnameseToSlug = (text) => {
  const map = {
    'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'đ': 'd',
    'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
    'Đ': 'D'
  };

  return text
    .split('')
    .map(char => map[char] || char)
    .join('')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/^-+|-+$/g, '')
    .trim();
};


const onTitleChange = (current) => {
  if (current.title) {
    current.slug = vietnameseToSlug(current.title);
  }
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