"""
Script to check Inventory Transaction History
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from ecommerce.models import (
    Product, 
    Inventory,
    InventoryTransaction,
    GoodsReceipt,
    GoodsReceiptItem
)
from django.db.models import Q, Sum, Count
from decimal import Decimal

User = get_user_model()

def print_divider(char="=", length=100):
    print(char * length)

def check_transaction_history():
    """Check inventory transaction history and verify data integrity"""
    
    print_divider()
    print("INVENTORY TRANSACTION HISTORY CHECK")
    print_divider()
    
    # 1. Overall Statistics
    print("\n📊 OVERALL STATISTICS")
    print_divider("-")
    
    total_transactions = InventoryTransaction.objects.count()
    total_inventories = Inventory.objects.count()
    total_products = Product.objects.count()
    
    print(f"Total Inventories: {total_inventories}")
    print(f"Total Products: {total_products}")
    print(f"Total Transactions: {total_transactions}")
    
    # Count by transaction type
    print("\n📈 Transactions by Type:")
    for tx_type, label in InventoryTransaction.TRANSACTION_TYPES:
        count = InventoryTransaction.objects.filter(transaction_type=tx_type).count()
        if count > 0:
            print(f"  {label:15} ({tx_type:10}): {count:5} transactions")
    
    # 2. Recent Transactions
    print("\n" + "=" * 100)
    print("🕒 RECENT TRANSACTIONS (Last 20)")
    print_divider("-")
    
    recent_txns = InventoryTransaction.objects.select_related(
        'inventory',
        'inventory__product',
        'inventory__product__name',
        'created_by'
    ).order_by('-created_at')[:20]
    
    if recent_txns.exists():
        print(f"\n{'ID':<8} {'Date/Time':<20} {'Type':<12} {'Quantity':<12} {'Ref Number':<20} {'Reason':<30}")
        print("-" * 100)
        
        for txn in recent_txns:
            try:
                product_name = txn.inventory.product.name.origin if txn.inventory.product.name else "N/A"
                product_name = product_name[:25] + "..." if len(product_name) > 25 else product_name
            except:
                product_name = "Unknown"
                
            date_str = txn.created_at.strftime('%Y-%m-%d %H:%M:%S')
            reason = (txn.reason[:27] + "...") if len(txn.reason) > 30 else txn.reason
            
            print(f"{txn.id:<8} {date_str:<20} {txn.transaction_type:<12} {txn.quantity:<12.2f} {txn.reference_number:<20} {reason:<30}")
            print(f"         └─ Product: {product_name}")
    else:
        print("⚠️  No transactions found!")
    
    # 3. Goods Receipt Related Transactions
    print("\n" + "=" * 100)
    print("📦 GOODS RECEIPT TRANSACTIONS")
    print_divider("-")
    
    gr_txns = InventoryTransaction.objects.filter(
        Q(reference_number__startswith='GR-') | Q(reference_number__contains='goods receipt')
    ).order_by('-created_at')[:10]
    
    if gr_txns.exists():
        print(f"\nFound {gr_txns.count()} Goods Receipt related transactions:")
        print(f"\n{'ID':<8} {'Type':<12} {'Qty':<10} {'Ref Number':<25} {'Date':<20}")
        print("-" * 100)
        
        for txn in gr_txns:
            date_str = txn.created_at.strftime('%Y-%m-%d %H:%M')
            print(f"{txn.id:<8} {txn.transaction_type:<12} {txn.quantity:<10.2f} {txn.reference_number:<25} {date_str:<20}")
    else:
        print("⚠️  No Goods Receipt transactions found!")
    
    # 4. Check Apply/Unapply Pairs
    print("\n" + "=" * 100)
    print("🔄 APPLY/UNAPPLY PAIR CHECK")
    print_divider("-")
    
    # Find GR-UNAPPLY transactions
    unapply_txns = InventoryTransaction.objects.filter(
        reference_number__contains='GR-UNAPPLY-'
    ).order_by('-created_at')[:5]
    
    if unapply_txns.exists():
        print(f"\nFound {unapply_txns.count()} UNAPPLY transactions:")
        
        for unapply in unapply_txns:
            print(f"\n🔸 Unapply Transaction #{unapply.id}")
            print(f"   Ref: {unapply.reference_number}")
            print(f"   Type: {unapply.transaction_type}")
            print(f"   Qty: {unapply.quantity}")
            print(f"   Date: {unapply.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Try to find matching apply
            gr_id = unapply.reference_number.replace('GR-UNAPPLY-', '')
            apply_txn = InventoryTransaction.objects.filter(
                reference_number=f'GR-{gr_id}',
                inventory=unapply.inventory
            ).order_by('-created_at').first()
            
            if apply_txn:
                print(f"   ✅ Found matching APPLY:")
                print(f"      Ref: {apply_txn.reference_number}")
                print(f"      Type: {apply_txn.transaction_type}")
                print(f"      Qty: {apply_txn.quantity}")
                print(f"      Date: {apply_txn.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Verify quantities match (opposite sign)
                if abs(apply_txn.quantity + unapply.quantity) < 0.01:
                    print(f"      ✅ Quantities match (reversed)")
                else:
                    print(f"      ❌ WARNING: Quantity mismatch!")
                    print(f"         Apply: {apply_txn.quantity}, Unapply: {unapply.quantity}")
            else:
                print(f"   ⚠️  No matching APPLY found")
    else:
        print("ℹ️  No UNAPPLY transactions found yet")
    
    # 5. Data Integrity Check
    print("\n" + "=" * 100)
    print("🔍 DATA INTEGRITY CHECK")
    print_divider("-")
    
    # Check for products with transactions but no inventory
    products_with_txns = InventoryTransaction.objects.values_list('inventory__product_id', flat=True).distinct()
    print(f"\nProducts with transactions: {len(set(products_with_txns))}")
    
    # Check inventories with transactions
    inventories_with_txns = InventoryTransaction.objects.values_list('inventory_id', flat=True).distinct()
    total_inventories_with_txns = len(set(inventories_with_txns))
    print(f"Inventories with transactions: {total_inventories_with_txns}")
    
    # Sample detailed check for one product
    print("\n📝 SAMPLE PRODUCT TRANSACTION HISTORY:")
    print_divider("-")
    
    sample_inventory = Inventory.objects.filter(
        transactions__isnull=False
    ).annotate(
        txn_count=Count('transactions')
    ).order_by('-txn_count').first()
    
    if sample_inventory:
        try:
            product_name = sample_inventory.product.name.origin
        except:
            product_name = "Unknown"
            
        print(f"\nProduct: {product_name}")
        print(f"Current Stock: {sample_inventory.current_quantity}")
        print(f"Transaction Count: {sample_inventory.transactions.count()}")
        
        print(f"\n{'Date':<20} {'Type':<12} {'Qty':<10} {'Running Total':<15} {'Reference':<30}")
        print("-" * 100)
        
        running_total = 0.0
        for txn in sample_inventory.transactions.order_by('created_at'):
            running_total += txn.quantity
            date_str = txn.created_at.strftime('%Y-%m-%d %H:%M')
            print(f"{date_str:<20} {txn.transaction_type:<12} {txn.quantity:<10.2f} {running_total:<15.2f} {txn.reference_number:<30}")
        
        print(f"\n✅ Final calculated stock: {running_total:.2f}")
        print(f"📊 Actual inventory stock: {sample_inventory.current_quantity:.2f}")
        
        if abs(running_total - sample_inventory.current_quantity) < 0.01:
            print("✅ Stock matches transaction history!")
        else:
            print("❌ WARNING: Stock mismatch!")
            print(f"   Difference: {abs(running_total - sample_inventory.current_quantity):.2f}")
    
    # 6. Orphaned Transactions Check
    print("\n" + "=" * 100)
    print("🔎 ORPHANED TRANSACTIONS CHECK")
    print_divider("-")
    
    orphaned = InventoryTransaction.objects.filter(
        inventory__isnull=True
    ).count()
    
    if orphaned > 0:
        print(f"⚠️  Found {orphaned} orphaned transactions (no inventory link)")
    else:
        print("✅ No orphaned transactions found")
    
    # 7. Summary
    print("\n" + "=" * 100)
    print("📋 SUMMARY")
    print_divider("-")
    
    print("\n✅ Transaction History Status:")
    print(f"  - Total Transactions: {total_transactions}")
    print(f"  - Active Inventories: {total_inventories}")
    print(f"  - Tracking Enabled: {'Yes' if total_transactions > 0 else 'No'}")
    
    if total_transactions == 0:
        print("\n⚠️  WARNING: No transactions found!")
        print("   This might mean:")
        print("   1. No goods receipts have been applied yet")
        print("   2. Transaction logging is not working")
        print("   3. Database was recently reset")
    else:
        print("\n✅ Transaction logging is working!")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    check_transaction_history()
