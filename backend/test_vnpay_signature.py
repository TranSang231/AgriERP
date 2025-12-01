"""
Test VNPay signature generation
This script helps debug VNPay signature issues
"""
import hashlib
import hmac
import urllib.parse
from datetime import datetime

# VNPay credentials from config.env
TMN_CODE = "7O7IZ0FE"
HASH_SECRET_KEY = "8A4VK1M5IH8EHWJEI12DXI492FA2VJI7"
RETURN_URL = "https://guide-courage-headquarters-photography.trycloudflare.com/payment/vnpay/return"
PAYMENT_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"

def create_test_payment():
    """Create a test payment request"""
    
    # Sample payment data
    request_data = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': TMN_CODE,
        'vnp_Amount': '10000000',  # 100,000 VND (x100)
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': 'TEST123',
        'vnp_OrderInfo': 'Test payment',
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': RETURN_URL,
        'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
        'vnp_IpAddr': '127.0.0.1'
    }
    
    # Sort by key
    sorted_data = sorted(request_data.items())
    
    # Build query string
    query_parts = []
    for key, val in sorted_data:
        encoded_val = urllib.parse.quote_plus(str(val))
        query_parts.append(f"{key}={encoded_val}")
    
    query_string = "&".join(query_parts)
    
    # Generate HMAC SHA512 signature
    byte_key = HASH_SECRET_KEY.encode('utf-8')
    byte_data = query_string.encode('utf-8')
    hash_value = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
    
    # Build final URL
    payment_url = f"{PAYMENT_URL}?{query_string}&vnp_SecureHash={hash_value}"
    
    print("=" * 80)
    print("VNPAY SIGNATURE TEST")
    print("=" * 80)
    print(f"\nTMN Code: {TMN_CODE}")
    print(f"Hash Secret Key: {HASH_SECRET_KEY}")
    print(f"Return URL: {RETURN_URL}")
    print(f"\nRequest Data:")
    for key, val in sorted_data:
        print(f"  {key}: {val}")
    
    print(f"\nQuery String (before hash):")
    print(query_string)
    
    print(f"\nGenerated Hash (SHA512):")
    print(hash_value)
    
    print(f"\nFull Payment URL:")
    print(payment_url)
    print("=" * 80)
    
    return payment_url

if __name__ == "__main__":
    create_test_payment()
