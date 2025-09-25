<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-4">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">{{ $t('daily_summary') }}</h1>
    </div>

    <!-- Filters -->
    <el-card>
      <el-form :model="filters" inline>
        <el-form-item :label="$t('employee')">
          <el-select 
            v-model="filters.employee_id" 
            :placeholder="$t('select_employee')"
            clearable
            filterable
            style="width: 250px"
            @change="loadSummary"
          >
            <el-option
              v-for="employee in employeesStore.allEmployees"
              :key="employee.id"
              :label="`${employee.first_name} ${employee.last_name}`"
              :value="employee.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item :label="$t('date')">
          <el-date-picker
            v-model="filters.date"
            type="date"
            :placeholder="$t('select_date')"
            format="DD/MM/YYYY"
            value-format="YYYY-MM-DD"
            @change="loadSummary"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="loadSummary" :loading="loading">
            <el-icon><Search /></el-icon>
            {{ $t('load_summary') }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Summary Cards -->
    <div v-if="summary" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <el-card class="text-center">
        <div class="text-3xl font-bold text-blue-600">{{ summary.total_records }}</div>
        <div class="text-gray-600">{{ $t('total_sessions') }}</div>
      </el-card>
      
      <el-card class="text-center">
        <div class="text-3xl font-bold text-green-600">{{ summary.total_duration_hours }}h</div>
        <div class="text-gray-600">{{ $t('total_work_hours') }}</div>
      </el-card>
      
      <el-card class="text-center">
        <div class="text-3xl font-bold text-orange-600">{{ summary.open_sessions }}</div>
        <div class="text-gray-600">{{ $t('open_sessions') }}</div>
      </el-card>
      
      <el-card class="text-center">
        <div class="text-3xl font-bold text-purple-600">{{ formatDuration(summary.total_duration_seconds) }}</div>
        <div class="text-gray-600">{{ $t('total_duration') }}</div>
      </el-card>
    </div>

    <!-- Daily Records -->
    <el-card v-if="summary && summary.records">
      <template #header>
        <div class="flex items-center gap-2">
          <el-icon><Clock /></el-icon>
          <span>{{ $t('daily_records') }} - {{ formatDate(filters.date) }}</span>
        </div>
      </template>

      <el-table :data="summary.records" v-loading="loading" stripe>
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

        <el-table-column prop="office.name" :label="$t('office')" min-width="150">
          <template #default="scope">
            {{ scope.row.office?.name || '-' }}
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

        <el-table-column :label="$t('actions')" min-width="120" fixed="right">
          <template #default="scope">
            <el-button 
              v-if="!scope.row.check_out_at"
              type="warning" 
              size="small"
              @click="checkOut(scope.row)"
            >
              {{ $t('checkout') }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- No Data -->
    <el-card v-else-if="!loading && filters.employee_id && filters.date">
      <div class="text-center py-8">
        <el-icon size="48" color="#909399"><Clock /></el-icon>
        <p class="mt-4 text-lg">{{ $t('no_records_found') }}</p>
        <p class="text-gray-500">{{ $t('no_records_for_date') }}</p>
      </div>
    </el-card>

    <!-- Instructions -->
    <el-card v-else>
      <div class="text-center py-8">
        <el-icon size="48" color="#409EFF"><InfoFilled /></el-icon>
        <p class="mt-4 text-lg">{{ $t('select_employee_and_date') }}</p>
        <p class="text-gray-500">{{ $t('to_view_daily_summary') }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useOauthStore } from '@/stores/oauth'
import { useTimekeepingStore } from '@/stores/timekeeping'
import { useEmployeesStore } from '@/stores/business/employee'
import TimekeepingService from '@/services/hrm/timekeeping'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Search, InfoFilled } from '@element-plus/icons-vue'

definePageMeta({
  layout: 'hrm'
})

const oauthStore = useOauthStore()
const timekeepingStore = useTimekeepingStore()
const employeesStore = useEmployeesStore()

// Reactive data
const filters = ref({
  employee_id: '',
  date: new Date().toISOString().split('T')[0] // Today
})

const loading = ref(false)
const summary = ref(null)

// Methods
const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('vi-VN')
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('vi-VN')
}

const formatDuration = (seconds) => {
  if (!seconds) return '0h 0m'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}h ${minutes}m`
}

const loadSummary = async () => {
  if (!filters.value.employee_id || !filters.value.date) {
    summary.value = null
    return
  }

  try {
    loading.value = true
    const data = await TimekeepingService.getDailySummary(
      filters.value.employee_id,
      filters.value.date
    )
    summary.value = data
  } catch (error) {
    ElMessage.error('Error loading daily summary')
    console.error(error)
    summary.value = null
  } finally {
    loading.value = false
  }
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
    await loadSummary() // Reload summary
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Error checking out')
      console.error(error)
    }
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await employeesStore.fetch()
  } catch (error) {
    console.error('Error loading employees:', error)
  }
})
</script>
