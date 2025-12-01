"""
Verify VNPay hash from debug log
"""
import hashlib
import hmac

# From vnpay_debug.log
query_string = "vnp_Amount=22000000&vnp_Command=pay&vnp_CreateDate=20251201121853&vnp_CurrCode=VND&vnp_IpAddr=2402%3A800%3A629c%3A9f53%3Ac16%3A6cbd%3A754e%3Adab1&vnp_Locale=vn&vnp_OrderInfo=Thanh+toan+don+hang+31b88e89-8c29-4c87-9747-78c0fe0c3302&vnp_OrderType=other&vnp_ReturnUrl=https%3A%2F%2Fguide-courage-headquarters-photography.trycloudflare.com%2Fpayment%2Fvnpay%2Freturn&vnp_TmnCode=7O7IZ0FE&vnp_TxnRef=31b88e89-8c29-4c87-9747-78c0fe0c3302&vnp_Version=2.1.0"

secret_key = "8A4VK1M5IH8EHWJEI12DXI492FA2VJI7"
expected_hash = "e39c5519814b75f11f4588401b033e4baed5500a722b8b08b62689f9ca12d2eaa9685047df4c581d63f913c961d85ffdac98a2afbf8cf63784661fc59888b39a"

# Calculate hash
byte_key = secret_key.encode('utf-8')
byte_data = query_string.encode('utf-8')
calculated_hash = hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()

print("="*80)
print("VNPAY HASH VERIFICATION")
print("="*80)
print(f"\nQuery String:\n{query_string}")
print(f"\nSecret Key:\n{secret_key}")
print(f"\nExpected Hash:\n{expected_hash}")
print(f"\nCalculated Hash:\n{calculated_hash}")
print(f"\nMatch: {calculated_hash == expected_hash}")

# Build full URL
payment_url = f"https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?{query_string}&vnp_SecureHash={calculated_hash}"
print(f"\nFull Payment URL:")
print(payment_url)
print("="*80)

# Test with VNPay sandbox directly
print("\n🔍 RECOMMENDATION:")
print("Copy the URL above and paste it directly into your browser.")
print("If it shows the VNPay payment page (not error page), then:")
print("  ✅ Credentials are CORRECT")
print("  ✅ Hash calculation is CORRECT")
print("  ❌ Problem is somewhere else in the flow")
print("\nIf it still shows error page, then:")
print("  ❌ Credentials might be wrong")
print("  ❌ Or account is not activated")
print("="*80)
