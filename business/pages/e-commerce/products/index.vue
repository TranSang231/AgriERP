<template>
  <div class="p-4 md:p-6 lg:p-8">
    <!-- Sử dụng el-card và el-form để bộ lọc trông chuyên nghiệp hơn -->
    <el-card class="mb-6" shadow="never">
      <template #header>
        <!-- FIX GIAO DIỆN: Dùng flexbox để căn chỉnh icon và chữ -->
        <div class="flex items-center gap-2">
          <el-icon :size="20" class="text-white-600 mt-7"><Search /></el-icon>
          <span class="font-semibold text-lg mt-7">Bộ lọc tìm kiếm</span>
        </div>
      </template>
      <el-form :model="filters" label-position="top">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <!-- Lọc theo tên sản phẩm -->
          <el-form-item label="Tên sản phẩm">
            <!-- FIX LOGIC: Đổi v-model từ filters.name thành filters.keyword -->
            <el-input
              v-model="filters.keyword"
              placeholder="Nhập tên sản phẩm"
              clearable
            />
          </el-form-item>

          <!-- Lọc theo danh mục -->
          <el-form-item label="Danh mục">
            <el-select
              v-model="filters.category_id"
              placeholder="Chọn danh mục"
              clearable
              filterable
              class="w-full"
            >
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name.origin"
                :value="cat.id"
              />
            </el-select>
          </el-form-item>

          <!-- Lọc theo khoảng giá -->
          <el-form-item label="Khoảng giá">
            <div class="flex items-center gap-2 w-full">
              <el-input-number
                v-model="filters.min_price"
                placeholder="Từ"
                :min="0"
                :controls="false"
                class="w-1/2"
              />
              <span class="text-gray-500">-</span>
              <el-input-number
                v-model="filters.max_price"
                placeholder="Đến"
                :min="filters.min_price || 0"
                :controls="false"
                class="w-1/2"
              />
            </div>
          </el-form-item>

          <!-- Lọc theo ngày cập nhật -->
          <el-form-item label="Ngày cập nhật">
            <el-date-picker
              v-model="filters.dateRange"
              type="daterange"
              range-separator="-"
              start-placeholder="Từ ngày"
              end-placeholder="Đến ngày"
              value-format="YYYY-MM-DD"
              class="w-full"
            />
          </el-form-item>
          
          <!-- Nút xóa bộ lọc -->
          <el-form-item label="&nbsp;">
            <el-button @click="resetFilters" type="info" plain class="w-full">Xóa bộ lọc</el-button>
          </el-form-item>
        </div>
      </el-form>
    </el-card>

    <!-- Bảng dữ liệu -->
    <PaginationTable
      ref="productTable"
      :page-size="5"
      :service="ProductService"
      :query-params="computedFilters"
      :canDeleteItems="canEdit"
      :canEditItems="canEdit"
      :canAddItems="canEdit"
      :multipleSelect="canEdit"
      :allowExportToExcel="true"
      :allowExportToJson="true"
    >
        <!-- Các cột của bạn -->
        <el-table-column prop="thumbnail" :label="t('Thumbnail')" min-width="86">
            <template #default="scope">
            <el-image
                v-if="scope.row.thumbnail"
                :src="scope.row.thumbnail"
                fit="cover"
                class="w-16 h-16 rounded-md"
            />
            <div v-else class="w-16 h-16 bg-gray-100 rounded-md flex items-center justify-center text-gray-400">
                <span>No Img</span>
            </div>
            </template>
        </el-table-column>

        <el-table-column prop="name" :label="t('Name')" min-width="150" sortable>
            <template #default="scope">
            <router-link
                :to="`/e-commerce/products/${scope.row.id}`"
                class="text-blue-600 hover:text-blue-800 hover:underline font-medium"
            >
                {{ scope.row.name?.origin }}
            </router-link>
            </template>
        </el-table-column>

        <el-table-column prop="unit" :label="$t('Unit')" min-width="100">
            <template #default="scope">
            {{ scope.row.unit?.origin }}
            </template>
        </el-table-column>

        <el-table-column prop="price" :label="$t('Price')" min-width="120" sortable />

        <el-table-column prop="categories" :label="$t('Categories')" min-width="180">
            <template #default="scope">
            <div class="flex flex-wrap gap-1">
                <el-tag
                type="primary"
                v-for="category in scope.row.categories"
                :key="category.id"
                size="small"
                effect="light"
                >
                {{ category.name ? category.name.origin : '' }}
                </el-tag>
            </div>
            </template>
        </el-table-column>

        <el-table-column prop="updated_at" :label="t('Updated_at')" min-width="180" sortable>
            <template #default="scope">
            {{ formatDateTime(scope.row.updated_at) }}
            </template>
        </el-table-column>
    </PaginationTable>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { Search } from '@element-plus/icons-vue'; // Import icon Search
import ProductService from "@/services/e-commerce/product";
import CategoryService from "@/services/e-commerce/category";
import PaginationTable from "@/components/PaginationTable.vue";
import { formatDateTime } from "~/utils/time";
import { useOauthStore } from "@/stores/oauth";

definePageMeta({
  layout: "ecommerce",
});

const { t } = useI18n();
const canEdit = computed(() => useOauthStore().hasOneOfScopes(["ecommerce:products:edit"]));
const productTable = ref(null);
const categories = ref([]);

// FIX LOGIC: Đổi tên thuộc tính từ `name` thành `keyword`
const filters = reactive({
  keyword: "",
  category_id: null,
  min_price: null,
  max_price: null,
  dateRange: [],
});

// Hàm lấy danh sách categories từ API
const fetchCategories = async () => {
  try {
    const response = await CategoryService.getAll();
    categories.value = response.data || [];
  } catch (error) {
    console.error("Không thể tải danh mục:", error);
  }
};

onMounted(() => {
  fetchCategories();
});

// Xử lý các tham số bộ lọc trước khi truyền xuống PaginationTable
const computedFilters = computed(() => {
  const params = { ...filters };
  if (params.dateRange && params.dateRange.length === 2) {
    params.start_date = params.dateRange[0];
    params.end_date = params.dateRange[1];
  }
  delete params.dateRange;
  Object.keys(params).forEach(key => (params[key] === null || params[key] === '') && delete params[key]);
  return params;
});

// Tự động tải lại bảng khi computedFilters thay đổi
watch(computedFilters, () => {
  if (productTable.value) {
    productTable.value.resetPageAndLoadData();
  }
}, {
  deep: true
});

// Hàm reset bộ lọc
const resetFilters = () => {
  // FIX LOGIC: Reset `keyword` thay vì `name`
  filters.keyword = "";
  filters.category_id = null;
  filters.min_price = null;
  filters.max_price = null;
  filters.dateRange = [];
  if (productTable.value) {
    productTable.value.resetPageAndLoadData();
  }
};
</script>

<style scoped>
/* Tùy chỉnh nhỏ cho các input không có mũi tên tăng giảm */
.el-input-number.no-controls .el-input-number__decrease,
.el-input-number.no-controls .el-input-number__increase {
  display: none;
}
</style>