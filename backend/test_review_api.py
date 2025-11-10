"""
Test script for Product Review API
Run: python test_review_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8008/api/v1/ecommerce"

def print_response(title, response):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*60}\n")

def test_review_api():
    """Test all review API endpoints"""
    
    # 1. Get all reviews for a product
    print("\n🚀 Testing Product Review API\n")
    
    product_id = 1
    response = requests.get(f"{BASE_URL}/reviews", params={'product_id': product_id})
    print_response(f"1. List reviews for product {product_id}", response)
    
    # 2. Get product review statistics
    response = requests.get(f"{BASE_URL}/reviews/product_statistics", params={'product_id': product_id})
    print_response(f"2. Review statistics for product {product_id}", response)
    
    # 3. Filter by rating
    response = requests.get(f"{BASE_URL}/reviews", params={'product_id': product_id, 'rating': 5})
    print_response(f"3. Filter 5-star reviews for product {product_id}", response)
    
    # 4. Sort by most helpful
    response = requests.get(f"{BASE_URL}/reviews", params={'product_id': product_id, 'sort': 'most_helpful'})
    print_response(f"4. Reviews sorted by most helpful", response)
    
    # 5. Only verified purchases
    response = requests.get(f"{BASE_URL}/reviews", params={'product_id': product_id, 'verified_only': 'true'})
    print_response(f"5. Only verified purchase reviews", response)
    
    # 6. Get a single review detail
    reviews_response = requests.get(f"{BASE_URL}/reviews", params={'product_id': product_id})
    if reviews_response.status_code == 200:
        reviews_data = reviews_response.json()
        if isinstance(reviews_data, list) and len(reviews_data) > 0:
            review_id = reviews_data[0]['id']
            response = requests.get(f"{BASE_URL}/reviews/{review_id}")
            print_response(f"6. Review detail (ID: {review_id})", response)
    
    # 7. Test authentication required endpoints (will fail without token)
    print("\n⚠️  The following require authentication (will return 401/403):\n")
    
    # Try to create review without auth
    response = requests.post(f"{BASE_URL}/reviews", json={
        'product': 1,
        'order': 1,
        'rating': 5,
        'title': 'Test review',
        'comment': 'This is a test'
    })
    print_response("7. Create review (without auth - should fail)", response)
    
    # Try to get my reviews without auth
    response = requests.get(f"{BASE_URL}/reviews/my_reviews")
    print_response("8. Get my reviews (without auth - should fail)", response)
    
    print("\n✅ Test completed!")
    print("\n📝 To test authenticated endpoints:")
    print("   1. Login with customer1@example.com / password123")
    print("   2. Get access token")
    print("   3. Use: headers={'Authorization': 'Bearer <token>'}")
    print("\n🔗 Review API endpoints:")
    print(f"   GET  {BASE_URL}/reviews?product_id=X")
    print(f"   GET  {BASE_URL}/reviews/{{id}}")
    print(f"   POST {BASE_URL}/reviews")
    print(f"   PUT  {BASE_URL}/reviews/{{id}}")
    print(f"   POST {BASE_URL}/reviews/{{id}}/mark_helpful")
    print(f"   POST {BASE_URL}/reviews/{{id}}/unmark_helpful")
    print(f"   GET  {BASE_URL}/reviews/product_statistics?product_id=X")
    print(f"   GET  {BASE_URL}/reviews/my_reviews")
    print(f"   GET  {BASE_URL}/reviews/can_review?product_id=X&order_id=Y")

if __name__ == '__main__':
    try:
        test_review_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server")
        print("Please make sure Django server is running:")
        print("  python manage.py runserver 8008")
    except Exception as e:
        print(f"❌ Error: {e}")
