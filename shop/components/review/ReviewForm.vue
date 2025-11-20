<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <h3 class="text-lg font-semibold mb-4">
      {{ isEdit ? 'Sửa đánh giá' : 'Viết đánh giá' }}
    </h3>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Rating -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Đánh giá của bạn <span class="text-red-500">*</span>
        </label>
        <div class="flex items-center gap-2">
          <button
            v-for="star in 5"
            :key="star"
            type="button"
            @click="formData.rating = star"
            @mouseenter="hoverRating = star"
            @mouseleave="hoverRating = 0"
            class="focus:outline-none transition-transform hover:scale-110"
          >
            <svg
              class="w-8 h-8"
              :class="star <= (hoverRating || formData.rating) ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
          <span class="ml-2 text-sm text-gray-600">
            {{ getRatingText(formData.rating) }}
          </span>
        </div>
        <p v-if="errors.rating" class="mt-1 text-sm text-red-600">{{ errors.rating }}</p>
      </div>
      
      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
          Tiêu đề <span class="text-red-500">*</span>
        </label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          placeholder="Nhập tiêu đề đánh giá"
          maxlength="200"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.title }"
        />
        <div class="flex justify-between mt-1">
          <p v-if="errors.title" class="text-sm text-red-600">{{ errors.title }}</p>
          <p class="text-sm text-gray-500 ml-auto">{{ formData.title.length }}/200</p>
        </div>
      </div>
      
      <!-- Comment -->
      <div>
        <label for="comment" class="block text-sm font-medium text-gray-700 mb-2">
          Nội dung <span class="text-red-500">*</span>
        </label>
        <textarea
          id="comment"
          v-model="formData.comment"
          rows="5"
          placeholder="Chia sẻ cảm nhận của bạn về sản phẩm..."
          maxlength="2000"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
          :class="{ 'border-red-500': errors.comment }"
        ></textarea>
        <div class="flex justify-between mt-1">
          <p v-if="errors.comment" class="text-sm text-red-600">{{ errors.comment }}</p>
          <p class="text-sm text-gray-500 ml-auto">{{ formData.comment.length }}/2000</p>
        </div>
      </div>
      
      <!-- Images (Optional - future enhancement) -->
      <!-- <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ $t('review.images') }}
        </label>
        <div class="flex items-center gap-2">
          <button type="button" class="px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 transition-colors">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
      </div> -->
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-600">{{ errorMessage }}</p>
      </div>
      
      <!-- Actions -->
      <div class="flex gap-3 pt-4">
        <button
          type="submit"
          :disabled="submitting"
          class="flex-1 px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="submitting" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Đang gửi...
          </span>
          <span v-else>
            {{ isEdit ? 'Cập nhật đánh giá' : 'Gửi đánh giá' }}
          </span>
        </button>
        <button
          v-if="onCancel"
          type="button"
          @click="onCancel"
          :disabled="submitting"
          class="px-6 py-3 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
        >
          Hủy
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'

interface ReviewFormData {
  rating: number
  title: string
  comment: string
  images?: string[]
}

interface Props {
  initialData?: Partial<ReviewFormData>
  isEdit?: boolean
  submitting?: boolean
  errorMessage?: string
  onCancel?: () => void
}

const props = withDefaults(defineProps<Props>(), {
  isEdit: false,
  submitting: false,
  errorMessage: ''
})

const emit = defineEmits<{
  submit: [data: ReviewFormData]
}>()

const hoverRating = ref(0)

const formData = reactive<ReviewFormData>({
  rating: props.initialData?.rating || 0,
  title: props.initialData?.title || '',
  comment: props.initialData?.comment || '',
  images: props.initialData?.images || []
})

const errors = reactive({
  rating: '',
  title: '',
  comment: ''
})

// Watch for initialData changes
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.rating = newData.rating || 0
    formData.title = newData.title || ''
    formData.comment = newData.comment || ''
    formData.images = newData.images || []
  }
}, { immediate: true, deep: true })

const getRatingText = (rating: number) => {
  const texts = [
    '',
    'Rất tệ',
    'Tệ',
    'Bình thường',
    'Tốt',
    'Rất tốt'
  ]
  return texts[rating] || ''
}

const validate = () => {
  let isValid = true
  
  // Reset errors
  errors.rating = ''
  errors.title = ''
  errors.comment = ''
  
  if (!formData.rating || formData.rating < 1 || formData.rating > 5) {
    errors.rating = 'Vui lòng chọn số sao đánh giá'
    isValid = false
  }
  
  if (!formData.title.trim()) {
    errors.title = 'Vui lòng nhập tiêu đề'
    isValid = false
  } else if (formData.title.length > 200) {
    errors.title = 'Tiêu đề không được quá 200 ký tự'
    isValid = false
  }
  
  if (!formData.comment.trim()) {
    errors.comment = 'Vui lòng nhập nội dung đánh giá'
    isValid = false
  } else if (formData.comment.length > 2000) {
    errors.comment = 'Nội dung không được quá 2000 ký tự'
    isValid = false
  }
  
  return isValid
}

const handleSubmit = () => {
  if (validate()) {
    emit('submit', { ...formData })
  }
}
</script>
