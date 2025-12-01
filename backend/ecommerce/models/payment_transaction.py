from django.db import models
from base.models import TimeStampedModel
from django.utils import timezone
from .order import Order


class PaymentTransactionType(models.TextChoices):
    """Payment transaction types"""
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    VNPAY = 'vnpay', 'VNPay'
    MOMO = 'momo', 'MoMo'
    ZALOPAY = 'zalopay', 'ZaloPay'
    COD = 'cod', 'Cash on Delivery'
    REFUND = 'refund', 'Refund'


class PaymentTransactionStatus(models.TextChoices):
    """Payment transaction statuses"""
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'
    REFUNDED = 'refunded', 'Refunded'


class PaymentTransaction(TimeStampedModel):
    """
    Model to store payment transaction history for orders
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        help_text="Order associated with this transaction"
    )
    transaction_type = models.CharField(
        max_length=50,
        choices=PaymentTransactionType.choices,
        default=PaymentTransactionType.BANK_TRANSFER,
        help_text="Type of payment transaction"
    )
    transaction_status = models.CharField(
        max_length=50,
        choices=PaymentTransactionStatus.choices,
        default=PaymentTransactionStatus.PENDING,
        help_text="Status of the transaction"
    )
    amount = models.FloatField(
        default=0.0,
        help_text="Transaction amount"
    )
    currency = models.CharField(
        max_length=10,
        default='VND',
        help_text="Currency code (e.g., VND, USD)"
    )
    bank_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Bank transaction reference number"
    )
    gateway_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text="Transaction ID from payment gateway (VNPay, MoMo, ZaloPay, etc.)"
    )
    bank_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Bank code (for VNPay)"
    )
    card_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Card type (for VNPay)"
    )
    gateway_response = models.JSONField(
        blank=True,
        null=True,
        help_text="Response data from payment gateway"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the transaction"
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the transaction was processed"
    )

    class Meta:
        db_table = "ecommerce_payment_transactions"
        ordering = ["-created_at"]
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency} - {self.transaction_status} - Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Auto-set processed_at when status changes to completed
        if self.transaction_status == PaymentTransactionStatus.COMPLETED and not self.processed_at:
            from django.utils import timezone
            self.processed_at = timezone.now()
        super().save(*args, **kwargs)

