"""
Analyze VNPay request from log to debug Code 99 error
"""

# From latest log (12:43:37)
query_string = "vnp_Amount=22000000&vnp_Command=pay&vnp_CreateDate=20251201124337&vnp_CurrCode=VND&vnp_IpAddr=2402%3A800%3A629c%3A9f53%3Ac16%3A6cbd%3A754e%3Adab1&vnp_IpnUrl=https%3A%2F%2Ffirm-remainder-wallpaper-swing.trycloudflare.com%2Fapi%2Fv1%2Fecommerce%2Fpayment%2Fvnpay%2Fipn&vnp_Locale=vn&vnp_OrderInfo=Thanh+toan+don+hang+7f5a9a43-46c3-4af7-8ec4-c79ca771574f&vnp_OrderType=other&vnp_ReturnUrl=https%3A%2F%2Fguide-courage-headquarters-photography.trycloudflare.com%2Fpayment%2Fvnpay%2Freturn&vnp_TmnCode=7O7IZ0FE&vnp_TxnRef=7f5a9a43-46c3-4af7-8ec4-c79ca771574f&vnp_Version=2.1.0"

import urllib.parse

print("="*80)
print("VNPAY REQUEST ANALYSIS - Code 99 Debug")
print("="*80)

# Parse query string
params = urllib.parse.parse_qs(query_string)

print("\n1. vnp_Amount:")
amount = params.get('vnp_Amount', [''])[0]
print(f"   Value: {amount}")
print(f"   Type: {type(amount)}")
print(f"   Is numeric: {amount.isdigit()}")
print(f"   ✅ OK" if amount.isdigit() and int(amount) > 0 else "   ❌ ERROR")

print("\n2. vnp_IpAddr:")
ip = params.get('vnp_IpAddr', [''])[0]
print(f"   Value: {ip}")
print(f"   Length: {len(ip)}")
print(f"   ⚠️  IPv6 detected! VNPay may reject IPv6 addresses!" if ':' in ip else "   ✅ IPv4 OK")

print("\n3. vnp_OrderInfo:")
order_info = params.get('vnp_OrderInfo', [''])[0]
print(f"   Value: {order_info}")
print(f"   Has special chars: {any(c in order_info for c in ['#', '&', '%'])}")
print(f"   ✅ OK" if not any(c in order_info for c in ['#', '&', '%']) else "   ❌ Has special chars")

print("\n4. vnp_ReturnUrl:")
return_url = params.get('vnp_ReturnUrl', [''])[0]
print(f"   Value: {return_url}")
print(f"   Length: {len(return_url)}")
print(f"   ✅ OK" if len(return_url) < 255 else "   ❌ Too long (>255 chars)")

print("\n5. vnp_IpnUrl:")
ipn_url = params.get('vnp_IpnUrl', [''])[0]
print(f"   Value: {ipn_url}")
print(f"   Length: {len(ipn_url)}")

print("\n" + "="*80)
print("SUSPECTED ISSUE:")
print("="*80)
print("🔴 vnp_IpAddr is using IPv6 (2402:800:629c:9f53:c16:6cbd:754e:dab1)")
print("   VNPay Sandbox may ONLY accept IPv4 addresses!")
print("\n   SOLUTION: Force IPv4 address to 127.0.0.1 or get real public IPv4")
print("="*80)
