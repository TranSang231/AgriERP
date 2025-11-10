<template>
  <div class="space-y-4">
    <!-- Sort Options -->
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold">
        {{ reviews.length }} {{ $t('review.reviews') }}
      </h3>
      <select
        :value="sortBy"
        @change="$emit('sort-change', ($event.target as HTMLSelectElement).value)"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
      >
        <option value="newest">{{ $t('review.newest') }}</option>
        <option value="oldest">{{ $t('review.oldest') }}</option>
        <option value="highest_rating">{{ $t('review.highestRating') }}</option>
        <option value="lowest_rating">{{ $t('review.lowestRating') }}</option>
        <option value="most_helpful">{{ $t('review.mostHelpful') }}</option>
      </select>
    </div>
    
    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="reviews.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
      </svg>
      <p class="mt-2 text-gray-500">{{ $t('review.noReviews') }}</p>
    </div>
    
    <!-- Review List -->
    <div v-else class="space-y-4">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
      >
        <!-- Header -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
              <span class="text-green-700 font-semibold text-lg">
                {{ review.customer_name?.charAt(0) || 'U' }}
              </span>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-900">{{ review.customer_name }}</span>
                <span v-if="review.is_verified_purchase" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  ✓ {{ $t('review.verifiedPurchase') }}
                </span>
              </div>
              <div class="flex items-center gap-2 mt-1">
                <RatingStars :rating="review.rating" />
                <span class="text-sm text-gray-500">{{ review.created_at_display }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Content -->
        <div class="space-y-2">
          <h4 v-if="review.title" class="font-semibold text-gray-900">{{ review.title }}</h4>
          <p class="text-gray-700 whitespace-pre-wrap">{{ review.comment }}</p>
          
          <!-- Images -->
          <div v-if="review.images && review.images.length > 0" class="flex gap-2 mt-3">
            <img
              v-for="(image, idx) in review.images"
              :key="idx"
              :src="image"
              :alt="`Review image ${idx + 1}`"
              class="w-20 h-20 object-cover rounded-lg cursor-pointer hover:opacity-75 transition-opacity"
              @click="$emit('image-click', image)"
            />
          </div>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center gap-4 mt-4 pt-4 border-t border-gray-100">
          <button
            @click="$emit('helpful-click', review)"
            class="flex items-center gap-2 text-sm transition-colors"
            :class="review.is_helpful_by_user 
              ? 'text-green-600 font-medium' 
              : 'text-gray-600 hover:text-green-600'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
            </svg>
            {{ $t('review.helpful') }} ({{ review.helpful_count || 0 }})
          </button>
          
          <button
            v-if="canEdit(review)"
            @click="$emit('edit-click', review)"
            class="text-sm text-gray-600 hover:text-green-600 transition-colors"
          >
            {{ $t('review.edit') }}
          </button>
          
          <button
            v-if="canDelete(review)"
            @click="$emit('delete-click', review)"
            class="text-sm text-gray-600 hover:text-red-600 transition-colors"
          >
            {{ $t('review.delete') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Load More -->
    <div v-if="hasMore && !loading" class="text-center pt-4">
      <button
        @click="$emit('load-more')"
        class="px-6 py-3 bg-white border-2 border-green-600 text-green-600 font-medium rounded-lg hover:bg-green-50 transition-colors"
      >
        {{ $t('review.loadMore') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import RatingStars from './RatingStars.vue'

interface Review {
  id: number
  customer_name: string
  customer_avatar?: string
  rating: number
  title?: string
  comment: string
  images?: string[]
  is_verified_purchase: boolean
  helpful_count: number
  is_helpful_by_user?: boolean
  created_at_display: string
  customer?: number
}

interface Props {
  reviews: Review[]
  loading?: boolean
  sortBy?: string
  hasMore?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
  sortBy: 'newest',
  hasMore: false
})

defineEmits<{
  'sort-change': [value: string]
  'helpful-click': [review: Review]
  'edit-click': [review: Review]
  'delete-click': [review: Review]
  'image-click': [image: string]
  'load-more': []
}>()

const authStore = useAuthStore()

const canEdit = (review: Review) => {
  // Check if current user is the review owner
  return authStore.isAuthenticated && authStore.user?.customer_id === review.customer
}

const canDelete = (review: Review) => {
  return canEdit(review)
}
</script>
