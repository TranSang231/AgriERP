from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    ProvinceViewSet,
    DistrictViewSet,
    WardViewSet,
    CustomerViewSet,
    ShippingAddressViewSet,
    ProductCategoryViewSet,
    ProductViewSet,
    PromotionViewSet,
    CartViewSet,
    OrderViewSet,
    GoodsReceiptViewSet,
    InventoryViewSet,
    general_statistics,
    sales_data,
    order_status_data,
    recent_orders,
    top_products,
    inventory_alerts
)


app_name = "ecommerce"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"provinces", ProvinceViewSet, basename="ecommerce-provinces")
router.register(r"districts", DistrictViewSet, basename="ecommerce-districts")
router.register(r"wards", WardViewSet, basename="ecommerce-wards")
router.register(r"product-categories", ProductCategoryViewSet, basename="ecommerce-product-categories")
router.register(r"products", ProductViewSet, basename="ecommerce-products")
router.register(r"promotions", PromotionViewSet, basename="ecommerce-promotions")
router.register(r"carts", CartViewSet, basename="ecommerce-carts")
router.register(r"orders", OrderViewSet, basename="ecommerce-orders")
router.register(r"goods-receipts", GoodsReceiptViewSet, basename="ecommerce-goods-receipts")
router.register(r"inventory", InventoryViewSet, basename="ecommerce-inventory")

router.register(r"customers", CustomerViewSet, basename="ecommerce-customers")
customer_router = routers.NestedSimpleRouter(router, r'customers', lookup='customers')
customer_router.register(r'shipping-addresses', ShippingAddressViewSet, basename="ecommerce-shipping-addresses")

urlpatterns = [
    path(r'api/v1/ecommerce/', include(router.urls)),
    path(r'api/v1/ecommerce/', include(customer_router.urls)),
    # Statistics endpoints
    path(r'api/v1/ecommerce/statistics/general', general_statistics, name='ecommerce-general-statistics'),
    path(r'api/v1/ecommerce/statistics/sales', sales_data, name='ecommerce-sales-data'),
    path(r'api/v1/ecommerce/statistics/order-status', order_status_data, name='ecommerce-order-status'),
    path(r'api/v1/ecommerce/statistics/recent-orders', recent_orders, name='ecommerce-recent-orders'),
    path(r'api/v1/ecommerce/statistics/top-products', top_products, name='ecommerce-top-products'),
    path(r'api/v1/ecommerce/statistics/inventory-alerts', inventory_alerts, name='ecommerce-inventory-alerts'),
]
