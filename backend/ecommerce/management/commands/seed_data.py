"""
Command to seed comprehensive test data for AgriERP Ecommerce
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from datetime import datetime, timedelta
import random

from core.settings.base import SECRET_KEY
from oauth.models import User, Role
from oauth.constants import AccountStatus
from common.constants import Gender
from businesses.models import Employee
from ecommerce.models import (
    ProductCategory, Product, ProductImage,
    Customer, Province, District, Ward,
    DeliveryServiceProvider, ShippingAddress,
    Cart, CartItem, Order, OrderItem,
    Inventory, InventoryTransaction,
    InventoryConfiguration, GoodsReceipt, GoodsReceiptItem,
    Promotion, PromotionItem, ProductReview, ReviewHelpful
)
from contents.models import ShortContent, LongContent, ShortTranslate, LongTranslate
from common.constants import Language


class Command(BaseCommand):
    help = 'Seed comprehensive test data for ecommerce'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--reviews-only',
            action='store_true',
            help='Only seed reviews for existing orders',
        )

    def handle(self, *args, **options):
        if options['reviews_only']:
            self.stdout.write(self.style.SUCCESS('Seeding reviews only...'))
            self.seed_reviews_only()
            return
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        with transaction.atomic():
            # 1. Create contents for multilingual support
            contents = self.create_contents()
            self.stdout.write(self.style.SUCCESS('✓ Created contents'))
            
            # 2. Create product categories
            categories = self.create_categories(contents)
            self.stdout.write(self.style.SUCCESS('✓ Created categories'))
            
            # 3. Create products
            products = self.create_products(categories, contents)
            self.stdout.write(self.style.SUCCESS('✓ Created products'))
            
            # 4. Create inventory
            self.create_inventory(products)
            self.stdout.write(self.style.SUCCESS('✓ Created inventory'))
            
            # 5. Create customers
            customers = self.create_customers()
            self.stdout.write(self.style.SUCCESS('✓ Created customers'))
            
            # 6. Create addresses
            provinces, districts, wards = self.create_addresses()
            self.stdout.write(self.style.SUCCESS('✓ Created addresses'))
            
            # 7. Create delivery service providers
            delivery_providers = self.create_delivery_providers()
            self.stdout.write(self.style.SUCCESS('✓ Created delivery providers'))
            
            # 8. Create shipping addresses
            self.create_shipping_addresses(customers, provinces, districts, wards)
            self.stdout.write(self.style.SUCCESS('✓ Created shipping addresses'))
            
            # 9. Create promotions
            promotions = self.create_promotions(products)
            self.stdout.write(self.style.SUCCESS('✓ Created promotions'))
            
            # 10. Create carts
            self.create_carts(customers, products)
            self.stdout.write(self.style.SUCCESS('✓ Created carts'))
            
            # 11. Create orders
            self.create_orders(customers, products, delivery_providers)
            self.stdout.write(self.style.SUCCESS('✓ Created orders'))
            
            # 12. Create goods receipts
            self.create_goods_receipts(products)
            self.stdout.write(self.style.SUCCESS('✓ Created goods receipts'))
            
            # 13. Create product reviews
            self.create_reviews(customers, products)
            self.stdout.write(self.style.SUCCESS('✓ Created product reviews'))

        self.stdout.write(self.style.SUCCESS('✅ Data seeding completed successfully!'))
        self.print_summary()

    def seed_reviews_only(self):
        """Seed reviews only for existing data"""
        with transaction.atomic():
            # Xóa reviews hiện có
            ReviewHelpful.objects.all().delete()
            ProductReview.objects.all().delete()
            
            # Lấy customers và products hiện có
            customers = list(Customer.objects.all())
            products = list(Product.objects.all())
            
            if not customers:
                self.stdout.write(self.style.ERROR('No customers found. Please run full seed first.'))
                return
            
            if not products:
                self.stdout.write(self.style.ERROR('No products found. Please run full seed first.'))
                return
            
            # Tạo reviews
            self.create_reviews(customers, products)
            self.stdout.write(self.style.SUCCESS('✓ Created product reviews'))
        
        self.stdout.write(self.style.SUCCESS('✅ Reviews seeding completed!'))
        self.stdout.write(f'Total reviews: {ProductReview.objects.count()}')

    def clear_data(self):
        """Clear existing ecommerce data"""
        # Delete in correct order to avoid foreign key constraints
        self.stdout.write('  Deleting orders...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        
        self.stdout.write('  Deleting carts...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        
        self.stdout.write('  Deleting promotions...')
        PromotionItem.objects.all().delete()
        Promotion.objects.all().delete()
        
        self.stdout.write('  Deleting shipping addresses...')
        ShippingAddress.objects.all().delete()
        
        self.stdout.write('  Deleting goods receipts...')
        GoodsReceiptItem.objects.all().delete()
        GoodsReceipt.objects.all().delete()
        
        self.stdout.write('  Deleting inventory...')
        InventoryTransaction.objects.all().delete()
        Inventory.objects.all().delete()
        
        self.stdout.write('  Deleting products...')
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        
        self.stdout.write('  Deleting categories...')
        ProductCategory.objects.all().delete()
        
        self.stdout.write('  Deleting customers...')
        Customer.objects.filter(email__contains='customer').delete()
        
        self.stdout.write('  Deleting addresses...')
        Ward.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()
        
        self.stdout.write('  Deleting delivery providers...')
        DeliveryServiceProvider.objects.all().delete()
        
        self.stdout.write('  Deleting reviews...')
        ReviewHelpful.objects.all().delete()
        ProductReview.objects.all().delete()
        
        self.stdout.write('  Deleting contents...')
        # Also delete content objects
        from contents.models import ShortTranslate, LongTranslate
        ShortTranslate.objects.all().delete()
        LongTranslate.objects.all().delete()
        ShortContent.objects.all().delete()
        LongContent.objects.all().delete()

    def create_contents(self):
        """Create multilingual content"""
        contents = {}
        
        # Helper function to create content with translations
        def create_content(origin, vi, en, is_long=False):
            if is_long:
                content = LongContent.objects.create(origin=origin)
                LongTranslate.objects.create(content=content, language=Language.VI, value=vi)
                LongTranslate.objects.create(content=content, language=Language.EN, value=en)
            else:
                content = ShortContent.objects.create(origin=origin)
                ShortTranslate.objects.create(content=content, language=Language.VI, value=vi)
                ShortTranslate.objects.create(content=content, language=Language.EN, value=en)
            return content
        
        # Product names
        contents['tomato'] = create_content('Tomato', 'Cà chua', 'Tomato')
        contents['lettuce'] = create_content('Lettuce', 'Xà lách', 'Lettuce')
        contents['carrot'] = create_content('Carrot', 'Cà rốt', 'Carrot')
        contents['potato'] = create_content('Potato', 'Khoai tây', 'Potato')
        contents['onion'] = create_content('Onion', 'Hành tây', 'Onion')
        contents['cabbage'] = create_content('Cabbage', 'Bắp cải', 'Cabbage')
        contents['cucumber'] = create_content('Cucumber', 'Dưa chuột', 'Cucumber')
        contents['pepper'] = create_content('Pepper', 'Ớt', 'Pepper')
        contents['eggplant'] = create_content('Eggplant', 'Cà tím', 'Eggplant')
        contents['broccoli'] = create_content('Broccoli', 'Bông cải xanh', 'Broccoli')
        
        # Categories
        contents['vegetables'] = create_content('Vegetables', 'Rau củ', 'Vegetables')
        contents['fruits'] = create_content('Fruits', 'Trái cây', 'Fruits')
        contents['herbs'] = create_content('Herbs', 'Rau thơm', 'Herbs')
        contents['organic'] = create_content('Organic', 'Hữu cơ', 'Organic')
        
        # Units
        contents['kg'] = create_content('kg', 'kg', 'kg')
        contents['piece'] = create_content('piece', 'cái', 'piece')
        contents['bunch'] = create_content('bunch', 'bó', 'bunch')
        
        # Descriptions (long content)
        contents['tomato_desc'] = create_content(
            'Fresh tomatoes',
            'Cà chua tươi, giàu vitamin C và chất chống oxy hóa',
            'Fresh tomatoes, rich in vitamin C and antioxidants',
            is_long=True
        )
        contents['lettuce_desc'] = create_content(
            'Fresh lettuce',
            'Xà lách xanh tươi, giòn ngon, giàu chất xơ',
            'Fresh green lettuce, crispy and rich in fiber',
            is_long=True
        )
        contents['carrot_desc'] = create_content(
            'Fresh carrots',
            'Cà rốt tươi, giàu vitamin A, tốt cho mắt',
            'Fresh carrots, rich in vitamin A, good for eyes',
            is_long=True
        )
        
        return contents

    def create_categories(self, contents):
        """Create product categories"""
        categories = []
        
        category_data = [
            {'name': contents['vegetables'], 'desc': 'Rau củ tươi ngon'},
            {'name': contents['fruits'], 'desc': 'Trái cây tươi'},
            {'name': contents['herbs'], 'desc': 'Rau thơm các loại'},
            {'name': contents['organic'], 'desc': 'Sản phẩm hữu cơ'},
        ]
        
        for data in category_data:
            category = ProductCategory.objects.create(
                name=data['name'],
                description=data['desc']
            )
            categories.append(category)
        
        return categories

    def create_products(self, categories, contents):
        """Create products"""
        products = []
        
        product_data = [
            # Vegetables
            {'name': contents['tomato'], 'desc': contents['tomato_desc'], 'price': 25000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['lettuce'], 'desc': contents['lettuce_desc'], 'price': 15000, 'unit': contents['bunch'], 'weight': 0.3},
            {'name': contents['carrot'], 'desc': contents['carrot_desc'], 'price': 18000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['potato'], 'desc': None, 'price': 20000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['onion'], 'desc': None, 'price': 22000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['cabbage'], 'desc': None, 'price': 12000, 'unit': contents['piece'], 'weight': 1.5},
            {'name': contents['cucumber'], 'desc': None, 'price': 15000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['pepper'], 'desc': None, 'price': 45000, 'unit': contents['kg'], 'weight': 0.5},
            {'name': contents['eggplant'], 'desc': None, 'price': 18000, 'unit': contents['kg'], 'weight': 1.0},
            {'name': contents['broccoli'], 'desc': None, 'price': 35000, 'unit': contents['kg'], 'weight': 0.8},
        ]
        
        for i, data in enumerate(product_data):
            product = Product.objects.create(
                name=data['name'],
                description=data['desc'],
                price=data['price'],
                unit=data['unit'],
                weight=data['weight'],
                length=15.0,
                width=10.0,
                height=8.0,
                tax_rate=0.1
            )
            
            # Add to categories
            product.categories.add(categories[0])  # All in vegetables
            if i % 2 == 0:
                product.categories.add(categories[3])  # Some organic
            
            products.append(product)
        
        return products

    def create_inventory(self, products):
        """Update inventory for products (inventory auto-created by signal)"""
        for product in products:
            quantity = random.randint(50, 500)
            min_quantity = random.randint(10, 30)
            
            # Get the auto-created inventory (created by signal)
            inventory = product.inventory
            
            # Update quantities
            inventory.current_quantity = quantity
            inventory.min_quantity = min_quantity
            inventory.reserved_quantity = 0
            inventory.save()
            
            # Create initial inventory transaction
            InventoryTransaction.objects.create(
                inventory=inventory,
                transaction_type='in',
                quantity=quantity,
                reason='Initial stock',
                reference_number=f'INIT-{product.id}'
            )

    def create_customers(self):
        """Create customer accounts"""
        customers = []
        
        customer_data = [
            {'first_name': 'Nguyễn', 'last_name': 'Văn A', 'email': 'customer1@example.com', 'phone': '0901234567', 'gender': Gender.MALE},
            {'first_name': 'Trần', 'last_name': 'Thị B', 'email': 'customer2@example.com', 'phone': '0902234567', 'gender': Gender.FEMALE},
            {'first_name': 'Lê', 'last_name': 'Văn C', 'email': 'customer3@example.com', 'phone': '0903234567', 'gender': Gender.MALE},
            {'first_name': 'Phạm', 'last_name': 'Thị D', 'email': 'customer4@example.com', 'phone': '0904234567', 'gender': Gender.FEMALE},
            {'first_name': 'Hoàng', 'last_name': 'Văn E', 'email': 'customer5@example.com', 'phone': '0905234567', 'gender': Gender.MALE},
        ]
        
        for i, data in enumerate(customer_data):
            # Check if customer already exists
            customer = Customer.objects.filter(email=data['email']).first()
            
            if customer:
                customers.append(customer)
                continue
            
            # Check if user already exists
            user = User.objects.filter(email=data['email']).first()
            
            if not user:
                # Create user account
                user = User.objects.create(
                    email=data['email'],
                    password=make_password('password123', salt=SECRET_KEY),
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    is_superuser=False,
                    is_staff=False,
                    active=True
                )
            
            # Create customer
            customer = Customer.objects.create(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                gender=data['gender'],
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(7300, 18250)),
                user=user,
                status=AccountStatus.ACTIVE
            )
            customers.append(customer)
        
        return customers

    def create_addresses(self):
        """Create provinces, districts, wards"""
        # Create provinces
        provinces = []
        province_data = [
            {'name': 'Hà Nội'},
            {'name': 'Hồ Chí Minh'},
            {'name': 'Đà Nẵng'},
        ]
        
        for data in province_data:
            province = Province.objects.create(name=data['name'])
            provinces.append(province)
        
        # Create districts
        districts = []
        district_data = [
            {'name': 'Ba Đình', 'province': provinces[0]},
            {'name': 'Hoàn Kiếm', 'province': provinces[0]},
            {'name': 'Quận 1', 'province': provinces[1]},
            {'name': 'Quận 2', 'province': provinces[1]},
        ]
        
        for data in district_data:
            district = District.objects.create(
                name=data['name'],
                province=data['province']
            )
            districts.append(district)
        
        # Create wards
        wards = []
        ward_data = [
            {'name': 'Phúc Xá', 'district': districts[0]},
            {'name': 'Trúc Bạch', 'district': districts[0]},
            {'name': 'Hàng Bài', 'district': districts[1]},
            {'name': 'Bến Nghé', 'district': districts[2]},
        ]
        
        for data in ward_data:
            ward = Ward.objects.create(
                name=data['name'],
                district=data['district']
            )
            wards.append(ward)
        
        return provinces, districts, wards

    def create_delivery_providers(self):
        """Create delivery service providers"""
        providers = []
        
        provider_data = [
            {'name': 'Giao Hàng Nhanh'},
            {'name': 'Giao Hàng Tiết Kiệm'},
            {'name': 'VNPost'},
            {'name': 'J&T Express'},
        ]
        
        for data in provider_data:
            provider = DeliveryServiceProvider.objects.create(
                name=data['name'],
                is_default=(data['name'] == 'Giao Hàng Nhanh')
            )
            providers.append(provider)
        
        return providers

    def create_shipping_addresses(self, customers, provinces, districts, wards):
        """Create shipping addresses for customers"""
        # Create mapping for easier access
        province_districts = {}
        for district in districts:
            if district.province.id not in province_districts:
                province_districts[district.province.id] = []
            province_districts[district.province.id].append(district)
        
        district_wards = {}
        for ward in wards:
            if ward.district.id not in district_wards:
                district_wards[ward.district.id] = []
            district_wards[ward.district.id].append(ward)
        
        for customer in customers:
            num_addresses = random.randint(1, 2)  # 1-2 addresses per customer
            
            for i in range(num_addresses):
                # Pick a province that has districts
                available_provinces = [p for p in provinces if p.id in province_districts]
                if not available_provinces:
                    continue
                    
                province = random.choice(available_provinces)
                
                # Pick a district in that province
                available_districts = province_districts.get(province.id, [])
                if not available_districts:
                    continue
                    
                district = random.choice(available_districts)
                
                # Pick a ward in that district
                available_wards = district_wards.get(district.id, [])
                ward = random.choice(available_wards) if available_wards else None
                
                ShippingAddress.objects.create(
                    customer=customer,
                    address=f'{random.randint(1, 999)} Đường {random.choice(["Lê Lợi", "Trần Hưng Đạo", "Nguyễn Huệ", "Hai Bà Trưng"])}',
                    province=province,
                    district=district,
                    ward=ward,
                    is_default=(i == 0)
                )

    def create_promotions(self, products):
        """Create promotions"""
        promotions = []
        
        # Create some promotions
        promotion1 = Promotion.objects.create(
            name='Giảm giá 10%',
            type=Promotion.TYPE_VOUCHER,
            discount=10.0,
            start=datetime.now(),
            end=datetime.now() + timedelta(days=30)
        )
        promotions.append(promotion1)
        
        # Add some products to promotion
        for product in products[:5]:
            PromotionItem.objects.create(
                promotion=promotion1,
                product=product
            )
        
        return promotions

    def create_carts(self, customers, products):
        """Create shopping carts"""
        for customer in customers[:3]:  # Only 3 customers have active carts
            cart = Cart.objects.create(customer=customer)
            
            # Add random items to cart
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=random.randint(1, 5)
                )

    def create_orders(self, customers, products, delivery_providers):
        """Create orders with different statuses"""
        from ecommerce.constants import OrderStatus, PaymentMethod, PaymenStatus, ShippingStatus
        
        statuses = [
            OrderStatus.NEW,
            OrderStatus.CONFIRMED,
            OrderStatus.PACKING,
            OrderStatus.SHIPPED,
            OrderStatus.COMPLETED,
        ]
        
        for customer in customers:
            # Create 2-4 orders per customer
            num_orders = random.randint(2, 4)
            
            for _ in range(num_orders):
                # Get customer's shipping address
                shipping_address = ShippingAddress.objects.filter(
                    customer=customer,
                    is_default=True
                ).first()
                
                if not shipping_address:
                    continue
                
                # Calculate totals
                num_items = random.randint(1, 4)
                selected_products = random.sample(products, num_items)
                
                order = Order.objects.create(
                    customer=customer,
                    customer_name=f"{customer.first_name} {customer.last_name}",
                    order_status=random.choice(statuses),
                    payment_method=PaymentMethod.CASH_ON_DELIVERY,
                    payment_status=PaymenStatus.INITIATED,
                    shipping_status=ShippingStatus.BOOKED,
                    shipping_fee=30000,
                    vat_rate=0.1,
                    date=datetime.now().date()
                )
                
                # Add order items
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name.origin if product.name else 'Product',
                        unit=product.unit.origin if product.unit else 'kg',
                        quantity=quantity,
                        price=product.price
                    )

    def create_goods_receipts(self, products):
        """Create goods receipts"""
        for i in range(5):
            receipt = GoodsReceipt.objects.create(
                supplier_name=f'Nhà cung cấp {i+1}',
                reference_code=f'GR-2024-{str(i+1).zfill(4)}',
                date=datetime.now().date() - timedelta(days=random.randint(1, 30)),
                note='Nhập hàng định kỳ',
                is_applied=True,
                applied_at=datetime.now()
            )
            
            # Add items to receipt
            num_items = random.randint(2, 5)
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                quantity = random.randint(50, 200)
                unit_cost = product.price * 0.7  # Cost price is 70% of selling price
                
                GoodsReceiptItem.objects.create(
                    receipt=receipt,
                    product=product,
                    unit=product.unit,
                    quantity=quantity,
                    unit_cost=unit_cost
                )
                
                # Update inventory using product helper method
                product.add_stock(
                    quantity=quantity,
                    reason=f'Goods receipt {receipt.reference_code}',
                    reference_number=receipt.reference_code
                )

    def create_reviews(self, customers, products):
        """Create product reviews for completed orders"""
        from ecommerce.constants.order_status import OrderStatus
        
        # Lấy các đơn hàng đã hoàn thành hoặc đang giao
        completed_orders = Order.objects.filter(
            order_status__in=[OrderStatus.COMPLETED, OrderStatus.SHIPPED]
        )
        
        review_templates = [
            {
                'rating': 5,
                'titles': [
                    'Sản phẩm tuyệt vời!',
                    'Rất hài lòng',
                    'Chất lượng tốt',
                    'Đáng đồng tiền bát gạo',
                    'Sẽ mua lại'
                ],
                'comments': [
                    'Sản phẩm rất tươi và chất lượng. Giao hàng nhanh, đóng gói cẩn thận. Sẽ ủng hộ shop lâu dài!',
                    'Mình đã mua nhiều lần và lần nào cũng hài lòng. Chất lượng ổn định, giá cả phải chăng.',
                    'Sản phẩm đúng như mô tả, tươi ngon. Shop phục vụ nhiệt tình. 5 sao xứng đáng!',
                    'Rất tốt! Đóng gói kỹ, giao hàng đúng hẹn. Sản phẩm tươi và sạch sẽ.',
                ]
            },
            {
                'rating': 4,
                'titles': [
                    'Tốt, sẽ mua lại',
                    'Khá ổn',
                    'Đáng thử',
                    'Chất lượng khá',
                ],
                'comments': [
                    'Sản phẩm tốt, chỉ có điều giao hàng hơi lâu một chút. Nhưng nhìn chung vẫn ok.',
                    'Chất lượng ổn, giá hơi cao so với thị trường. Nhưng được cái yên tâm về nguồn gốc.',
                    'Sản phẩm tươi nhưng size hơi nhỏ. Tuy nhiên vẫn đáng để mua.',
                    'Khá tốt, chỉ trừ 1 sao vì đóng gói chưa thật kỹ. Sản phẩm thì ok.',
                ]
            },
            {
                'rating': 3,
                'titles': [
                    'Tạm được',
                    'Bình thường',
                    'Cũng được',
                ],
                'comments': [
                    'Sản phẩm bình thường, không có gì đặc biệt. Giá hơi cao.',
                    'Chất lượng trung bình. Có thể tốt hơn với mức giá này.',
                    'Không tệ nhưng cũng không xuất sắc. Sẽ cân nhắc khi mua lần sau.',
                ]
            },
        ]
        
        created_reviews = []
        
        for order in completed_orders:
            # Mỗi order sẽ có 50% chance được review
            if random.random() < 0.5:
                continue
            
            # Lấy các items trong order
            order_items = order.items.all()
            
            # Review random 1-3 sản phẩm trong order
            items_to_review = random.sample(
                list(order_items),
                min(random.randint(1, 3), len(order_items))
            )
            
            for item in items_to_review:
                # Random chọn rating template
                template = random.choice(review_templates)
                rating = template['rating']
                
                # Kiểm tra xem đã review chưa
                existing_review = ProductReview.objects.filter(
                    customer=order.customer,
                    product=item.product,
                    order=order
                ).first()
                
                if existing_review:
                    continue
                
                review = ProductReview.objects.create(
                    customer=order.customer,
                    product=item.product,
                    order=order,
                    rating=rating,
                    title=random.choice(template['titles']),
                    comment=random.choice(template['comments']),
                    is_verified_purchase=True,  # Auto verified vì có order
                    is_approved=True,  # Auto approve for seed data
                )
                
                created_reviews.append(review)
                
                # Random tạo helpful votes từ customers khác
                other_customers = [c for c in customers if c != order.customer]
                helpful_customers = random.sample(
                    other_customers,
                    min(random.randint(0, 3), len(other_customers))
                )
                
                for helpful_customer in helpful_customers:
                    ReviewHelpful.objects.create(
                        review=review,
                        customer=helpful_customer
                    )
                    review.helpful_count += 1
                
                if review.helpful_count > 0:
                    review.save(update_fields=['helpful_count'])
        
        self.stdout.write(f'    Created {len(created_reviews)} reviews')

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 DATA SUMMARY'))
        self.stdout.write('='*50)
        
        summary = [
            ('Product Categories', ProductCategory.objects.count()),
            ('Products', Product.objects.count()),
            ('Inventory Records', Inventory.objects.count()),
            ('Inventory Transactions', InventoryTransaction.objects.count()),
            ('Customers', Customer.objects.filter(email__contains='customer').count()),
            ('Provinces', Province.objects.count()),
            ('Districts', District.objects.count()),
            ('Wards', Ward.objects.count()),
            ('Delivery Providers', DeliveryServiceProvider.objects.count()),
            ('Shipping Addresses', ShippingAddress.objects.count()),
            ('Promotions', Promotion.objects.count()),
            ('Carts', Cart.objects.count()),
            ('Orders', Order.objects.count()),
            ('Order Items', OrderItem.objects.count()),
            ('Goods Receipts', GoodsReceipt.objects.count()),
            ('Product Reviews', ProductReview.objects.count()),
        ]
        
        for label, count in summary:
            self.stdout.write(f'  {label}: {count}')
        
        self.stdout.write('='*50 + '\n')
        
        # Print login info
        self.stdout.write(self.style.SUCCESS('👤 TEST ACCOUNTS'))
        self.stdout.write('='*50)
        self.stdout.write('  Email: customer1@example.com')
        self.stdout.write('  Email: customer2@example.com')
        self.stdout.write('  Email: customer3@example.com')
        self.stdout.write('  Password: password123')
        self.stdout.write('='*50 + '\n')
