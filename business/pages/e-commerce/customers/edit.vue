<template>
  <div class="flex flex-col w-full pt-20 px-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <el-loading v-loading="loading" />
    </div>
    
    <div v-else-if="customerData" class="max-w-4xl mx-auto w-full">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">
            {{ t('Edit Customer') }}: {{ getCustomerName(customerData) }}
          </h1>
          <p class="text-gray-600 mt-1">{{ t('Update e-commerce customer information') }}</p>
        </div>
        <el-button @click="goBack">
          {{ t('Back') }}
        </el-button>
      </div>

      <!-- Customer Form -->
      <el-card>
        <template #header>
          <div class="flex items-center">
            <el-icon class="mr-2"><User /></el-icon>
            <span class="font-semibold">{{ t('Customer Information') }}</span>
          </div>
        </template>

        <el-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          label-width="120px"
          class="space-y-6"
        >
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <el-form-item :label="t('First Name')" prop="first_name">
              <el-input
                v-model="formData.first_name"
                :placeholder="t('Enter first name')"
              />
            </el-form-item>

            <el-form-item :label="t('Last Name')" prop="last_name">
              <el-input
                v-model="formData.last_name"
                :placeholder="t('Enter last name')"
              />
            </el-form-item>

            <el-form-item :label="t('Email')" prop="email">
              <el-input
                v-model="formData.email"
                type="email"
                :placeholder="t('Enter email address')"
              />
            </el-form-item>

            <el-form-item :label="t('Phone')" prop="phone">
              <el-input
                v-model="formData.phone"
                :placeholder="t('Enter phone number')"
              />
            </el-form-item>

            <el-form-item :label="t('Gender')" prop="gender">
              <el-select
                v-model="formData.gender"
                :placeholder="t('Select gender')"
                class="w-full"
              >
                <el-option
                  :label="t('Male')"
                  value="male"
                />
                <el-option
                  :label="t('Female')"
                  value="female"
                />
              </el-select>
            </el-form-item>

            <el-form-item :label="t('Date of Birth')" prop="date_of_birth">
              <el-date-picker
                v-model="formData.date_of_birth"
                type="date"
                :placeholder="t('Select date of birth')"
                class="w-full"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </div>

          <!-- Address Information -->
          <el-form-item :label="t('Address')" prop="address">
            <el-input
              v-model="formData.address"
              type="textarea"
              :rows="3"
              :placeholder="t('Enter address')"
            />
          </el-form-item>

          <!-- Location Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <el-form-item :label="t('Province')" prop="province_id">
              <el-input
                v-model="formData.province_id"
                :placeholder="t('Enter province ID')"
              />
            </el-form-item>

            <el-form-item :label="t('District')" prop="district_id">
              <el-input
                v-model="formData.district_id"
                :placeholder="t('Enter district ID')"
              />
            </el-form-item>

            <el-form-item :label="t('Ward')" prop="ward_id">
              <el-input
                v-model="formData.ward_id"
                :placeholder="t('Enter ward ID')"
              />
            </el-form-item>
          </div>

          <!-- Avatar -->
          <el-form-item :label="t('Avatar')" prop="avatar">
            <el-input
              v-model="formData.avatar"
              :placeholder="t('Enter avatar URL')"
            />
          </el-form-item>

          <!-- Status -->
          <el-form-item :label="t('Status')" prop="status">
            <el-select
              v-model="formData.status"
              :placeholder="t('Select status')"
              class="w-full"
            >
              <el-option
                :label="t('Active')"
                :value="1"
              />
              <el-option
                :label="t('Inactive')"
                :value="0"
              />
            </el-select>
          </el-form-item>

          <!-- Form Actions -->
          <div class="flex justify-end space-x-4 pt-6 border-t">
            <el-button @click="goBack">
              {{ t('Cancel') }}
            </el-button>
            <el-button
              type="primary"
              :loading="saving"
              @click="submitForm"
            >
              {{ t('Update') }}
            </el-button>
          </div>
        </el-form>
      </el-card>
    </div>
    
    <div v-else class="flex justify-center items-center h-64">
      <el-empty :description="t('Customer not found')" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CustomerService from '@/services/e-commerce/customer'
import { ElMessage } from 'element-plus'

definePageMeta({
  layout: 'ecommerce'
})

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const formRef = ref()
const saving = ref(false)
const loading = ref(true)
const customerData = ref(null)
const customerId = route.query.id

const formData = reactive({
  id: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: '',
  avatar: '',
  province_id: '',
  district_id: '',
  ward_id: '',
  date_of_birth: '',
  gender: '',
  status: 1
})

const formRules = {
  email: [
    { required: true, message: t('Please enter email address'), trigger: 'blur' },
    { type: 'email', message: t('Please enter a valid email address'), trigger: 'blur' }
  ],
  first_name: [
    { required: true, message: t('Please enter first name'), trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: t('Please enter last name'), trigger: 'blur' }
  ]
}

const loadCustomer = async () => {
  try {
    loading.value = true
    const response = await CustomerService.getCustomer(customerId)
    customerData.value = response
    Object.assign(formData, response)
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

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    await CustomerService.updateCustomer(formData)
    ElMessage.success(t('Customer updated successfully'))
    router.push(`/e-commerce/customers/${customerId}`)
  } catch (error) {
    console.error('Error saving customer:', error)
    ElMessage.error(t('Failed to save customer'))
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push(`/e-commerce/customers/${customerId}`)
}

onMounted(() => {
  loadCustomer()
})
</script>
