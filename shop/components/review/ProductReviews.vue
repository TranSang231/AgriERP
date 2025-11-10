<template>
  <div class="space-y-6">
    <!-- Review Summary -->
    <ReviewSummary
      :statistics="statistics"
      :loading="loadingStatistics"
      :selected-rating="filters.rating"
      :verified-only="filters.verified_only"
      @filter-rating="handleFilterRating"
      @filter-verified="handleFilterVerified"
    />
    
    <!-- Write Review Button (if user can review) -->
    <div v-if="canWriteReview && !showReviewForm" class="flex justify-center">
      <button
        @click="showReviewForm = true"
        class="px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Viết đánh giá
      </button>
    </div>
    
    <!-- Review Form -->
    <ReviewForm
      v-if="showReviewForm"
      :initial-data="editingReview"
      :is-edit="!!editingReview"
      :submitting="submittingReview"
      :error-message="reviewError"
      :on-cancel="handleCancelReview"
      @submit="handleSubmitReview"
    />
    
    <!-- Review List -->
    <ReviewList
      :reviews="reviews"
      :loading="loadingReviews"
      :sort-by="filters.sort"
      :has-more="hasMore"
      @sort-change="handleSortChange"
      @helpful-click="handleHelpfulClick"
      @edit-click="handleEditClick"
      @delete-click="handleDeleteClick"
      @image-click="handleImageClick"
      @load-more="loadMore"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useReviewService, type Review, type ReviewStatistics, type CreateReviewData } from '~/services/reviewService'
import ReviewSummary from './ReviewSummary.vue'
import ReviewList from './ReviewList.vue'
import ReviewForm from './ReviewForm.vue'

interface Props {
  productId: number | string  // Support both number and UUID
}

const props = defineProps<Props>()

const authStore = useAuthStore()
const reviewService = useReviewService()

// State
const statistics = ref<ReviewStatistics | null>(null)
const reviews = ref<Review[]>([])
const loadingStatistics = ref(false)
const loadingReviews = ref(false)
const submittingReview = ref(false)
const reviewError = ref('')
const showReviewForm = ref(false)
const editingReview = ref<Review | null>(null)
const canWriteReview = ref(false)
const hasMore = ref(false)

const filters = ref({
  rating: null as number | null,
  verified_only: false,
  sort: 'newest' as string
})

// Load statistics
const loadStatistics = async () => {
  loadingStatistics.value = true
  try {
    const data = await reviewService.getProductStatistics(props.productId)
    console.log('Statistics API response:', data)
    console.log('Type of statistics:', typeof data)
    
    // Handle both direct object and wrapped response
    if (data && typeof data === 'object') {
      // Check if it's wrapped in a 'data' or 'results' property
      if ('results' in data || 'data' in data) {
        statistics.value = (data as any).results || (data as any).data
      } else {
        statistics.value = data
      }
    } else {
      statistics.value = null
    }
    console.log('Final statistics:', statistics.value)
  } catch (error) {
    console.error('Failed to load review statistics:', error)
    statistics.value = null
  } finally {
    loadingStatistics.value = false
  }
}

// Load reviews
const loadReviews = async () => {
  loadingReviews.value = true
  try {
    const data = await reviewService.getProductReviews({
      product_id: props.productId,
      ...(filters.value.rating && { rating: filters.value.rating }),
      verified_only: filters.value.verified_only,
      sort: filters.value.sort as any
    })
    console.log('Raw API response:', data)
    console.log('Type of data:', typeof data)
    console.log('Is array:', Array.isArray(data))
    
    // Check if data has 'results' property (paginated response)
    if (data && typeof data === 'object' && 'results' in data) {
      reviews.value = data.results || []
      console.log('Using paginated results:', reviews.value.length)
    } else if (Array.isArray(data)) {
      reviews.value = data
      console.log('Using array data:', reviews.value.length)
    } else {
      reviews.value = []
      console.log('No valid data, setting empty array')
    }
    
    hasMore.value = false // TODO: Implement pagination
  } catch (error) {
    console.error('Failed to load reviews:', error)
    reviews.value = []
  } finally {
    loadingReviews.value = false
  }
}

