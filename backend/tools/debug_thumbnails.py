import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.base")

def main():
    from ecommerce.models import Product
    from binary_database_files.models import File

    print("=== Debug product thumbnails vs DB files ===")

    products = Product.objects.all()[:20]
    if not products:
        print("No products found.")
        return

    for p in products:
        tn = getattr(p, "thumbnail", None)
        tn_name = tn.name if tn else None
        print("\nProduct:", p.id)
        print("  thumbnail name:", tn_name)
        if tn_name:
            qs = File.objects.filter(name=tn_name)
            if qs.exists():
                f = qs.first()
                print("  -> FOUND matching File record:")
                print("     id:", f.id)
                print("     name:", f.name)
                print("     size:", f.size)
            else:
                print("  -> NO File record with this name in DB")

if __name__ == "__main__":
    django.setup()
    main()