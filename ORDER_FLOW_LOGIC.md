# 📋 ORDER FLOW LOGIC - Kiểm Tra Chi Tiết

## 🎯 Tổng Quan

Khi khách hàng order 1 sản phẩm, hệ thống thực hiện các bước sau:

### **Flow Chính:**
```
1. CREATE ORDER → Reserve Inventory (tăng reserved_quantity)
2. SHIP ORDER → Giảm cả current_quantity và reserved_quantity
3. CANCEL ORDER → Unreserve (giảm reserved_quantity)
```

---

## 📊 Inventory Model

### **Fields Quan Trọng:**

| Field | Mô Tả | Ý Nghĩa |
|-------|-------|---------|
| `current_quantity` | Tổng số lượng hiện có trong kho | Số lượng thực tế trong kho |
| `reserved_quantity` | Số lượng đã được đặt trước (orders chưa ship) | Đã bán nhưng chưa xuất kho |
| `available_quantity` | **current - reserved** | Có thể bán cho khách mới |

### **Property:**
```python
@property
def available_quantity(self):
    """Quantity available for new orders"""
    return max(0, self.current_quantity - self.reserved_quantity)
```

---

## 🔄 Chi Tiết Flow Khi Order

### **STEP 1: Customer Tạo Order (API: POST /api/ecommerce/orders/)**

#### Backend Logic (`order.py` - `create()` method):

```python
# 1. Validate stock availability
if inventory.available_quantity < order_quantity:
    return Response({'error': 'Not enough stock'}, status=400)

# 2. Create order
order = Order.objects.create(
    customer=customer,
    order_status=OrderStatus.CONFIRMED
)

# 3. Create order items
OrderItem.objects.create(
    order=order,
    product=product,
    quantity=quantity,
    price=product.price
)

# 4. Reserve inventory
inventory.reserved_quantity += quantity
inventory.save()

# 5. Create transaction record
InventoryTransaction.objects.create(
    inventory=inventory,
    transaction_type='reserve',
    quantity=quantity,
    reference_number=f"ORDER-{order.id}",
    reason=f"Reserved for order {order.id}"
)
```

#### Inventory State Changes:
```
Before: current=1000, reserved=0, available=1000
Action: Reserve 50
After:  current=1000, reserved=50, available=950

❌ Stock chưa giảm (vẫn còn trong kho)
✅ Đã reserve (không bán cho khách khác)
```

#### Transaction History:
```
Type: 'reserve'
Quantity: +50
Reference: ORDER-{order_id}
Reason: "Reserved for order {order_id}"
```

---

### **STEP 2: Ship Order (API: POST /api/ecommerce/orders/{id}/ship)**

#### Backend Logic (`order.py` - `ship_order()` method):

```python
# Validate order status
if order.order_status not in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]:
    return Response({'error': 'Order must be confirmed to ship'}, status=400)

# For each order item
for item in order.items.all():
    inventory = item.product.inventory
    quantity = item.quantity
    
    # Check reserved quantity
    if inventory.reserved_quantity < quantity:
        return Response({'error': 'Insufficient reserved quantity'}, status=400)
    
    # Move from reserved to shipped (decrease both)
    inventory.reserved_quantity -= quantity
    inventory.current_quantity -= quantity
    inventory.save()
    
    # Create transaction
    InventoryTransaction.objects.create(
        inventory=inventory,
        transaction_type='out',
        quantity=quantity,
        reference_number=f"ORDER-{order.id}",
        reason=f"Shipped for order {order.id}"
    )

# Update order status
order.order_status = OrderStatus.SHIPPED
order.save()
```

#### Inventory State Changes:
```
Before: current=1000, reserved=50, available=950
Action: Ship 50
After:  current=950, reserved=0, available=950

✅ Stock giảm (đã xuất kho)
✅ Reserved giảm (đơn hàng đã xuất)
```

#### Transaction History:
```
Type: 'out'
Quantity: -50 (hoặc 50)
Reference: ORDER-{order_id}
Reason: "Shipped for order {order_id}"
```

