default_scopes = {
    "ecommerce:addresses:view-mine": "View my addresses",
    "ecommerce:customers:view-mine": "View my information",
    "ecommerce:customers:edit-mine": "Edit my information",
    "ecommerce:addresses:edit-mine": "Edit my addresses",
    "ecommerce:orders:view-mine": "View my orders",
    "ecommerce:orders:edit-mine": "Edit my orders"
}

approvable_scopes = {
	"ecommerce:addresses:view": "View all customer's addresses",
    "ecommerce:addresses:edit": "Edit all customer's addresses",
    "knowledge:namespaces:edit": "Edit all namespaces",
    "ecommerce:customers:view": "View all customers",
    "ecommerce:customers:edit": "Edit all customers",
    "ecommerce:products:view": "View all products",
    "ecommerce:products:edit": "Edit all products",
    "ecommerce:promotions:view": "Vuew all promotions",
    "ecommerce:promotions:edit": "Edit all promotions",
    "ecommerce:orders:view": "View all orders",
    "ecommerce:orders:edit": "Edit all orders",
    "ecommerce:goods-receipts:view": "View all goods receipts",
    "ecommerce:goods-receipts:edit": "Edit all goods receipts",
    "ecommerce:bills:view": "View all bills",
    "ecommerce:bills:edit": "edit all bills"
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
