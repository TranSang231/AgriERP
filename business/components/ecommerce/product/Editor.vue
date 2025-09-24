<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    
    <ModelForm
      :service="productService"
      :default="defaultData"
      :rules="formRules"
      :nestedFields="['name', 'unit', 'description', 'images']"
      :overrideIfFieldNullOrEmpty="overrideFields"
      contentType="multipart/form-data"
      title="Product Information"
    >
      <template #default="{ current, editing }">
        <el-row :gutter="20">
          <!-- Basic Information -->
          <el-col :span="24">
            <el-card class="mb-4">
              <template #header>
                <h3 class="text-lg font-semibold">Basic Information</h3>
              </template>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="Product Name" prop="name.origin" required>
                    <el-input
                      v-model="current.name.origin"
                      placeholder="Enter product name"
                      :disabled="!editing"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="Unit" prop="unit.origin">
                    <el-input
                      v-model="current.unit.origin"
                      placeholder="e.g., kg, piece, box"
                      :disabled="!editing"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="Description" prop="description.origin">
                <el-input
                  v-model="current.description.origin"
                  type="textarea"
                  :rows="4"
                  placeholder="Enter product description"
                  :disabled="!editing"
                />
              </el-form-item>
            </el-card>
          </el-col>

          <!-- Pricing & Stock -->
          <el-col :span="24">
            <el-card class="mb-4">
              <template #header>
                <h3 class="text-lg font-semibold">Pricing & Stock</h3>
              </template>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="Price" prop="price" required>
                    <el-input-number
                      v-model="current.price"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="In Stock" prop="in_stock">
                    <el-input-number
                      v-model="current.in_stock"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="Tax Rate (%)" prop="tax_rate">
                <el-input-number
                  v-model="current.tax_rate"
                  :min="0"
                  :max="100"
                  :precision="2"
                  placeholder="0.00"
                  :disabled="!editing"
                  class="w-full"
                />
              </el-form-item>
            </el-card>
          </el-col>

          <!-- Physical Properties -->
          <el-col :span="24">
            <el-card class="mb-4">
              <template #header>
                <h3 class="text-lg font-semibold">Physical Properties</h3>
              </template>
              
              <el-row :gutter="20">
                <el-col :span="6">
                  <el-form-item label="Weight (kg)" prop="weight">
                    <el-input-number
                      v-model="current.weight"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="6">
                  <el-form-item label="Length (cm)" prop="length">
                    <el-input-number
                      v-model="current.length"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="6">
                  <el-form-item label="Width (cm)" prop="width">
                    <el-input-number
                      v-model="current.width"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="6">
                  <el-form-item label="Height (cm)" prop="height">
                    <el-input-number
                      v-model="current.height"
                      :min="0"
                      :precision="2"
                      placeholder="0.00"
                      :disabled="!editing"
                      class="w-full"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-card>
          </el-col>

          <!-- Images -->
          <el-col :span="24">
            <el-card class="mb-4">
              <template #header>
                <h3 class="text-lg font-semibold">Images</h3>
              </template>
              
              <el-form-item label="Thumbnail" prop="thumbnail">
                <el-upload
                  class="thumbnail-uploader"
                  :auto-upload="false"
                  :on-change="handleThumbnailChange"
                  :before-upload="beforeImageUpload"
                  :disabled="!editing"
                  accept="image/*"
                >
                  <img v-if="current.thumbnail" :src="current.thumbnail" class="thumbnail" />
                  <el-icon v-else class="thumbnail-uploader-icon"><Plus /></el-icon>
                </el-upload>
              </el-form-item>

              <el-form-item label="Product Images" prop="images">
                <el-upload
                  class="images-uploader"
                  :auto-upload="false"
                  :file-list="imageFileList"
                  :on-change="handleImagesChange"
                  :on-remove="handleImageRemove"
                  :before-upload="beforeImageUpload"
                  multiple
                  :disabled="!editing"
                  accept="image/*"
                >
                  <el-button type="primary" :disabled="!editing">Add Images</el-button>
                </el-upload>
              </el-form-item>
            </el-card>
          </el-col>

          <!-- Categories -->
          <el-col :span="24">
            <el-card class="mb-4">
              <template #header>
                <h3 class="text-lg font-semibold">Categories</h3>
              </template>
              
              <el-form-item label="Product Categories" prop="category_ids">
                <el-select
                  v-model="current.category_ids"
                  multiple
                  placeholder="Select categories"
                  :disabled="!editing"
                  class="w-full"
                  :loading="categoriesLoading"
                >
                  <el-option
                    v-for="category in categories"
                    :key="category.id"
                    :label="category.name.origin"
                    :value="category.id"
                  />
                </el-select>
              </el-form-item>
            </el-card>
          </el-col>
        </el-row>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import ModelForm from '@/components/ModelForm.vue'
import BackButton from '@/components/BackButton.vue'
import productService from '@/services/e-commerce/product'
import categoryService from '@/services/e-commerce/category'

const props = defineProps({
  defaultData: {
    type: Object,
    default: () => ({
      name: { origin: null },
      unit: { origin: null },
      price: 0.0,
      in_stock: 0.0,
      categories: [],
      category_ids: [],
      description: { origin: null },
      thumbnail: null,
      images: [],
      weight: 0.0,
      length: 0.0,
      width: 0.0,
      height: 0.0,
      tax_rate: 0.0
    })
  }
})

const categories = ref([])
const categoriesLoading = ref(false)

// Image file list for display
const imageFileList = computed(() => {
  return (props.defaultData?.images || []).map((img, index) => ({
    uid: index,
    name: `image-${index}`,
    url: img.image
  }))
})

// Form validation rules
const formRules = {
  'name.origin': [
    { required: true, message: 'Product name is required', trigger: 'blur' }
  ],
  price: [
    { required: true, message: 'Price is required', trigger: 'blur' },
    { type: 'number', min: 0, message: 'Price must be greater than or equal to 0', trigger: 'blur' }
  ]
}

// Fields to override if null or empty
const overrideFields = {
  name: { origin: '' },
  unit: { origin: '' },
  description: { origin: '' },
  images: []
}

// Image upload handlers
const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('Upload file must be an image!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('Image size must be less than 2MB!')
    return false
  }
  return true
}

const handleThumbnailChange = (file, fileList) => {
  if (file.raw) {
    // Create a preview URL for the thumbnail
    const reader = new FileReader()
    reader.onload = (e) => {
      // This will be handled by the ModelForm component
      // The file will be included in the form data when saving
    }
    reader.readAsDataURL(file.raw)
  }
}

const handleImagesChange = (file, fileList) => {
  // This will be handled by the ModelForm component
  // The files will be included in the form data when saving
}

const handleImageRemove = (file, fileList) => {
  // Remove image from the images array
  // This will be handled by the ModelForm component
}

// Load categories
const loadCategories = async () => {
  try {
    categoriesLoading.value = true
    const response = await categoryService.gets()
    categories.value = (response && response.results) ? response.results : (response || [])
  } catch (error) {
    console.error('Error loading categories:', error)
    ElMessage.error('Failed to load categories')
  } finally {
    categoriesLoading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.thumbnail-uploader .thumbnail {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.thumbnail-uploader .thumbnail-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
}

.images-uploader {
  width: 100%;
}
</style>