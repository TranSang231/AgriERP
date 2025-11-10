<template>
  <div v-if="!hasPermission" class="permission-guard">
    <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
        </svg>
        <div>
          <h3 class="text-sm font-medium text-red-800">{{ title }}</h3>
          <p class="text-sm text-red-700 mt-1">{{ message }}</p>
          <div v-if="showUpgrade" class="mt-3">
            <button 
              @click="$emit('upgrade')" 
              class="text-sm bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded-md transition-colors"
            >
              {{ upgradeText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useActionPermissions } from '~/composables/useActionPermissions'
import { CustomerPermission } from '~/stores/auth'

interface Props {
  permission: CustomerPermission
  title?: string
  message?: string
  showUpgrade?: boolean
  upgradeText?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Không có quyền truy cập',
  message: 'Bạn không có quyền thực hiện hành động này.',
  showUpgrade: false,
  upgradeText: 'Nâng cấp tài khoản'
})

const emit = defineEmits<{
  upgrade: []
}>()
import { useAuthorization } from '~/composables/useAuthorization'

const { can } = useAuthorization ()

const hasPermission = computed(() => can(props.permission))
</script>

<style scoped>
.permission-guard {
  /* Additional styling if needed */
}
</style>
