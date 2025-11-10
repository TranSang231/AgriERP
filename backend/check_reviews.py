import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ecommerce.models import ProductReview, Product

# Get first product
product = Product.objects.first()
print(f"Product ID: {product.id}")
print(f"Product Name: {product.name}")

# Count reviews
all_reviews = ProductReview.objects.filter(product=product)
approved_reviews = all_reviews.filter(is_approved=True)

print(f"\nTotal reviews: {all_reviews.count()}")
print(f"Approved reviews: {approved_reviews.count()}")

# Show first 5
print("\nFirst 5 reviews:")
for r in approved_reviews[:5]:
    print(f"  - Customer: {r.customer.email}")
    print(f"    Rating: {r.rating}★")
    print(f"    Title: {r.title}")
    print(f"    Comment: {r.comment[:50]}...")
    print()

# Check statistics
print(f"Average rating: {product.average_rating}")
print(f"Review count: {product.review_count}")
print(f"Distribution: {product.rating_distribution}")
