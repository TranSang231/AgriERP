<template>
  <div class="flex flex-col w-full pt-20 px-6">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">
            {{ t('Customer Overview') }}
          </h1>
          <p class="text-gray-600 mt-1">{{ t('Statistics and insights for your e-commerce customers') }}</p>
        </div>
        <div class="flex space-x-2">
          <el-button @click="refreshData">
            <el-icon class="mr-1"><Refresh /></el-icon>
            {{ t('Refresh') }}
          </el-button>
          <el-button type="primary" @click="goToCustomers">
            {{ t('View All Customers') }}
          </el-button>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <el-card class="text-center">
          <div class="flex flex-col items-center">
            <el-icon class="text-4xl text-blue-500 mb-2"><User /></el-icon>
            <h3 class="text-2xl font-bold text-gray-900">{{ totalCustomers }}</h3>
            <p class="text-gray-600">{{ t('Total Customers') }}</p>
          </div>
        </el-card>

        <el-card class="text-center">
          <div class="flex flex-col items-center">
            <el-icon class="text-4xl text-green-500 mb-2"><Check /></el-icon>
            <h3 class="text-2xl font-bold text-gray-900">{{ activeCustomers }}</h3>
            <p class="text-gray-600">{{ t('Active Customers') }}</p>
          </div>
        </el-card>

        <el-card class="text-center">
          <div class="flex flex-col items-center">
            <el-icon class="text-4xl text-red-500 mb-2"><Close /></el-icon>
            <h3 class="text-2xl font-bold text-gray-900">{{ inactiveCustomers }}</h3>
            <p class="text-gray-600">{{ t('Inactive Customers') }}</p>
          </div>
        </el-card>

        <el-card class="text-center">
          <div class="flex flex-col items-center">
            <el-icon class="text-4xl text-purple-500 mb-2"><TrendCharts /></el-icon>
            <h3 class="text-2xl font-bold text-gray-900">{{ newCustomersThisMonth }}</h3>
            <p class="text-gray-600">{{ t('New This Month') }}</p>
          </div>
        </el-card>
      </div>

      <!-- Gender Distribution -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <el-card>
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2"><PieChart /></el-icon>
              <span class="font-semibold">{{ t('Gender Distribution') }}</span>
            </div>
          </template>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-gray-600">{{ t('Male') }}</span>
              <div class="flex items-center">
                <div class="w-32 bg-gray-200 rounded-full h-2 mr-2">
                  <div 
                    class="bg-blue-500 h-2 rounded-full" 
                    :style="{ width: malePercentage + '%' }"
                  ></div>
                </div>
                <span class="text-sm font-medium">{{ maleCustomers }} ({{ malePercentage }}%)</span>
              </div>
            </div>
            
            <div class="flex justify-between items-center">
              <span class="text-gray-600">{{ t('Female') }}</span>
              <div class="flex items-center">
                <div class="w-32 bg-gray-200 rounded-full h-2 mr-2">
                  <div 
                    class="bg-pink-500 h-2 rounded-full" 
                    :style="{ width: femalePercentage + '%' }"
                  ></div>
                </div>
                <span class="text-sm font-medium">{{ femaleCustomers }} ({{ femalePercentage }}%)</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Recent Customers -->
        <el-card>
          <template #header>
            <div class="flex items-center">
              <el-icon class="mr-2"><Clock /></el-icon>
              <span class="font-semibold">{{ t('Recent Customers') }}</span>
            </div>
          </template>
          
          <div class="space-y-3">
            <div
              v-for="customer in recentCustomers"
              :key="customer.id"
              class="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded"
            >
              <el-avatar
                :src="customer.avatar"
                :size="40"
                shape="circle"
                icon="User"
              />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ getCustomerName(customer) }}
                </p>
                <p class="text-xs text-gray-500">{{ customer.email }}</p>
              </div>
              <el-tag
                :type="getStatusType(customer.status)"
                size="small"
              >
                {{ getStatusLabel(customer.status) }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Customer List with Actions -->
      <el-card>
        <template #header>
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <el-icon class="mr-2"><List /></el-icon>
              <span class="font-semibold">{{ t('All Customers') }}</span>
            </div>
            <el-button type="primary" @click="goToCustomers">
              {{ t('Manage Customers') }}
            </el-button>
          </div>
        </template>
        
        <div class="overflow-x-auto">
          <el-table :data="customers" style="width: 100%">
            <el-table-column prop="name" :label="t('Name')" min-width="200">
              <template #default="scope">
                <div class="flex items-center space-x-3">
                  <el-avatar
                    :src="scope.row.avatar"
                    :size="32"
                    shape="circle"
                    icon="User"
                  />
                  <div>
                    <p class="font-medium">{{ getCustomerName(scope.row) }}</p>
                    <p class="text-sm text-gray-500">{{ scope.row.email }}</p>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="phone" :label="t('Phone')" min-width="120">
              <template #default="scope">
                {{ scope.row.phone || '-' }}
              </template>
            </el-table-column>
            
            <el-table-column prop="gender" :label="t('Gender')" min-width="100">
              <template #default="scope">
                <el-tag
                  :type="scope.row.gender === 'male' ? 'primary' : 'success'"
                  size="small"
                >
                  {{ getGenderLabel(scope.row.gender) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="status" :label="t('Status')" min-width="100">
              <template #default="scope">
                <el-tag
                  :type="getStatusType(scope.row.status)"
                  size="small"
                >
                  {{ getStatusLabel(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" :label="t('Created')" min-width="120">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            
            <el-table-column :label="t('Actions')" min-width="120">
              <template #default="scope">
                <el-button
                  size="small"
                  @click="viewCustomer(scope.row.id)"
                >
                  {{ t('View') }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CustomerService from '@/services/e-commerce/customer'
import { useCustomersStore } from '@/stores/e-commerce/customers'
import { formatDate } from '~/utils/time'
import { ElMessage } from 'element-plus'

definePageMeta({
  layout: 'ecommerce'
})

const { t } = useI18n()
const router = useRouter()
const customersStore = useCustomersStore()

const customers = ref([])
const loading = ref(false)

const totalCustomers = computed(() => customersStore.allCustomers.length)
const activeCustomers = computed(() => customersStore.activeCustomers.length)
const inactiveCustomers = computed(() => customersStore.inactiveCustomers.length)
const maleCustomers = computed(() => customersStore.customersByGender('male').length)
const femaleCustomers = computed(() => customersStore.customersByGender('female').length)

const malePercentage = computed(() => {
  if (totalCustomers.value === 0) return 0
  return Math.round((maleCustomers.value / totalCustomers.value) * 100)
})

const femalePercentage = computed(() => {
  if (totalCustomers.value === 0) return 0
  return Math.round((femaleCustomers.value / totalCustomers.value) * 100)
})

const newCustomersThisMonth = computed(() => {
  const now = new Date()
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
  
  return customersStore.allCustomers.filter(customer => {
    const createdDate = new Date(customer.created_at)
    return createdDate >= startOfMonth
  }).length
})

const recentCustomers = computed(() => {
  return customersStore.allCustomers
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 5)
})

const loadCustomers = async () => {
  try {
    loading.value = true
    await CustomerService.fetch(true)
    customers.value = customersStore.allCustomers.slice(0, 10) // Show first 10 customers
  } catch (error) {
    console.error('Error loading customers:', error)
    ElMessage.error(t('Failed to load customers'))
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadCustomers()
}

const goToCustomers = () => {
  router.push('/e-commerce/customers')
}

const viewCustomer = (customerId) => {
  router.push(`/e-commerce/customers/${customerId}`)
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

onMounted(() => {
  loadCustomers()
})
</script>
