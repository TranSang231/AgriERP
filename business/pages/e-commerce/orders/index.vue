<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <PaginationTable
      :page-size="5"
      :service="OrderService"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
      :searchable="true"
    >
      <el-table-column prop="customer_name" :label="t('Customer')" min-width="150" />
      <el-table-column prop="payment_method" :label="$t('Payment_method')" min-width="180">
        <template
          v-if="constantsStore && constantsStore.paymentMethods"
          #default="scope"
        >
          {{ constantsStore.paymentMethodDescription(scope.row.payment_method) }}
        </template>
      </el-table-column>
      <el-table-column prop="payment_status" :label="$t('Payment_status')" min-width="180">
        <template
          v-if="constantsStore && constantsStore.paymentStatuses"
          #default="scope"
        >
          {{ constantsStore.paymentStatusDescription(scope.row.payment_status) }}
        </template>
      </el-table-column>
      <el-table-column prop="shipping_status" :label="$t('Shipping_status')" min-width="180">
        <template
          v-if="constantsStore && constantsStore.shippingStatuses"
          #default="scope"
        >
          {{ constantsStore.shippingStatusDescription(scope.row.shipping_status) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="updated_at"
        :label="t('Updated_at')"
        min-width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.updated_at) }}
        </template>
      </el-table-column>
    </PaginationTable>
  </div>
</template>

<script setup>
import OrderService from "@/services/e-commerce/order";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";
import { useConstantsStore } from '@/stores/constants';
import ConstantsService from '@/services/constants';
definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const constantsStore = useConstantsStore();
const fetchData = () => {
  ConstantsService.fetch([
    "payment_methods",
    "payment_statuses",
    "shipping_statuses"
  ]);
};

const canEdit = computed(() => oauthStore.hasOneOfScopes(["ecommerce:orders:edit"]))

onMounted(() => {
  fetchData();
});
</script>
