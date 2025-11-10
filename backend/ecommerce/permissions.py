from rest_framework import permissions
from ecommerce.models import Customer, Order
from ecommerce.constants.order_status import OrderStatus


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission cho phép:
    - Ai cũng có thể xem (read)
    - Chỉ owner của review mới có thể edit/delete
    """
    
    def has_permission(self, request, view):
        # Read permissions cho tất cả
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions yêu cầu authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permissions cho tất cả
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions chỉ cho owner
        try:
            customer = Customer.objects.get(user=request.user)
            return obj.customer == customer
        except Customer.DoesNotExist:
            return False


class HasPurchasedProduct(permissions.BasePermission):
    """
    Permission kiểm tra customer đã mua sản phẩm chưa
    Chỉ áp dụng cho create review
    """
    
    message = "Bạn phải mua sản phẩm này trước khi đánh giá"
    
    def has_permission(self, request, view):
        # Chỉ check khi create review
        if view.action != 'create':
            return True
        
        if not request.user or not request.user.is_authenticated:
            self.message = "Bạn phải đăng nhập để đánh giá"
            return False
        
        try:
            customer = Customer.objects.get(user=request.user)
            product_id = request.data.get('product')
            
            if not product_id:
                self.message = "Thiếu thông tin sản phẩm"
                return False
            
            # Kiểm tra có đơn hàng nào chứa sản phẩm và đã hoàn thành/đang giao
            has_purchased = Order.objects.filter(
                customer=customer,
                order_status__in=[OrderStatus.COMPLETED, OrderStatus.SHIPPED],
                items__product_id=product_id
            ).exists()
            
            if not has_purchased:
                self.message = "Bạn cần mua và nhận sản phẩm này trước khi đánh giá"
                return False
            
            return True
            
        except Customer.DoesNotExist:
            self.message = "Không tìm thấy thông tin khách hàng"
            return False
        except Exception as e:
            self.message = f"Lỗi khi kiểm tra quyền: {str(e)}"
            return False


class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Permission cho phép:
    - Ai cũng có thể xem
    - Chỉ customer mới có thể thao tác
    """
    
    def has_permission(self, request, view):
        # Read permissions cho tất cả
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions yêu cầu là customer
        if not request.user or not request.user.is_authenticated:
            return False
        
        try:
            Customer.objects.get(user=request.user)
            return True
        except Customer.DoesNotExist:
            return False
