<template>
  <el-dialog
    v-model="dialogVisible"
    :title="$t('move_page')"
    width="600px"
    :before-close="handleClose"
  >
    <div v-if="page" class="move-page-dialog">
      <!-- Current page info -->
      <div class="current-page-info mb-6">
        <h4 class="text-lg font-medium mb-2">{{ $t('page_to_move') }}</h4>
        <div class="flex items-center p-3 bg-blue-50 rounded-lg">
          <el-icon class="mr-2 text-blue-500">
            <Document />
          </el-icon>
          <div>
            <div class="font-medium">{{ page.title }}</div>
            <div class="text-sm text-gray-500">
              {{ $t('current_location') }}: {{ getCurrentLocation() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Target selection -->
      <div class="target-selection mb-6">
        <h4 class="text-lg font-medium mb-2">{{ $t('select_new_parent') }}</h4>
        
        <!-- Root level option -->
        <div 
          class="target-option"
          :class="{ 'selected': selectedParentId === null }"
          @click="selectParent(null)"
        >
          <el-radio 
            v-model="selectedParentId" 
            :label="null"
            @change="selectParent(null)"
          >
            <div class="flex items-center">
              <el-icon class="mr-2">
                <Folder />
              </el-icon>
              <span class="font-medium">{{ $t('root_level') }}</span>
              <span class="text-sm text-gray-500 ml-2">
                ({{ $t('no_parent_page') }})
              </span>
            </div>
          </el-radio>
        </div>

        <!-- Available parent pages -->
        <div class="available-parents max-h-60 overflow-y-auto">
          <div
            v-for="targetPage in availableTargets"
            :key="targetPage.id"
            class="target-option"
            :class="{ 'selected': selectedParentId === targetPage.id }"
            @click="selectParent(targetPage.id)"
          >
            <el-radio 
              v-model="selectedParentId" 
              :label="targetPage.id"
              @change="selectParent(targetPage.id)"
            >
              <div class="flex items-center">
                <el-icon class="mr-2">
                  <Document />
                </el-icon>
                <div>
                  <div class="font-medium">{{ targetPage.title }}</div>
                  <div class="text-sm text-gray-500">
                    {{ getPagePath(targetPage) }}
                  </div>
                </div>
              </div>
            </el-radio>
          </div>
        </div>

        <div v-if="availableTargets.length === 0" class="text-center py-4 text-gray-500">
          {{ $t('no_available_targets') }}
        </div>
      </div>

      <!-- Preview -->
      <div v-if="selectedParentId !== undefined" class="preview-section mb-6">
        <h4 class="text-lg font-medium mb-2">{{ $t('preview') }}</h4>
        <div class="p-3 bg-green-50 rounded-lg">
          <div class="flex items-center">
            <el-icon class="mr-2 text-green-500">
              <Position />
            </el-icon>
            <div>
              <div class="font-medium">{{ getPreviewText() }}</div>
              <div class="text-sm text-gray-600 mt-1">
                {{ $t('new_location') }}: {{ getNewLocation() }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Warnings -->
      <div v-if="hasSubPages" class="warning-section mb-6">
        <el-alert
          :title="$t('move_warning_title')"
          type="warning"
          :description="$t('move_warning_description', { count: subPagesCount })"
          show-icon
          :closable="false"
        />
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">
          {{ $t('cancel') }}
        </el-button>
        <el-button 
          type="primary" 
          :disabled="selectedParentId === undefined || isMoving"
          :loading="isMoving"
          @click="confirmMove"
        >
          {{ $t('move_page') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Document, Folder, Position } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  page: {
    type: Object,
    default: null
  },
  allPages: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'confirm']);

const { t } = useI18n();

// Reactive data
const selectedParentId = ref(undefined);
const isMoving = ref(false);

// Computed properties
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// Get pages that cannot be moved (current page and its descendants)
const excludedPageIds = computed(() => {
  if (!props.page) return [];
  
  const getDescendants = (pageId, pages) => {
    const descendants = [];
    const directChildren = pages.filter(p => p.parent_id === pageId);
    
    directChildren.forEach(child => {
      descendants.push(child.id);
      descendants.push(...getDescendants(child.id, pages));
    });
    
    return descendants;
  };
  
  return [props.page.id, ...getDescendants(props.page.id, props.allPages)];
});

// Available target pages (excluding current page and its descendants)
const availableTargets = computed(() => {
  return props.allPages.filter(page => 
    !excludedPageIds.value.includes(page.id)
  ).sort((a, b) => a.title.localeCompare(b.title));
});

// Check if current page has sub-pages
const hasSubPages = computed(() => {
  if (!props.page) return false;
  return props.allPages.some(p => p.parent_id === props.page.id);
});

const subPagesCount = computed(() => {
  if (!props.page) return 0;
  return props.allPages.filter(p => p.parent_id === props.page.id).length;
});

// Helper methods
const findPageById = (id) => {
  return props.allPages.find(p => p.id === id);
};

const getPagePath = (page) => {
  const path = [];
  let currentPage = page;
  
  while (currentPage && currentPage.parent_id) {
    const parent = findPageById(currentPage.parent_id);
    if (parent) {
      path.unshift(parent.title);
      currentPage = parent;
    } else {
      break;
    }
  }
  
  return path.length > 0 ? path.join(' > ') : t('root_level');
};

const getCurrentLocation = () => {
  if (!props.page) return '';
  
  if (!props.page.parent_id) {
    return t('root_level');
  }
  
  const parent = findPageById(props.page.parent_id);
  return parent ? getPagePath(parent) + ' > ' + parent.title : t('unknown');
};

const getNewLocation = () => {
  if (selectedParentId.value === null) {
    return t('root_level');
  }
  
  const parent = findPageById(selectedParentId.value);
  return parent ? getPagePath(parent) + ' > ' + parent.title : t('unknown');
};

const getPreviewText = () => {
  const pageName = props.page?.title || '';
  
  if (selectedParentId.value === null) {
    return t('move_to_root_preview', { page: pageName });
  }
  
  const parent = findPageById(selectedParentId.value);
  const parentName = parent?.title || '';
  
  return t('move_to_parent_preview', { page: pageName, parent: parentName });
};

const selectParent = (parentId) => {
  selectedParentId.value = parentId;
};

const confirmMove = async () => {
  if (!props.page || selectedParentId.value === undefined) return;
  
  isMoving.value = true;
  try {
    await emit('confirm', props.page.id, selectedParentId.value);
  } finally {
    isMoving.value = false;
  }
};

const handleClose = () => {
  selectedParentId.value = undefined;
  emit('update:modelValue', false);
};

// Watch for dialog visibility changes
watch(() => props.modelValue, (newValue) => {
  if (newValue && props.page) {
    // Reset selection when dialog opens
    selectedParentId.value = undefined;
  }
});
</script>

<style scoped>
.move-page-dialog {
  max-height: 70vh;
  overflow-y: auto;
}

.target-option {
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.target-option:hover {
  border-color: #409eff;
  background-color: #f0f8ff;
}

.target-option.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.target-option :deep(.el-radio) {
  width: 100%;
}

.target-option :deep(.el-radio__label) {
  width: 100%;
  padding-left: 8px;
}

.current-page-info,
.target-selection,
.preview-section,
.warning-section {
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 16px;
}

.current-page-info:last-child,
.target-selection:last-child,
.preview-section:last-child,
.warning-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>