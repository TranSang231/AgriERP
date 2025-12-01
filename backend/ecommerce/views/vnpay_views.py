"""
VNPay Payment Views
Handles payment creation, callback (IPN), and return URL
"""
import hashlib
import hmac
import logging
import urllib.parse
from datetime import datetime
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from ecommerce.models import Order, PaymentTransaction
from ecommerce.vnpay import VNPayPayment, VNPayConfig

logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    """Get client IP address from request - IPv4 only for VNPay"""
    # TEMPORARY FIX: Use public IP to test Code 99 error
    # VNPay may require real public IP instead of 127.0.0.1
    logger.info('[VNPAY] Using hardcoded public IP: 13.160.92.202')
    return '13.160.92.202'
    
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0].strip()
    # else:
    #     ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    # 
    # # VNPay only accepts IPv4, reject IPv6
    # if ':' in ip and '.' not in ip:
    #     # This is IPv6, return default IPv4
    #     logger.warning(f'[VNPAY] IPv6 detected ({ip}), using 127.0.0.1 instead')
    #     return '127.0.0.1'
    # 
    # return ip


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    """
    Create VNPay payment URL for an order
    
    Request body:
    {
        "order_id": 123,
        "bank_code": "NCB",  # Optional
        "language": "vn"      # Optional, default: vn
    }
    
    Returns:
    {
        "payment_url": "https://sandbox.vnpayment.vn/...",
        "order_id": 123
    }
    """
    try:
        order_id = request.data.get('order_id')
        bank_code = request.data.get('bank_code', '')
        language = request.data.get('language', VNPayConfig.LANGUAGE_VN)
        
        if not order_id:
            return Response(
                {'error': 'order_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get order
        try:
            order = Order.objects.select_related('customer').get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user owns this order
        print(f"[VNPAY] Order customer: {order.customer}")
        print(f"[VNPAY] Order customer.user_id: {order.customer.user_id if order.customer else 'No customer'} (type: {type(order.customer.user_id).__name__})")
        print(f"[VNPAY] Request user: {request.user}")
        print(f"[VNPAY] Request user.id: {request.user.id} (type: {type(request.user.id).__name__})")
        
        if not order.customer or str(order.customer.user_id) != str(request.user.id):
            print(f"[VNPAY] Permission denied - customer.user_id={order.customer.user_id if order.customer else None}, request.user.id={request.user.id}")
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if order is already paid
        if hasattr(order, 'payment_status') and order.payment_status == 'paid':
            return Response(
                {'error': 'Order already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total amount from order items
        from django.db.models import Sum
        total_amount = order.items.aggregate(total=Sum('amount'))['total'] or 0
        
        if total_amount <= 0:
            return Response(
                {'error': 'Order has no items or invalid amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Build VNPay payment request
        vnp = VNPayPayment()
        vnp.request_data['vnp_Version'] = VNPayConfig.VERSION
        vnp.request_data['vnp_Command'] = VNPayConfig.COMMAND_PAY
        vnp.request_data['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.request_data['vnp_Amount'] = str(int(total_amount * 100))  # Convert to VNPay format (x100)
        vnp.request_data['vnp_CurrCode'] = VNPayConfig.CURRENCY_VND
        vnp.request_data['vnp_TxnRef'] = str(order_id)
        vnp.request_data['vnp_OrderInfo'] = f'Thanh toan don hang {order_id}'
        vnp.request_data['vnp_OrderType'] = 'other'
        vnp.request_data['vnp_Locale'] = language
        
        if bank_code:
            vnp.request_data['vnp_BankCode'] = bank_code
        
        vnp.request_data['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.request_data['vnp_IpAddr'] = get_client_ip(request)
        vnp.request_data['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
        
        # Temporarily disable IPN URL to test Code 99
        # Add IPN URL if configured
        # if settings.VNPAY_IPN_URL:
        #     vnp.request_data['vnp_IpnUrl'] = settings.VNPAY_IPN_URL
        
        # Log request data for debugging
        logger.info(f'[VNPAY] Creating payment for order {order_id}')
        logger.info(f'[VNPAY] Request data: {vnp.request_data}')
        logger.info(f'[VNPAY] Return URL: {settings.VNPAY_RETURN_URL}')
        logger.info(f'[VNPAY] TMN Code: {settings.VNPAY_TMN_CODE}')
        
        # Generate payment URL
        payment_url = vnp.get_payment_url(
            settings.VNPAY_PAYMENT_URL,
            settings.VNPAY_HASH_SECRET_KEY
        )
        
        logger.info(f'[VNPAY] Generated payment URL: {payment_url}')
        
        # 🔍 DEBUG: Print FULL URL to console for manual testing
        print("\n" + "="*100)
        print("🔗 VNPAY PAYMENT URL - COPY & PASTE VÀO BROWSER ĐỂ TEST:")
        print("="*100)
        print(payment_url)
        print("="*100 + "\n")
        
        return Response({
            'payment_url': payment_url,
            'order_id': order_id
        })
        
    except Exception as e:
        logger.error(f'Error creating VNPay payment: {str(e)}')
        return Response(
            {'error': 'Failed to create payment URL'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def payment_ipn(request):
    """
    VNPay IPN (Instant Payment Notification) callback
    This is called by VNPay server to notify payment result
    
    Must return JsonResponse with RspCode and Message
    """
    try:
        input_data = request.GET.dict()
        
        if not input_data:
            return Response({
                'RspCode': '99',
                'Message': 'Invalid request'
            })
        
        vnp = VNPayPayment()
        vnp.response_data = dict(input_data)
        
        # Extract data
        order_id = input_data.get('vnp_TxnRef')
        amount = int(input_data.get('vnp_Amount', 0)) / 100
        vnp_transaction_no = input_data.get('vnp_TransactionNo')
        vnp_response_code = input_data.get('vnp_ResponseCode')
        vnp_bank_code = input_data.get('vnp_BankCode', '')
        vnp_card_type = input_data.get('vnp_CardType', '')
        vnp_pay_date = input_data.get('vnp_PayDate')
        
        # Validate signature
        if not vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            logger.error(f'Invalid VNPay signature for order {order_id}')
            return Response({
                'RspCode': '97',
                'Message': 'Invalid Signature'
            })
        
        # Get order
        try:
            order = Order.objects.prefetch_related('items').get(id=order_id)
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found in IPN')
            return Response({
                'RspCode': '01',
                'Message': 'Order Not Found'
            })
        
        # Calculate total amount from order items
        from django.db.models import Sum
        order_total = order.items.aggregate(total=Sum('amount'))['total'] or 0
        
        # Check amount
        if abs(float(order_total) - amount) > 0.01:
            logger.error(f'Amount mismatch for order {order_id}: {order_total} != {amount}')
            return Response({
                'RspCode': '04',
                'Message': 'Invalid amount'
            })
        
        # Update order based on payment result
        with transaction.atomic():
            # Create or update payment transaction
            payment_transaction, created = PaymentTransaction.objects.get_or_create(
                order=order,
                transaction_no=vnp_transaction_no,
                defaults={
                    'amount': amount,
                    'response_code': vnp_response_code,
                    'bank_code': vnp_bank_code,
                    'card_type': vnp_card_type,
                    'pay_date': datetime.strptime(vnp_pay_date, '%Y%m%d%H%M%S') if vnp_pay_date else None,
                    'status': 'success' if vnp_response_code == '00' else 'failed'
                }
            )
            
            if not created:
                logger.warning(f'Payment transaction already exists for order {order_id}')
                return Response({
                    'RspCode': '02',
                    'Message': 'Order Already Updated'
                })
            
            # Update order status
            if vnp_response_code == VNPayConfig.RESPONSE_CODE_SUCCESS:
                order.payment_status = 'paid'
                order.status = 'processing'  # Or your desired status
                order.save()
                logger.info(f'Order {order_id} payment successful via VNPay')
            else:
                order.payment_status = 'failed'
                order.save()
                logger.warning(f'Order {order_id} payment failed: {vnp_response_code}')
        
        return Response({
            'RspCode': '00',
            'Message': 'Confirm Success'
        })
        
    except Exception as e:
        logger.error(f'Error in VNPay IPN: {str(e)}')
        return Response({
            'RspCode': '99',
            'Message': 'Unknown error'
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def payment_return(request):
    """
    VNPay return URL
    This is where user is redirected after payment
    
    Frontend should handle this URL and display payment result
    """
    try:
        input_data = request.GET.dict()
        
        if not input_data:
            return Response({
                'success': False,
                'message': 'Invalid request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        vnp = VNPayPayment()
        vnp.response_data = dict(input_data)
        
        # Extract data
        order_id = input_data.get('vnp_TxnRef')
        amount = int(input_data.get('vnp_Amount', 0)) / 100
        order_desc = input_data.get('vnp_OrderInfo')
        vnp_transaction_no = input_data.get('vnp_TransactionNo')
        vnp_response_code = input_data.get('vnp_ResponseCode')
        vnp_bank_code = input_data.get('vnp_BankCode', '')
        vnp_card_type = input_data.get('vnp_CardType', '')
        
        # Log for debugging
        logger.info(f'[VNPAY RETURN] Order: {order_id}, ResponseCode: {vnp_response_code}')
        logger.info(f'[VNPAY RETURN] Full params: {dict(input_data)}')

        # Manual hash reconstruction to compare with VNPay signature
        debug_payload = dict(input_data)
        vnp_secure_hash = debug_payload.pop('vnp_SecureHash', None)
        debug_payload.pop('vnp_SecureHashType', None)

        hash_pairs = []
        for key, value in sorted(debug_payload.items()):
            encoded_val = urllib.parse.quote_plus(str(value))
            hash_pairs.append(f"{key}={encoded_val}")
        raw_hash_data = "&".join(hash_pairs)

        computed_debug_hash = None
        secret_key = getattr(settings, 'VNPAY_HASH_SECRET_KEY', '') or ''
        if secret_key:
            computed_debug_hash = hmac.new(
                bytes(secret_key, 'utf-8'),
                bytes(raw_hash_data, 'utf-8'),
                hashlib.sha512
            ).hexdigest()

        print("---------------- DEBUG VNPAY RETURN ----------------")
        print(f"Order ID: {order_id}")
        print(f"1. Chuỗi thô server tạo ra: {raw_hash_data}")
        print(f"2. Chữ ký server tính được: {computed_debug_hash}")
        print(f"3. Chữ ký VNPAY gửi sang:   {vnp_secure_hash}")
        print("----------------------------------------------------")
        if computed_debug_hash and vnp_secure_hash:
            print("=> TRÙNG KHỚP!" if computed_debug_hash == vnp_secure_hash else "=> KHÔNG KHỚP!")
        else:
            print("=> KHÔNG THỂ SO SÁNH (thiếu secret hoặc chữ ký)")
        
        # Validate signature
        is_valid = vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)
        
        logger.info(f'[VNPAY RETURN] Signature valid: {is_valid}')
        
        if not is_valid:
            logger.error(f'[VNPAY RETURN] Invalid signature for order {order_id}')
            return Response({
                'success': False,
                'message': 'Invalid signature',
                'order_id': order_id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare response
        response_data = {
            'success': vnp_response_code == VNPayConfig.RESPONSE_CODE_SUCCESS,
            'order_id': order_id,
            'amount': amount,
            'transaction_no': vnp_transaction_no,
            'response_code': vnp_response_code,
            'message': VNPayConfig.get_response_message(vnp_response_code),
            'bank_code': vnp_bank_code,
            'card_type': vnp_card_type
        }
        
        return Response(response_data)
        
    except Exception as e:
        logger.error(f'Error in VNPay return: {str(e)}')
        return Response({
            'success': False,
            'message': 'Unknown error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