---

### **STEP 3: Cancel Order (API: POST /api/ecommerce/orders/{id}/cancel)**

#### Backend Logic (`order.py` - `cancel_order()` method):

```python
# Validate order status
if order.order_status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
    return Response({'error': 'Cannot cancel shipped orders'}, status=400)

# For each order item
for item in order.items.all():
    inventory = item.product.inventory
    quantity = item.quantity
    
    # Unreserve inventory
    inventory.reserved_quantity = max(0, inventory.reserved_quantity - quantity)
    inventory.save()
    
    # Create transaction
    InventoryTransaction.objects.create(
        inventory=inventory,
        transaction_type='unreserve',
        quantity=quantity,
        reference_number=f"ORDER-{order.id}",
        reason=f"Cancelled order {order.id}"
    )

# Update order status
order.order_status = OrderStatus.CANCELLED
order.save()
```

#### Inventory State Changes:
```
Giả sử có order 100 chưa ship:
Before: current=950, reserved=100, available=850
Action: Cancel order 100
After:  current=950, reserved=0, available=950

❌ Stock không tăng (vì chưa xuất kho)
✅ Reserved giảm (đơn hàng hủy)
✅ Available tăng (có thể bán lại)
```

#### Transaction History:
```
Type: 'unreserve'
Quantity: 100
Reference: ORDER-{order_id}
Reason: "Cancelled order {order_id}"
```

---

## 🧪 Test Case Examples

### **Scenario 1: Normal Order Flow**

```
Initial:  current=1000, reserved=0, available=1000

CREATE Order 50:
→ current=1000, reserved=50, available=950
→ Transaction: reserve +50

SHIP Order 50:
→ current=950, reserved=0, available=950
→ Transaction: out -50

Result: ✅ Stock giảm 50, available giảm 50
```

### **Scenario 2: Order & Cancel**

```
Initial:  current=1000, reserved=0, available=1000

CREATE Order 100:
→ current=1000, reserved=100, available=900
→ Transaction: reserve +100

CANCEL Order 100:
→ current=1000, reserved=0, available=1000
→ Transaction: unreserve 100

Result: ✅ Trở lại trạng thái ban đầu
```

### **Scenario 3: Multiple Orders**

```
Initial: current=1000, reserved=0, available=1000

Order 1 (50) - CREATE:
→ current=1000, reserved=50, available=950

Order 2 (100) - CREATE:
→ current=1000, reserved=150, available=850

Order 1 (50) - SHIP:
→ current=950, reserved=100, available=850

Order 2 (100) - CANCEL:
→ current=950, reserved=0, available=950

Result: ✅ Chỉ Order 1 đã ship, Order 2 hủy
```

---

## ✅ Validation Rules

### **Khi Tạo Order:**
```python
# 1. Check available quantity
if inventory.available_quantity < order_quantity:
    raise ValueError("Not enough stock")

# 2. Check product has inventory
if not hasattr(product, 'inventory'):
    raise ValueError("Product has no inventory")

# 3. Atomic transaction
with transaction.atomic():
    # Create order + reserve inventory
```

### **Khi Ship:**
```python
# 1. Check order status
if order.order_status not in [CONFIRMED, PROCESSING]:
    raise ValueError("Order must be confirmed")

# 2. Check reserved quantity
if inventory.reserved_quantity < quantity:
    raise ValueError("Insufficient reserved quantity")

# 3. Decrease both current and reserved
```

### **Khi Cancel:**
```python
# 1. Check order status
if order.order_status in [SHIPPED, DELIVERED]:
    raise ValueError("Cannot cancel shipped orders")

# 2. Unreserve safely
inventory.reserved_quantity = max(0, inventory.reserved_quantity - quantity)
```

---

## 📈 Transaction History

### **Transaction Types:**