// Check if user can write review
const checkCanReview = async () => {
  console.log('🔍 Checking can review - isAuthenticated:', authStore.isAuthenticated)
  
  if (!authStore.isAuthenticated) {
    canWriteReview.value = false
    console.log('❌ Not authenticated, cannot write review')
    return
  }
  
  try {
    const result = await reviewService.canReview(props.productId)
    canWriteReview.value = result?.can_review || false
    console.log('✅ Can review result:', result)
    console.log('   canWriteReview:', canWriteReview.value)
  } catch (error) {
    console.warn('⚠️ Failed to check can_review permission (non-critical):', error)
    canWriteReview.value = false
  }
}

// Handlers
const handleFilterRating = (rating: number | null) => {
  filters.value.rating = rating
  loadReviews()
}

const handleFilterVerified = (enabled: boolean) => {
  filters.value.verified_only = enabled
  loadReviews()
}

const handleSortChange = (sort: string) => {
  filters.value.sort = sort
  loadReviews()
}

const handleSubmitReview = async (data: CreateReviewData) => {
  submittingReview.value = true
  reviewError.value = ''
  
  try {
    if (editingReview.value) {
      // Update existing review
      await reviewService.updateReview(editingReview.value.id, data)
    } else {
      // Create new review
      const reviewData = {
        ...data,
        product: props.productId, // Add product ID
        // order: null // Optional: can add order selection later
      }
      console.log('📝 Creating review with data:', reviewData)
      await reviewService.createReview(reviewData)
    }
    
    // Reload data
    await Promise.all([
      loadStatistics(),
      loadReviews(),
      checkCanReview()
    ])
    
    // Close form
    showReviewForm.value = false
    editingReview.value = null
    
    // Show success message
    // TODO: Add toast notification
    alert(editingReview.value ? 'Cập nhật đánh giá thành công!' : 'Tạo đánh giá thành công!')
  } catch (error: any) {
    reviewError.value = error.message || 'Có lỗi xảy ra, vui lòng thử lại'
    console.error('❌ Review submission error:', error)
  } finally {
    submittingReview.value = false
  }
}

const handleCancelReview = () => {
  showReviewForm.value = false
  editingReview.value = null
  reviewError.value = ''
}

const handleEditClick = (review: Review) => {
  editingReview.value = review
  showReviewForm.value = true
}

const handleDeleteClick = async (review: Review) => {
  if (!confirm('Bạn có chắc chắn muốn xóa đánh giá này?')) {
    return
  }
  
  try {
    await reviewService.deleteReview(review.id)
    
    // Reload data
    await Promise.all([
      loadStatistics(),
      loadReviews(),
      checkCanReview()
    ])
    
    alert('Xóa đánh giá thành công!')
  } catch (error: any) {
    alert(error.message || 'Có lỗi xảy ra khi xóa đánh giá')
  }
}

const handleHelpfulClick = async (review: Review) => {
  if (!authStore.isAuthenticated) {
    // TODO: Show login modal
    alert('Vui lòng đăng nhập để đánh dấu hữu ích')
    return
  }
  
  try {
    if (review.is_helpful_by_user) {
      await reviewService.unmarkHelpful(review.id)
    } else {
      await reviewService.markHelpful(review.id)
    }
    
    // Reload reviews to update helpful count
    await loadReviews()
  } catch (error: any) {
    alert(error.message || 'Có lỗi xảy ra')
  }
}

const handleImageClick = (image: string) => {
  // TODO: Open image viewer/lightbox
  window.open(image, '_blank')
}

const loadMore = () => {
  // TODO: Implement pagination
  console.log('Load more reviews')
}

// Initialize
onMounted(async () => {
  await Promise.all([
    loadStatistics(),
    loadReviews(),
    checkCanReview()
  ])
})

// Watch auth changes
watch(() => authStore.isAuthenticated, () => {
  checkCanReview()
})
</script>
