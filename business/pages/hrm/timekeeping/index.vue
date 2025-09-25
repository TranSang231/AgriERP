<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-4">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">{{ $t('time_records') }}</h1>
      <div class="flex gap-2">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          {{ $t('refresh') }}
        </el-button>
      </div>
    </div>

    <!-- Filters -->
    <el-card class="mb-4">
      <el-form :model="filters" inline>
        <el-form-item :label="$t('employee')">
          <el-select 
            v-model="filters.employee_id" 
            :placeholder="$t('select_employee')"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="employee in employeesStore.allEmployees"
              :key="employee.id"
              :label="`${employee.first_name} ${employee.last_name}`"
              :value="employee.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item :label="$t('office')">
          <el-select 
            v-model="filters.office_id" 
            :placeholder="$t('select_office')"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="office in officesStore.allOffices"
              :key="office.id"
              :label="office.name"
              :value="office.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item :label="$t('date_from')">
          <el-date-picker
            v-model="filters.date_from"
            type="date"
            :placeholder="$t('select_date')"
            format="DD/MM/YYYY"
            value-format="YYYY-MM-DD"
            clearable
          />
        </el-form-item>

        <el-form-item :label="$t('date_to')">
          <el-date-picker
            v-model="filters.date_to"
            type="date"
            :placeholder="$t('select_date')"
            format="DD/MM/YYYY"
            value-format="YYYY-MM-DD"
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="applyFilters">
            {{ $t('filter') }}
          </el-button>
          <el-button @click="clearFilters">
            {{ $t('clear') }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Time Records Table -->
    <el-card>
      <el-table 
        :data="filteredRecords" 
        v-loading="timekeepingStore.loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="employee.first_name" :label="$t('first_name')" min-width="120">
          <template #default="scope">
            {{ scope.row.employee?.first_name || 'N/A' }}
          </template>
        </el-table-column>
        
        <el-table-column prop="employee.last_name" :label="$t('last_name')" min-width="120">
          <template #default="scope">
            {{ scope.row.employee?.last_name || 'N/A' }}
          </template>
        </el-table-column>

        <el-table-column prop="office.name" :label="$t('office')" min-width="150">
          <template #default="scope">
            {{ scope.row.office?.name || '-' }}
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

        <el-table-column prop="note" :label="$t('note')" min-width="150">
          <template #default="scope">
            {{ scope.row.note || '-' }}
          </template>
        </el-table-column>

        <el-table-column :label="$t('actions')" min-width="150" fixed="right">
          <template #default="scope">
            <el-button 
              v-if="!scope.row.check_out_at"
              type="warning" 
              size="small"
              @click="checkOut(scope.row)"
            >
              {{ $t('checkout') }}
            </el-button>
            <el-button 
              v-if="canEdit"
              type="danger" 
              size="small"
              @click="deleteRecord(scope.row)"
            >
              {{ $t('delete') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalRecords"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOauthStore } from '@/stores/oauth'
import { useTimekeepingStore } from '@/stores/timekeeping'
import { useEmployeesStore } from '@/stores/business/employee'
import { useOfficesStore } from '@/stores/offices'
import TimekeepingService from '@/services/hrm/timekeeping'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

definePageMeta({
  layout: 'hrm'
})

const oauthStore = useOauthStore()
const timekeepingStore = useTimekeepingStore()
const employeesStore = useEmployeesStore()
const officesStore = useOfficesStore()

// Reactive data
const filters = ref({
  employee_id: '',
  office_id: '',
  date_from: '',
  date_to: ''
})

const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// Computed
const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(['timekeeping:edit'])
})

const filteredRecords = computed(() => {
  return timekeepingStore.allTimeRecords
})

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

const applyFilters = async () => {
  try {
    timekeepingStore.setLoading(true)
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters.value
    }
    
    // Remove empty filters
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })
    
    const data = await TimekeepingService.getTimeRecords(params)
    timekeepingStore.setTimeRecords(data.results || data)
    totalRecords.value = data.count || data.length
  } catch (error) {
    ElMessage.error('Error loading time records')
    console.error(error)
  } finally {
    timekeepingStore.setLoading(false)
  }
}

const clearFilters = () => {
  filters.value = {
    employee_id: '',
    office_id: '',
    date_from: '',
    date_to: ''
  }
  applyFilters()
}

const refreshData = () => {
  applyFilters()
}

const checkOut = async (record) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to check out this session?',
      'Confirm Check Out',
      {
        confirmButtonText: 'Yes',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    await TimekeepingService.checkOut(record.id)
    ElMessage.success('Checked out successfully')
    refreshData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Error checking out')
      console.error(error)
    }
  }
}

const deleteRecord = async (record) => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this time record?',
      'Confirm Delete',
      {
        confirmButtonText: 'Yes',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    await TimekeepingService.delete(record.id)
    ElMessage.success('Time record deleted successfully')
    refreshData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Error deleting time record')
      console.error(error)
    }
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  applyFilters()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  applyFilters()
}

// Lifecycle
onMounted(async () => {
  try {
    // Load initial data
    await Promise.all([
      employeesStore.fetch(),
      officesStore.fetch(),
      applyFilters()
    ])
  } catch (error) {
    console.error('Error loading initial data:', error)
  }
})
</script>
