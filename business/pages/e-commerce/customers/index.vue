<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="CustomerService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
      <el-table-column prop="avatar" :label="t('Avatar')" min-width="80">
        <template #default="scope">
          <el-avatar
            v-if="scope.row.avatar"
            :src="scope.row.avatar"
            :size="50"
            shape="circle"
          />
          <el-avatar
            v-else
            :size="50"
            shape="circle"
            icon="User"
          />
        </template>
      </el-table-column>
      
      <el-table-column prop="name" :label="t('Name')" min-width="200">
        <template #default="scope">
          <div class="flex flex-col">
            <span class="font-medium">
              {{ getCustomerName(scope.row) }}
            </span>
            <span class="text-sm text-gray-500">
              {{ scope.row.email }}
            </span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="phone" :label="t('Phone')" min-width="150">
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
      
      <el-table-column prop="status" :label="t('Status')" min-width="120">
        <template #default="scope">
          <el-tag
            :type="getStatusType(scope.row.status)"
            size="small"
          >
            {{ getStatusLabel(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="date_of_birth" :label="t('Date of Birth')" min-width="120">
        <template #default="scope">
          {{ scope.row.date_of_birth ? formatDate(scope.row.date_of_birth) : '-' }}
        </template>
      </el-table-column>
      
      <el-table-column
        prop="created_at"
        :label="t('Created_at')"
        min-width="150"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.created_at) }}
        </template>
      </el-table-column>
    </PaginationTable>
  </div>
</template>

<script setup>
import CustomerService from "@/services/e-commerce/customer";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime, formatDate } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();

const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:customers:edit"]));

const getCustomerName = (customer) => {
  const firstName = customer.first_name || '';
  const lastName = customer.last_name || '';
  return `${firstName} ${lastName}`.trim() || customer.email || '-';
};

const getGenderLabel = (gender) => {
  switch (gender) {
    case 'male':
      return t('Male');
    case 'female':
      return t('Female');
    default:
      return '-';
  }
};

const getStatusLabel = (status) => {
  switch (status) {
    case 1:
      return t('Active');
    case 0:
      return t('Inactive');
    default:
      return t('Unknown');
  }
};

const getStatusType = (status) => {
  switch (status) {
    case 1:
      return 'success';
    case 0:
      return 'danger';
    default:
      return 'info';
  }
};
</script>
