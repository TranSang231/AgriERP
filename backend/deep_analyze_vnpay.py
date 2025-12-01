"""
Deep analysis of VNPay Code 99 error - checking all possible issues
"""
import urllib.parse

# Latest request (12:49:09)
query_string = "vnp_Amount=22000000&vnp_Command=pay&vnp_CreateDate=20251201124909&vnp_CurrCode=VND&vnp_IpAddr=127.0.0.1&vnp_IpnUrl=https%3A%2F%2Ffirm-remainder-wallpaper-swing.trycloudflare.com%2Fapi%2Fv1%2Fecommerce%2Fpayment%2Fvnpay%2Fipn&vnp_Locale=vn&vnp_OrderInfo=Thanh+toan+don+hang+d62a004f-943e-4987-9f4d-957de0700c4e&vnp_OrderType=other&vnp_ReturnUrl=https%3A%2F%2Fguide-courage-headquarters-photography.trycloudflare.com%2Fpayment%2Fvnpay%2Freturn&vnp_TmnCode=7O7IZ0FE&vnp_TxnRef=d62a004f-943e-4987-9f4d-957de0700c4e&vnp_Version=2.1.0"

print("="*100)
print("VNPAY CODE 99 ERROR - COMPLETE ANALYSIS")
print("="*100)

# Decode to see actual values
decoded = urllib.parse.unquote(query_string)
print(f"\nDecoded query string:\n{decoded}\n")

# Parse parameters
params = {}
for param in query_string.split('&'):
    key, value = param.split('=', 1)
    params[key] = urllib.parse.unquote(value)

print("\n" + "="*100)
print("PARAMETER VALIDATION:")
print("="*100)

# Check each parameter
issues = []

# 1. vnp_Amount
amount = params.get('vnp_Amount', '')
print(f"\n1. vnp_Amount: {amount}")
if not amount.isdigit():
    issues.append("❌ Amount is not numeric")
elif int(amount) <= 0:
    issues.append("❌ Amount is zero or negative")
elif int(amount) < 10000:
    issues.append("⚠️  Amount too small (< 100 VND)")
else:
    print(f"   ✅ Valid: {int(amount)/100:,.0f} VND")

# 2. vnp_IpAddr
ip = params.get('vnp_IpAddr', '')
print(f"\n2. vnp_IpAddr: {ip}")
if not ip:
    issues.append("❌ IP Address is empty")
elif ':' in ip and '.' not in ip:
    issues.append("❌ IPv6 detected (VNPay needs IPv4)")
else:
    print("   ✅ Valid IPv4")

# 3. vnp_OrderInfo
order_info = params.get('vnp_OrderInfo', '')
print(f"\n3. vnp_OrderInfo: {order_info}")
print(f"   Length: {len(order_info)}")
if len(order_info) > 255:
    issues.append("❌ OrderInfo too long (>255 chars)")
if any(c in order_info for c in ['#', '&', '%', '=']):
    issues.append("❌ OrderInfo contains special chars")
print("   ✅ OK")

# 4. vnp_ReturnUrl
return_url = params.get('vnp_ReturnUrl', '')
print(f"\n4. vnp_ReturnUrl: {return_url}")
print(f"   Length: {len(return_url)}")
if len(return_url) > 255:
    issues.append("❌ ReturnUrl too long (>255 chars)")
if not return_url.startswith('http'):
    issues.append("❌ ReturnUrl doesn't start with http")
else:
    print("   ✅ OK")

# 5. vnp_IpnUrl
ipn_url = params.get('vnp_IpnUrl', '')
print(f"\n5. vnp_IpnUrl: {ipn_url}")
print(f"   Length: {len(ipn_url)}")
if len(ipn_url) > 255:
    issues.append("❌ IpnUrl too long (>255 chars)")
else:
    print("   ✅ OK")

# 6. vnp_TxnRef
txn_ref = params.get('vnp_TxnRef', '')
print(f"\n6. vnp_TxnRef: {txn_ref}")
print(f"   Length: {len(txn_ref)}")
if len(txn_ref) > 100:
    issues.append("⚠️  TxnRef might be too long (UUID: {len(txn_ref)} chars)")
print(f"   ⚠️  Using full UUID ({len(txn_ref)} chars) - VNPay expects max 100")

# 7. Check required fields
required_fields = [
    'vnp_Version', 'vnp_Command', 'vnp_TmnCode', 'vnp_Amount', 
    'vnp_CurrCode', 'vnp_TxnRef', 'vnp_OrderInfo', 'vnp_OrderType',
    'vnp_ReturnUrl', 'vnp_CreateDate', 'vnp_IpAddr'
]

print(f"\n7. Required Fields Check:")
for field in required_fields:
    if field in params:
        print(f"   ✅ {field}")
    else:
        print(f"   ❌ {field} MISSING!")
        issues.append(f"❌ Missing required field: {field}")

# Check for vnp_Locale (should be exactly 'vn' or 'en')
locale = params.get('vnp_Locale', '')
print(f"\n8. vnp_Locale: '{locale}'")
if locale not in ['vn', 'en']:
    issues.append(f"⚠️  Locale '{locale}' might not be valid (should be 'vn' or 'en')")

print("\n" + "="*100)
print("SUMMARY:")
print("="*100)

if issues:
    print("\n⚠️  FOUND ISSUES:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n✅ All parameters look correct!")
    print("\n🔍 If still getting Code 99, possible causes:")
    print("   1. TMN_CODE not activated on VNPay")
    print("   2. Need to configure IPN URL on VNPay portal first")
    print("   3. VNPay Sandbox server issue")
    print("   4. Secret Key mismatch (double-check on portal)")

print("="*100)
