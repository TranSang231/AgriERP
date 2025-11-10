<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <el-loading v-loading="loading" />
    </div>
    
    <div v-else-if="customerData" class="w-full max-w-6xl">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex items-center space-x-4">
          <el-avatar
            :src="customerData.avatar"
            :size="80"
            shape="circle"
            icon="User"
          />
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ getCustomerName(customerData) }}
            </h1>
            <p class="text-gray-600">{{ customerData.email }}</p>
            <p class="text-sm text-blue-600 font-medium">{{ t('E-commerce Customer') }}</p>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <el-button
            v-if="canEdit"
            type="primary"
            @click="editCustomer"
          >
            {{ t('Edit') }}
          </el-button>
          <el-button
            v-if="canEdit"
            type="danger"
            @click="deleteCustomer"
          >
            {{ t('Delete') }}
          </el-button>
        </div>
      </div>

      <!-- Status Badge -->
      <div class="mb-6">
        <el-tag
          :type="getStatusType(customerData.status)"
          size="large"
        >
          {{ getStatusLabel(customerData.status) }}
        </el-tag>
      </div>

      <!-- Customer Information -->
      <el-card class="mb-6">
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><User /></el-icon>
            <span class="font-semibold">{{ t('Customer Information') }}</span>
          </div>
        </template>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('First Name') }}
            </label>
            <p class="text-gray-900">{{ customerData.first_name || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Last Name') }}
            </label>
            <p class="text-gray-900">{{ customerData.last_name || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Email') }}
            </label>
            <p class="text-gray-900">{{ customerData.email || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Phone') }}
            </label>
            <p class="text-gray-900">{{ customerData.phone || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Gender') }}
            </label>
            <p class="text-gray-900">{{ getGenderLabel(customerData.gender) }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Date of Birth') }}
            </label>
            <p class="text-gray-900">{{ customerData.date_of_birth ? formatDate(customerData.date_of_birth) : '-' }}</p>
          </div>
        </div>
        
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ t('Address') }}
          </label>
          <p class="text-gray-900">{{ customerData.address || '-' }}</p>
        </div>
      </el-card>

      <!-- Location Information -->
      <el-card class="mb-6" v-if="customerData.province_id || customerData.district_id || customerData.ward_id">
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Location /></el-icon>
            <span class="font-semibold">{{ t('Location Information') }}</span>
          </div>
        </template>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Province') }}
            </label>
            <p class="text-gray-900">{{ customerData.province_id || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('District') }}
            </label>
            <p class="text-gray-900">{{ customerData.district_id || '-' }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Ward') }}
            </label>
            <p class="text-gray-900">{{ customerData.ward_id || '-' }}</p>
          </div>
        </div>
      </el-card>

      <!-- Shipping Addresses -->
      <el-card v-if="customerData.shipping_addresses && customerData.shipping_addresses.length > 0">
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Truck /></el-icon>
            <span class="font-semibold">{{ t('Shipping Addresses') }}</span>
          </div>
        </template>
        
        <div class="space-y-4">
          <div
            v-for="(address, index) in customerData.shipping_addresses"
            :key="index"
            class="border rounded-lg p-4"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium text-gray-900">
                  {{ address.name || t('Address') }} {{ index + 1 }}
                </h4>
                <p class="text-gray-600">{{ address.address }}</p>
                <p class="text-sm text-gray-500">
                  {{ address.phone || customerData.phone }}
                </p>
              </div>
              <el-tag
                v-if="address.is_default"
                type="success"
                size="small"
              >
                {{ t('Default') }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Timestamps -->
      <el-card class="mt-6">
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><Clock /></el-icon>
            <span class="font-semibold">{{ t('Timestamps') }}</span>
          </div>
        </template>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Created At') }}
            </label>
            <p class="text-gray-900">{{ formatDateTime(customerData.created_at) }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('Updated At') }}
            </label>
            <p class="text-gray-900">{{ formatDateTime(customerData.updated_at) }}</p>
          </div>
        </div>
      </el-card>
    </div>
    
    <div v-else class="flex justify-center items-center h-64">
      <el-empty :description="t('Customer not found')" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CustomerService from '@/services/e-commerce/customer'
import { formatDateTime, formatDate } from '~/utils/time'
import { useOauthStore } from '@/stores/oauth'
import { ElMessage, ElMessageBox } from 'element-plus'

definePageMeta({
  layout: 'ecommerce'
})

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const customerData = ref(null)
const loading = ref(true)

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:customers:edit"]))

const loadCustomer = async () => {
  try {
    loading.value = true
    const customerId = route.params.id
    if (customerId && customerId !== 'new') {
      const response = await CustomerService.getCustomer(customerId)
      customerData.value = response
    }
  } catch (error) {
    console.error('Error loading customer:', error)
    ElMessage.error(t('Failed to load customer data'))
  } finally {
    loading.value = false
  }
}

const getCustomerName = (customer) => {
  const firstName = customer.first_name || ''
  const lastName = customer.last_name || ''
  return `${firstName} ${lastName}`.trim() || customer.email || '-'
}

const getGenderLabel = (gender) => {
  switch (gender) {
    case 'male':
      return t('Male')
    case 'female':
      return t('Female')
    default:
      return '-'
  }
}

const getStatusLabel = (status) => {
  switch (status) {
    case 1:
      return t('Active')
    case 0:
      return t('Inactive')
    default:
      return t('Unknown')
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 1:
      return 'success'
    case 0:
      return 'danger'
    default:
      return 'info'
  }
}

const editCustomer = () => {
  router.push(`/e-commerce/customers/edit?id=${route.params.id}`)
}

const deleteCustomer = async () => {
  try {
    await ElMessageBox.confirm(
      t('Are you sure you want to delete this customer?'),
      t('Confirm Delete'),
      {
        confirmButtonText: t('Delete'),
        cancelButtonText: t('Cancel'),
        type: 'warning',
      }
    )
    
    await CustomerService.deleteCustomer(route.params.id)
    ElMessage.success(t('Customer deleted successfully'))
    router.push('/e-commerce/customers')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting customer:', error)
      ElMessage.error(t('Failed to delete customer'))
    }
  }
}

onMounted(() => {
  loadCustomer()
})
</script>
