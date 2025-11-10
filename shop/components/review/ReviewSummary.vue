<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <h3 class="text-lg font-semibold mb-4">{{ $t('review.customerReviews') }}</h3>
    
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
    </div>
    
    <div v-else-if="statistics" class="space-y-4">
      <!-- Average Rating -->
      <div class="flex items-center gap-4">
        <div class="text-center">
          <div class="text-4xl font-bold text-gray-900">
            {{ statistics.average_rating?.toFixed(1) || '0.0' }}
          </div>
          <RatingStars :rating="statistics.average_rating || 0" />
          <div class="text-sm text-gray-500 mt-1">
            {{ statistics.review_count || 0 }} {{ $t('review.reviews') }}
          </div>
        </div>
        
        <!-- Rating Distribution -->
        <div class="flex-1 space-y-2">
          <div
            v-for="star in [5, 4, 3, 2, 1]"
            :key="star"
            class="flex items-center gap-2"
          >
            <span class="text-sm text-gray-600 w-12">{{ star }} {{ $t('review.star') }}</span>
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div
                class="bg-yellow-400 h-2 rounded-full transition-all"
                :style="{ width: `${getPercentage(star)}%` }"
              ></div>
            </div>
            <span class="text-sm text-gray-500 w-12 text-right">
              {{ getCount(star) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Filter Buttons -->
      <div class="flex flex-wrap gap-2 pt-4 border-t">
        <button
          @click="$emit('filter-rating', null)"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="selectedRating === null 
            ? 'bg-green-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          {{ $t('review.all') }}
        </button>
        <button
          v-for="star in [5, 4, 3, 2, 1]"
          :key="`filter-${star}`"
          @click="$emit('filter-rating', star)"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="selectedRating === star 
            ? 'bg-green-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          {{ star }} <span class="text-yellow-400">★</span>
        </button>
        <button
          @click="$emit('filter-verified', !verifiedOnly)"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors"
          :class="verifiedOnly 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        >
          ✓ {{ $t('review.verifiedPurchase') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import RatingStars from './RatingStars.vue'

interface ReviewStatistics {
  average_rating: number
  review_count: number
  rating_distribution: Record<number, number>
  rating_percentages?: Record<number, number>
}

interface Props {
  statistics: ReviewStatistics | null
  loading?: boolean
  selectedRating?: number | null
  verifiedOnly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  selectedRating: null,
  verifiedOnly: false
})

defineEmits<{
  'filter-rating': [rating: number | null]
  'filter-verified': [enabled: boolean]
}>()

const getCount = (star: number) => {
  return props.statistics?.rating_distribution?.[star] || 0
}

const getPercentage = (star: number) => {
  if (!props.statistics?.rating_percentages) return 0
  return props.statistics.rating_percentages[star] || 0
}
</script>
