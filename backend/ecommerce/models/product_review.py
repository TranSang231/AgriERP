from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from base.models import TimeStampedModel
from .product import Product
from .customer import Customer
from .order import Order


class ProductReview(TimeStampedModel):
    """
    Product review by customers.
    BUSINESS RULE: Only customers who have purchased the product can review it.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        help_text='Order that contains this product (for verification)'
    )
    
    # Rating (1-5 stars)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    
    # Review content
    title = models.CharField(max_length=200, blank=True, help_text='Review title')
    comment = models.TextField(max_length=2000, help_text='Review content')
    
    # Images (store URLs as JSON array)
    images = models.JSONField(default=list, blank=True, help_text='Review images URLs')
    
    # Verification
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text='Customer has purchased this product'
    )
    
    # Moderation
    is_approved = models.BooleanField(default=True, help_text='Review is approved by admin')
    
    # Engagement
    helpful_count = models.IntegerField(default=0, help_text='Number of customers who found this helpful')
    
    class Meta:
        db_table = 'ecommerce_product_reviews'
        ordering = ['-created_at']
        # One review per product per order
        unique_together = [['product', 'customer', 'order']]
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['product', 'rating']),
            models.Index(fields=['customer']),
        ]
    
    def __str__(self):
        return f'{self.customer} - {self.product} - {self.rating}★'
    
    @classmethod
    def can_customer_review(cls, customer, product, order=None):
        """
        Check if customer can review this product.
        Rules:
        1. Must have purchased the product (order completed/delivered)
        2. Can only review once per order
        3. If no specific order, check any completed order with this product
        """
        from .order_item import OrderItem
        from ..constants import OrderStatus
        
        if order:
            # Check specific order
            if order.customer != customer:
                return False, "This is not your order"
            
            if order.order_status not in [OrderStatus.COMPLETED, OrderStatus.SHIPPED]:
                return False, "Order must be completed or shipped to review"
            
            # Check if product is in this order
            has_product = OrderItem.objects.filter(
                order=order,
                product=product
            ).exists()
            
            if not has_product:
                return False, "Product not found in this order"
            
            # Check if already reviewed
            already_reviewed = cls.objects.filter(
                product=product,
                customer=customer,
                order=order
            ).exists()
            
            if already_reviewed:
                return False, "You have already reviewed this product for this order"
            
            return True, "Can review"
        
        else:
            # Check any completed order with this product
            from django.db.models import Q
            
            completed_orders = Order.objects.filter(
                customer=customer,
                order_status__in=[OrderStatus.COMPLETED, OrderStatus.SHIPPED]
            ).filter(
                items__product=product
            ).distinct()
            
            if not completed_orders.exists():
                return False, "You must purchase this product before reviewing"
            
            # Check if already reviewed for all orders
            reviewed_orders = cls.objects.filter(
                product=product,
                customer=customer
            ).values_list('order_id', flat=True)
            
            # Find orders not yet reviewed
            available_orders = completed_orders.exclude(id__in=reviewed_orders)
            
            if not available_orders.exists():
                return False, "You have already reviewed this product for all your purchases"
            
            return True, "Can review"
    
    def mark_helpful(self):
        """Increment helpful count"""
        self.helpful_count += 1
        self.save(update_fields=['helpful_count', 'updated_at'])
    
    def save(self, *args, **kwargs):
        # Auto-verify purchase if order is provided
        if self.order and self.order.customer == self.customer:
            from .order_item import OrderItem
            if OrderItem.objects.filter(order=self.order, product=self.product).exists():
                self.is_verified_purchase = True
        
        super().save(*args, **kwargs)


class ReviewHelpful(TimeStampedModel):
    """
    Track which customers found a review helpful.
    Prevents duplicate helpful marks.
    """
    review = models.ForeignKey(
        ProductReview,
        on_delete=models.CASCADE,
        related_name='helpful_marks'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='helpful_reviews'
    )
    is_helpful = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'ecommerce_review_helpful'
        unique_together = [['review', 'customer']]
        indexes = [
            models.Index(fields=['review', 'customer']),
        ]
    
    def __str__(self):
        return f'{self.customer} found {self.review} helpful'
