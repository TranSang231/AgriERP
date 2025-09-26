<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-4">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">{{ $t('checkin') }}</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Check In Form -->
      <el-card>
        <template #header>
          <div class="flex items-center gap-2">
            <el-icon><Clock /></el-icon>
            <span>{{ $t('check_in_now') }}</span>
          </div>
        </template>

        <el-form 
          :model="checkInForm" 
          :rules="checkInRules" 
          ref="checkInFormRef"
          label-width="120px"
        >
          <el-form-item :label="$t('employee')" prop="employee_id">
            <el-select 
              v-model="checkInForm.employee_id" 
              :placeholder="$t('select_employee')"
              filterable
              style="width: 100%"
              @change="onEmployeeChange"
            >
              <el-option
                v-for="employee in employeesStore.allEmployees"
                :key="employee.id"
                :label="`${employee.first_name} ${employee.last_name}`"
                :value="employee.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item :label="$t('office')" prop="office_id">
            <el-select 
              v-model="checkInForm.office_id" 
              :placeholder="$t('select_office')"
              clearable
              style="width: 100%"
            >
              <el-option
                v-for="office in officesStore.allOffices"
                :key="office.id"
                :label="office.name"
                :value="office.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item :label="$t('check_in_time')" prop="check_in_at">
            <el-date-picker
              v-model="checkInForm.check_in_at"
              type="datetime"
              :placeholder="$t('select_datetime')"
              format="DD/MM/YYYY HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item :label="$t('source')" prop="source">
            <el-select 
              v-model="checkInForm.source" 
              :placeholder="$t('select_source')"
              clearable
              style="width: 100%"
            >
              <el-option label="Web" value="web" />
              <el-option label="Mobile" value="mobile" />
              <el-option label="Device" value="device" />
              <el-option label="Manual" value="manual" />
            </el-select>
          </el-form-item>

          <el-form-item :label="$t('note')" prop="note">
            <el-input
              v-model="checkInForm.note"
              type="textarea"
              :rows="3"
              :placeholder="$t('enter_note')"
            />
          </el-form-item>

          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleCheckIn"
              :loading="loading"
              :disabled="!canCheckIn"
            >
              <el-icon><Check /></el-icon>
              {{ $t('checkin') }}
            </el-button>
            <div v-if="!canCheckIn" class="text-xs text-red-500 mt-1">
              {{ $t('no_permission_to_checkin') }}
            </div>
            <el-button @click="resetForm">
              {{ $t('reset') }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- Current Session Info -->
      <el-card v-if="currentSession">
        <template #header>
          <div class="flex items-center gap-2">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ $t('current_session') }}</span>
          </div>
        </template>

        <div class="space-y-4">
          <div class="flex justify-between">
            <span class="font-medium">{{ $t('employee') }}:</span>
            <span>{{ getEmployeeName(currentSession.employee_id) }}</span>
          </div>
          
          <div class="flex justify-between">
            <span class="font-medium">{{ $t('office') }}:</span>
            <span>{{ getOfficeName(currentSession.office_id) || '-' }}</span>
          </div>
          
          <div class="flex justify-between">
            <span class="font-medium">{{ $t('check_in_time') }}:</span>
            <span>{{ formatDateTime(currentSession.check_in_at) }}</span>
          </div>
          
          <div class="flex justify-between">
            <span class="font-medium">{{ $t('duration') }}:</span>
            <el-tag type="warning">{{ formatDuration(currentSession.duration_seconds) }}</el-tag>
          </div>

          <div class="flex justify-between">
            <span class="font-medium">{{ $t('source') }}:</span>
            <span>{{ currentSession.source || '-' }}</span>
          </div>

          <div v-if="currentSession.note" class="flex justify-between">
            <span class="font-medium">{{ $t('note') }}:</span>
            <span>{{ currentSession.note }}</span>
          </div>

          <el-divider />

          <el-button 
            type="warning" 
            @click="handleCheckOut"
            :loading="checkOutLoading"
            style="width: 100%"
          >
            <el-icon><Close /></el-icon>
            {{ $t('checkout') }}
          </el-button>
        </div>
      </el-card>

      <!-- No Current Session -->
      <el-card v-else-if="selectedEmployeeId">
        <template #header>
          <div class="flex items-center gap-2">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ $t('session_status') }}</span>
          </div>
        </template>

        <div class="text-center py-8">
          <el-icon size="48" color="#67C23A"><Check /></el-icon>
          <p class="mt-4 text-lg">{{ $t('no_open_session') }}</p>
          <p class="text-gray-500">{{ $t('ready_to_check_in') }}</p>
        </div>
      </el-card>
    </div>

    <!-- Recent Records -->
    <el-card>
      <template #header>
        <div class="flex items-center gap-2">
          <el-icon><Clock /></el-icon>
          <span>{{ $t('recent_records') }}</span>
        </div>
      </template>

      <el-table :data="recentRecords" v-loading="loadingRecent">
        <el-table-column prop="employee.first_name" :label="$t('employee')" min-width="150">
          <template #default="scope">
            {{ getEmployeeName(scope.row.employee_id) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="check_in_at" :label="$t('checkin')" min-width="150">
          <template #default="scope">
            {{ formatDateTime(scope.row.check_in_at) }}
          </template>
        </el-table-column>

        <el-table-column prop="check_out_at" :label="$t('checkout')" min-width="150">
          <template #default="scope">
            {{ scope.row.check_out_at ? formatDateTime(scope.row.check_out_at) : '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="duration_seconds" :label="$t('duration')" min-width="120">
          <template #default="scope">
            <el-tag :type="scope.row.check_out_at ? 'success' : 'warning'">
              {{ scope.row.check_out_at ? formatDuration(scope.row.duration_seconds) : $t('in_progress') }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="source" :label="$t('source')" min-width="100">
          <template #default="scope">
            {{ scope.row.source || '-' }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useOauthStore } from '@/stores/oauth'
import { useTimekeepingStore } from '@/stores/timekeeping'
import { useEmployeesStore } from '@/stores/business/employee'
import { useOfficesStore } from '@/stores/offices'
import TimekeepingService from '@/services/hrm/timekeeping'
import EmployeeService from '@/services/hrm/employees'
import OfficeService from '@/services/offices'
import { ElMessage } from 'element-plus'
import { Clock, Check, Close, InfoFilled } from '@element-plus/icons-vue'

definePageMeta({
  layout: 'hrm'
})

const oauthStore = useOauthStore()
const timekeepingStore = useTimekeepingStore()
const employeesStore = useEmployeesStore()
const officesStore = useOfficesStore()

// Reactive data
const checkInForm = ref({
  employee_id: '',
  office_id: '',
  check_in_at: '',
  source: 'web',
  note: ''
})

const checkInFormRef = ref()
const loading = ref(false)
const checkOutLoading = ref(false)
const loadingRecent = ref(false)
const currentSession = ref(null)
const recentRecords = ref([])

// Computed
const canCheckIn = computed(() => {
  const hasPermission = oauthStore.hasOneOfScopes(['timekeeping:check'])
  console.log('Can check in:', hasPermission, 'Available scopes:', oauthStore.tokenInfo?.scopes)
  return hasPermission
})

const selectedEmployeeId = computed(() => checkInForm.value.employee_id)

// Validation rules
const checkInRules = {
  employee_id: [
    { required: true, message: 'Please select an employee', trigger: 'change' }
  ]
}

// Methods
const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('vi-VN')
}

const formatDuration = (seconds) => {
  if (!seconds) return '0h 0m'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}h ${minutes}m`
}

const getEmployeeName = (employeeId) => {
  const employee = employeesStore.allEmployees.find(emp => emp.id === employeeId)
  return employee ? `${employee.first_name} ${employee.last_name}` : 'Unknown'
}

const getOfficeName = (officeId) => {
  const office = officesStore.allOffices.find(off => off.id === officeId)
  return office ? office.name : null
}

const onEmployeeChange = async () => {
  if (selectedEmployeeId.value) {
    await loadCurrentSession()
  } else {
    currentSession.value = null
  }
}

const loadCurrentSession = async () => {
  if (!selectedEmployeeId.value) return
  
  try {
    const session = await TimekeepingService.getCurrentSession(selectedEmployeeId.value)
    currentSession.value = session
  } catch (error) {
    console.error('Error loading current session:', error)
  }
}

const handleCheckIn = async () => {
  if (!checkInFormRef.value) return
  
  try {
    await checkInFormRef.value.validate()
    
    loading.value = true
    
    const data = {
      ...checkInForm.value,
      check_in_at: checkInForm.value.check_in_at || new Date().toISOString()
    }
    
    console.log('Check-in data:', data)
    const result = await TimekeepingService.checkIn(data)
    console.log('Check-in result:', result)
    
    ElMessage.success('Checked in successfully')
    
    resetForm()
    await loadCurrentSession()
    await loadRecentRecords()
  } catch (error) {
    console.error('Check-in error:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else if (error.response?.data) {
      ElMessage.error(JSON.stringify(error.response.data))
    } else {
      ElMessage.error('Error checking in: ' + error.message)
    }
  } finally {
    loading.value = false
  }
}

const handleCheckOut = async () => {
  if (!currentSession.value) return
  
  try {
    checkOutLoading.value = true
    
    await TimekeepingService.checkOut(currentSession.value.id)
    ElMessage.success('Checked out successfully')
    
    currentSession.value = null
    await loadRecentRecords()
  } catch (error) {
    ElMessage.error('Error checking out')
    console.error(error)
  } finally {
    checkOutLoading.value = false
  }
}

const resetForm = () => {
  checkInForm.value = {
    employee_id: '',
    office_id: '',
    check_in_at: '',
    source: 'web',
    note: ''
  }
  currentSession.value = null
  if (checkInFormRef.value) {
    checkInFormRef.value.clearValidate()
  }
}

const loadRecentRecords = async () => {
  try {
    loadingRecent.value = true
    const records = await TimekeepingService.getTimeRecords({ page_size: 10 })
    recentRecords.value = records.results || records
  } catch (error) {
    console.error('Error loading recent records:', error)
  } finally {
    loadingRecent.value = false
  }
}

// Watchers
watch(selectedEmployeeId, () => {
  onEmployeeChange()
})

// Lifecycle
onMounted(async () => {
  try {
    // Force fetch fresh data from server
    await Promise.all([
      EmployeeService.fetch(true), // force = true
      OfficeService.fetch(true),   // force = true
      loadRecentRecords()
    ])
    console.log('Loaded offices:', officesStore.allOffices)
  } catch (error) {
    console.error('Error loading initial data:', error)
  }
})
</script>
