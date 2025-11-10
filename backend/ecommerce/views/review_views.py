from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404

from ecommerce.models import ProductReview, ReviewHelpful, Product, Customer
from ecommerce.serializers.review_serializer import (
    ProductReviewSerializer,
    ProductReviewCreateSerializer,
    ReviewStatisticsSerializer,
    ProductReviewListSerializer
)
from ecommerce.permissions import IsReviewOwnerOrReadOnly, HasPurchasedProduct


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho ProductReview
    
    Endpoints:
    - GET /reviews/ - List tất cả reviews (có thể filter theo product)
    - GET /reviews/{id}/ - Chi tiết 1 review
    - POST /reviews/ - Tạo review mới (yêu cầu đã mua sản phẩm)
    - PUT/PATCH /reviews/{id}/ - Update review (chỉ owner)
    - DELETE /reviews/{id}/ - Xóa review (chỉ owner)
    - POST /reviews/{id}/mark_helpful/ - Đánh dấu review hữu ích
    - POST /reviews/{id}/unmark_helpful/ - Bỏ đánh dấu helpful
    - GET /reviews/product_statistics/?product_id=X - Thống kê review của sản phẩm
    """
    
    queryset = ProductReview.objects.select_related('customer', 'product', 'order')
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly, HasPurchasedProduct]
    
    def get_serializer_class(self):
        """Chọn serializer phù hợp với action"""
        if self.action in ['create', 'update', 'partial_update']:
            return ProductReviewCreateSerializer
        elif self.action == 'list':
            return ProductReviewListSerializer
        return ProductReviewSerializer
    
    def get_queryset(self):
        """
        Filter queryset
        - Chỉ hiển thị reviews đã được approve (is_approved=True)
        - Có thể filter theo product_id
        - Có thể filter theo rating
        - Có thể sort theo: newest, oldest, highest_rating, lowest_rating, most_helpful
        """
        queryset = self.queryset.filter(is_approved=True)
        
        # Filter theo product
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Filter theo rating
        rating = self.request.query_params.get('rating')
        if rating:
            try:
                queryset = queryset.filter(rating=int(rating))
            except ValueError:
                pass
        
        # Filter theo verified purchase
        verified_only = self.request.query_params.get('verified_only')
        if verified_only and verified_only.lower() == 'true':
            queryset = queryset.filter(is_verified_purchase=True)
        
        # Sorting
        sort_by = self.request.query_params.get('sort', 'newest')
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'highest_rating':
            queryset = queryset.order_by('-rating', '-created_at')
        elif sort_by == 'lowest_rating':
            queryset = queryset.order_by('rating', '-created_at')
        elif sort_by == 'most_helpful':
            queryset = queryset.order_by('-helpful_count', '-created_at')
        
        return queryset
    
    def perform_create(self, serializer):
        """Tạo review - customer được set từ serializer validation"""
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def mark_helpful(self, request, pk=None):
        """
        Đánh dấu review là hữu ích
        POST /reviews/{id}/mark_helpful/
        """
        review = self.get_object()
        
        # Lấy customer
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(
                {'detail': 'Không tìm thấy thông tin khách hàng'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Không cho phép đánh dấu review của chính mình
        if review.customer == customer:
            return Response(
                {'detail': 'Bạn không thể đánh dấu hữu ích review của chính mình'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tạo hoặc lấy ReviewHelpful
        helpful, created = ReviewHelpful.objects.get_or_create(
            review=review,
            customer=customer
        )
        
        if created:
            # Tăng helpful_count
            review.helpful_count += 1
            review.save(update_fields=['helpful_count'])
            
            return Response(
                {'detail': 'Đã đánh dấu review hữu ích', 'helpful_count': review.helpful_count},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Bạn đã đánh dấu review này hữu ích rồi', 'helpful_count': review.helpful_count},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def unmark_helpful(self, request, pk=None):
        """
        Bỏ đánh dấu review hữu ích
        POST /reviews/{id}/unmark_helpful/
        """
        review = self.get_object()
        
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(
                {'detail': 'Không tìm thấy thông tin khách hàng'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Xóa ReviewHelpful nếu tồn tại
        deleted_count, _ = ReviewHelpful.objects.filter(
            review=review,
            customer=customer
        ).delete()
        
        if deleted_count > 0:
            # Giảm helpful_count
            review.helpful_count = max(0, review.helpful_count - 1)
            review.save(update_fields=['helpful_count'])
            
            return Response(
                {'detail': 'Đã bỏ đánh dấu hữu ích', 'helpful_count': review.helpful_count},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Bạn chưa đánh dấu review này hữu ích', 'helpful_count': review.helpful_count},
                status=status.HTTP_200_OK
            )
    
    @action(detail=False, methods=['get'])
    def product_statistics(self, request):
        """
        Lấy thống kê review của sản phẩm
        GET /reviews/product_statistics/?product_id=X
        """
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response(
                {'detail': 'Thiếu product_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Không tìm thấy sản phẩm'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Sử dụng properties từ Product model
        statistics = {
            'average_rating': product.average_rating,
            'review_count': product.review_count,
            'rating_distribution': product.rating_distribution
        }
        
        serializer = ReviewStatisticsSerializer(statistics)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def my_reviews(self, request):
        """
        Lấy danh sách reviews của user hiện tại
        GET /reviews/my_reviews/
        """
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(
                {'detail': 'Không tìm thấy thông tin khách hàng'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reviews = ProductReview.objects.filter(customer=customer).select_related(
            'product', 'order'
        ).order_by('-created_at')
        
        serializer = ProductReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def can_review(self, request):
        """
        Kiểm tra có thể review sản phẩm không
        GET /reviews/can_review/?product_id=X&order_id=Y
        """
        product_id = request.query_params.get('product_id')
        order_id = request.query_params.get('order_id')
        
        if not product_id:
            return Response(
                {'detail': 'Thiếu product_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            customer = Customer.objects.get(user=request.user)
            product = Product.objects.get(id=product_id)
            order = None
            if order_id:
                from ecommerce.models import Order
                order = Order.objects.get(id=order_id, customer=customer)
        except Customer.DoesNotExist:
            return Response(
                {'can_review': False, 'message': 'Không tìm thấy thông tin khách hàng'},
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {'can_review': False, 'message': 'Không tìm thấy sản phẩm'},
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {'can_review': False, 'message': 'Không tìm thấy đơn hàng'},
                status=status.HTTP_200_OK
            )
        
        can_review, message = ProductReview.can_customer_review(
            customer=customer,
            product=product,
            order=order
        )
        
        return Response(
            {'can_review': can_review, 'message': message},
            status=status.HTTP_200_OK
        )