| Type | Khi Nào | Quantity | Current | Reserved |
|------|---------|----------|---------|----------|
| `reserve` | Create Order | +qty | Không đổi | Tăng |
| `unreserve` | Cancel Order | qty | Không đổi | Giảm |
| `out` | Ship Order | qty | Giảm | Giảm |

### **Transaction Structure:**
```python
InventoryTransaction {
    transaction_type: 'reserve' | 'unreserve' | 'out'
    quantity: float
    reference_number: "ORDER-{order_id}"
    reason: "Reserved for order X" | "Shipped for order X" | "Cancelled order X"
    created_by: User (nullable)
    created_at: DateTime
}
```

---

## 🎯 Key Points

### ✅ **Đúng:**
1. **CREATE ORDER → Reserve** (tăng `reserved_quantity`)
2. **SHIP ORDER → Decrease Both** (`current_quantity` và `reserved_quantity` giảm)
3. **CANCEL ORDER → Unreserve** (giảm `reserved_quantity`)
4. **Available = Current - Reserved** (luôn đúng)
5. **Transaction History** đầy đủ cho audit trail

### ❌ **Lưu Ý:**
1. **KHÔNG giảm `current_quantity` khi create order** (chỉ reserve)
2. **KHÔNG tăng `current_quantity` khi cancel order** (vì chưa xuất kho)
3. **PHẢI check `available_quantity`** khi tạo order (không phải `current_quantity`)
4. **PHẢI atomic transaction** để tránh race condition
5. **KHÔNG cho phép cancel order đã ship**

---

## 📊 Summary Flow Chart

```
                    CREATE ORDER
                         ↓
                  ┌──────────────┐
                  │  Reserve     │
                  │  Inventory   │
                  └──────────────┘
                         ↓
                   reserved++
                         ↓
                    ┌─────────┐
                    │ SHIP?   │
                    └─────────┘
                    ↙         ↘
                YES             NO (CANCEL)
                 ↓               ↓
         ┌──────────────┐   ┌──────────────┐
         │  Ship Order  │   │ Cancel Order │
         │  current--   │   │ unreserve    │
         │  reserved--  │   │ reserved--   │
         └──────────────┘   └──────────────┘
```

---

## 🔍 Kiểm Tra Database

### Query để kiểm tra:
```sql
-- Check inventory state
SELECT 
    p.id,
    p.name,
    i.current_quantity,
    i.reserved_quantity,
    (i.current_quantity - i.reserved_quantity) as available
FROM ecommerce_products p
LEFT JOIN ecommerce_inventory i ON p.id = i.product_id;

-- Check transaction history
SELECT 
    it.created_at,
    it.transaction_type,
    it.quantity,
    it.reference_number,
    it.reason
FROM ecommerce_inventory_transactions it
WHERE it.inventory_id = 'xxx'
ORDER BY it.created_at DESC;

-- Check orders with inventory impact
SELECT 
    o.id,
    o.order_status,
    oi.quantity,
    p.name,
    i.reserved_quantity
FROM ecommerce_orders o
JOIN ecommerce_order_items oi ON oi.order_id = o.id
JOIN ecommerce_products p ON oi.product_id = p.id
LEFT JOIN ecommerce_inventory i ON i.product_id = p.id;
```

---

## ✅ Kết Luận

**Logic khi khách hàng order sản phẩm là ĐÚNG:**

1. ✅ **Reserve khi tạo order** → Không cho khách khác mua số lượng đã đặt
2. ✅ **Decrease khi ship** → Xuất kho thực tế
3. ✅ **Unreserve khi cancel** → Trả lại số lượng có thể bán
4. ✅ **Transaction history đầy đủ** → Audit trail hoàn chỉnh
5. ✅ **Atomic operations** → Tránh race conditions
6. ✅ **Validation đầy đủ** → Prevent invalid operations

**Flow này đảm bảo:**
- Inventory accuracy (số liệu chính xác)
- Stock reservation (đặt trước đúng)
- Order fulfillment (xuất kho đúng)
- Audit trail (lịch sử đầy đủ)
- Data integrity (tính toàn vẹn)
