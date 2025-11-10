from rest_framework import serializers
from django.db.models import Count, Q
from ecommerce.models import ProductReview, ReviewHelpful, Customer


class ReviewHelpfulSerializer(serializers.ModelSerializer):
    """Serializer cho ReviewHelpful model"""
    
    class Meta:
        model = ReviewHelpful
        fields = ['id', 'customer', 'created_at']
        read_only_fields = ['created_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer để hiển thị review"""
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_avatar = serializers.SerializerMethodField()
    is_verified_purchase = serializers.BooleanField(read_only=True)
    helpful_count = serializers.IntegerField(read_only=True)
    is_helpful_by_user = serializers.SerializerMethodField()
    created_at_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'customer', 'customer_name', 'customer_avatar',
            'order', 'rating', 'title', 'comment', 'images',
            'is_verified_purchase', 'is_approved', 'helpful_count',
            'is_helpful_by_user', 'created_at', 'created_at_display', 'updated_at'
        ]
        read_only_fields = [
            'customer', 'is_verified_purchase', 'is_approved',
            'helpful_count', 'created_at', 'updated_at'
        ]
    
    def get_customer_avatar(self, obj):
        """Lấy avatar của customer (nếu có)"""
        if obj.customer and hasattr(obj.customer, 'avatar') and obj.customer.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.customer.avatar.url)
        return None
    
    def get_is_helpful_by_user(self, obj):
        """Kiểm tra user hiện tại đã đánh dấu helpful chưa"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                customer = Customer.objects.get(user=request.user)
                return ReviewHelpful.objects.filter(
                    review=obj,
                    customer=customer
                ).exists()
            except Customer.DoesNotExist:
                pass
        return False
    
    def get_created_at_display(self, obj):
        """Format ngày tạo để hiển thị"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < timedelta(minutes=1):
            return "Vừa xong"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} phút trước"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} giờ trước"
        elif diff < timedelta(days=30):
            days = diff.days
            return f"{days} ngày trước"
        else:
            return obj.created_at.strftime("%d/%m/%Y")


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer để tạo/update review"""
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'order', 'rating', 'title', 'comment', 'images'
        ]
    
    def validate_rating(self, value):
        """Validate rating trong khoảng 1-5"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating phải từ 1 đến 5 sao")
        return value
    
    def validate_title(self, value):
        """Validate độ dài title"""
        if len(value) > 200:
            raise serializers.ValidationError("Tiêu đề không được quá 200 ký tự")
        return value
    
    def validate_comment(self, value):
        """Validate độ dài comment"""
        if len(value) > 2000:
            raise serializers.ValidationError("Nội dung đánh giá không được quá 2000 ký tự")
        return value
    
    def validate(self, data):
        """Validate toàn bộ dữ liệu"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Bạn phải đăng nhập để đánh giá")
        
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Không tìm thấy thông tin khách hàng")
        
        product = data.get('product')
        order = data.get('order')
        
        # Kiểm tra có thể review không
        can_review, message = ProductReview.can_customer_review(
            customer=customer,
            product=product,
            order=order,
            exclude_review_id=self.instance.id if self.instance else None
        )
        
        if not can_review:
            raise serializers.ValidationError(message)
        
        # Set customer từ request
        data['customer'] = customer
        
        return data
    
    def create(self, validated_data):
        """Tạo review mới"""
        return ProductReview.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Cập nhật review"""
        # Không cho phép thay đổi product, customer, order
        validated_data.pop('product', None)
        validated_data.pop('customer', None)
        validated_data.pop('order', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ReviewStatisticsSerializer(serializers.Serializer):
    """Serializer cho thống kê review của sản phẩm"""
    average_rating = serializers.FloatField()
    review_count = serializers.IntegerField()
    rating_distribution = serializers.DictField()
    
    # Thêm phần trăm cho mỗi rating
    rating_percentages = serializers.SerializerMethodField()
    
    def get_rating_percentages(self, obj):
        """Tính phần trăm cho mỗi rating"""
        total = obj.get('review_count', 0)
        if total == 0:
            return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        distribution = obj.get('rating_distribution', {})
        return {
            rating: round((count / total) * 100, 1)
            for rating, count in distribution.items()
        }


class ProductReviewListSerializer(serializers.ModelSerializer):
    """Serializer rút gọn để list reviews trong product detail"""
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_at_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'customer_name', 'rating', 'title', 'comment',
            'is_verified_purchase', 'helpful_count', 'created_at_display'
        ]
    
    def get_created_at_display(self, obj):
        """Format ngày tạo"""
        return obj.created_at.strftime("%d/%m/%Y")
