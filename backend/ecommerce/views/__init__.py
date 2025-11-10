from .province import ProvinceViewSet
from .district import DistrictViewSet
from .ward import WardViewSet
from .customer import CustomerViewSet
from .shipping_address import ShippingAddressViewSet
from .product_category import ProductCategoryViewSet
from .product import ProductViewSet
from .promotion import PromotionViewSet
from .cart import CartViewSet
from .order import OrderViewSet
from .goods_receipt import GoodsReceiptViewSet
from .inventory import InventoryViewSet
from .statistic import (
    general_statistics,
    sales_data,
    order_status_data,
    recent_orders,
    top_products,
    inventory_alerts
)