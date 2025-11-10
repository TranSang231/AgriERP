import { useApi } from '~/services/api'

export interface Review {
  id: number
  product: number | string  // Support UUID
  customer: number
  customer_name: string
  customer_avatar?: string
  order?: number | string  // Support UUID
  rating: number
  title: string
  comment: string
  images?: string[]
  is_verified_purchase: boolean
  is_approved: boolean
  helpful_count: number
  is_helpful_by_user?: boolean
  created_at: string
  created_at_display: string
  updated_at: string
}

export interface ReviewStatistics {
  average_rating: number
  review_count: number
  rating_distribution: Record<number, number>
  rating_percentages: Record<number, number>
}

export interface CreateReviewData {
  product: number | string  // Support UUID
  order: number | string  // Support UUID
  rating: number
  title: string
  comment: string
  images?: string[]
}

export const useReviewService = () => {
  const { request } = useApi()
  
  /**
   * Get reviews for a product
   */
  const getProductReviews = async (params: {
    product_id: number | string  // Support UUID
    rating?: number
    verified_only?: boolean
    sort?: 'newest' | 'oldest' | 'highest_rating' | 'lowest_rating' | 'most_helpful'
  }) => {
    const data = await request<Review[]>('/reviews', {
      method: 'GET',
      params
    })
    return data || []
  }
  
  /**
   * Get review statistics for a product
   */
  const getProductStatistics = async (productId: number | string) => {
    const data = await request<ReviewStatistics>('/reviews/product_statistics', {
      method: 'GET',
      params: { product_id: productId }
    })
    return data
  }
  
  /**
   * Get a single review
   */
  const getReview = async (reviewId: number) => {
    const data = await request<Review>(`/reviews/${reviewId}`, {
      method: 'GET'
    })
    return data
  }
  
  /**
   * Create a new review
   */
  const createReview = async (reviewData: CreateReviewData) => {
    const data = await request<Review>('/reviews', {
      method: 'POST',
      body: reviewData
    })
    return data
  }
  
  /**
   * Update a review
   */
  const updateReview = async (reviewId: number, reviewData: Partial<CreateReviewData>) => {
    const data = await request<Review>(`/reviews/${reviewId}`, {
      method: 'PATCH',
      body: reviewData
    })
    return data
  }
  
  /**
   * Delete a review
   */
  const deleteReview = async (reviewId: number) => {
    const data = await request(`/reviews/${reviewId}`, {
      method: 'DELETE'
    })
    return data
  }
  
  /**
   * Mark review as helpful
   */
  const markHelpful = async (reviewId: number) => {
    const data = await request(`/reviews/${reviewId}/mark_helpful`, {
      method: 'POST'
    })
    return data
  }
  
  /**
   * Unmark review as helpful
   */
  const unmarkHelpful = async (reviewId: number) => {
    const data = await request(`/reviews/${reviewId}/unmark_helpful`, {
      method: 'POST'
    })
    return data
  }
  
  /**
   * Get my reviews
   */
  const getMyReviews = async () => {
    const data = await request<Review[]>('/reviews/my_reviews', {
      method: 'GET'
    })
    return data || []
  }
  
  /**
   * Check if can review a product
   */
  const canReview = async (productId: number | string, orderId?: number | string) => {
    const data = await request<{ can_review: boolean; message: string }>('/reviews/can_review', {
      method: 'GET',
      params: {
        product_id: productId,
        ...(orderId && { order_id: orderId })
      }
    })
    return data
  }
  
  return {
    getProductReviews,
    getProductStatistics,
    getReview,
    createReview,
    updateReview,
    deleteReview,
    markHelpful,
    unmarkHelpful,
    getMyReviews,
    canReview
  }
}
