from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..models import Product, Order, Customer, OrderItem
from ..constants import OrderStatus, PaymenStatus


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def general_statistics(request):
    """
    Get general statistics for ecommerce dashboard
    """
    try:
        # Calculate date ranges
        today = timezone.now().date()
        last_month_start = today.replace(day=1) - timedelta(days=1)
        last_month_start = last_month_start.replace(day=1)
        current_month_start = today.replace(day=1)
        
        # Total counts
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_customers = Customer.objects.count()
        
        # Total revenue
        total_revenue = OrderItem.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Growth calculations
        # Products growth
        products_last_month = Product.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=current_month_start
        ).count()
        products_this_month = Product.objects.filter(
            created_at__gte=current_month_start
        ).count()
        products_growth = calculate_growth_percentage(products_last_month, products_this_month)
        
        # Orders growth
        orders_last_month = Order.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=current_month_start
        ).count()
        orders_this_month = Order.objects.filter(
            created_at__gte=current_month_start
        ).count()
        orders_growth = calculate_growth_percentage(orders_last_month, orders_this_month)
        
        # Customers growth
        customers_last_month = Customer.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=current_month_start
        ).count()
        customers_this_month = Customer.objects.filter(
            created_at__gte=current_month_start
        ).count()
        customers_growth = calculate_growth_percentage(customers_last_month, customers_this_month)
        
        # Revenue growth
        revenue_last_month = OrderItem.objects.filter(
            order__created_at__gte=last_month_start,
            order__created_at__lt=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        revenue_this_month = OrderItem.objects.filter(
            order__created_at__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        revenue_growth = calculate_growth_percentage(revenue_last_month, revenue_this_month)
        
        data = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'products_growth': products_growth,
            'orders_growth': orders_growth,
            'customers_growth': customers_growth,
            'revenue_growth': revenue_growth
        }
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_data(request):
    """
    Get sales data for chart visualization
    """
    try:
        period = request.GET.get('period', '30d')
        
        # Calculate date range based on period
        end_date = timezone.now().date()
        if period == '7d':
            start_date = end_date - timedelta(days=7)
        elif period == '30d':
            start_date = end_date - timedelta(days=30)
        elif period == '3m':
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get daily sales data
        sales_data = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            orders=Count('id'),
            revenue=Sum('orderitem__amount')
        ).order_by('date')
        
        # Fill missing dates with zero values
        data = []
        current_date = start_date
        sales_dict = {item['date']: item for item in sales_data}
        
        while current_date <= end_date:
            if current_date in sales_dict:
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'orders': sales_dict[current_date]['orders'],
                    'revenue': sales_dict[current_date]['revenue'] or 0
                })
            else:
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'orders': 0,
                    'revenue': 0
                })
            current_date += timedelta(days=1)
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_status_data(request):
    """
    Get order status distribution data
    """
    try:
        status_data = Order.objects.values('order_status').annotate(
            count=Count('id')
        ).order_by('order_status')
        
        # Map status codes to readable names
        status_map = dict(OrderStatus.CHOICES)
        
        data = []
        for item in status_data:
            data.append({
                'status': status_map.get(item['order_status'], 'Unknown'),
                'status_code': item['order_status'],
                'count': item['count']
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def recent_orders(request):
    """
    Get recent orders for dashboard
    """
    try:
        limit = int(request.GET.get('limit', 5))
        
        orders = Order.objects.select_related('customer').prefetch_related(
            'items'
        ).order_by('-created_at')[:limit]
        
        data = []
        for order in orders:
            total_amount = order.items.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            data.append({
                'id': order.id,
                'customer_name': order.customer_name or (
                    f"{order.customer.first_name} {order.customer.last_name}" 
                    if order.customer else "Guest"
                ),
                'total_amount': total_amount,
                'order_status': order.order_status,
                'payment_status': order.payment_status,
                'created_at': order.created_at.isoformat()
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def top_products(request):
    """
    Get top selling products
    """
    try:
        limit = int(request.GET.get('limit', 5))
        
        # Get products with their sales data
        products = Product.objects.annotate(
            sold_quantity=Sum('orderitem__quantity'),
            total_revenue=Sum('orderitem__amount')
        ).filter(
            sold_quantity__isnull=False
        ).order_by('-sold_quantity')[:limit]
        
        data = []
        for product in products:
            # Get product name from related content
            product_name = "Unknown Product"
            if product.name:
                try:
                    # Assuming name is a ForeignKey to ShortContent
                    product_name = str(product.name)
                except:
                    product_name = f"Product #{product.id}"
            
            data.append({
                'id': product.id,
                'name': product_name,
                'price': product.price,
                'sold_quantity': product.sold_quantity or 0,
                'in_stock': product.in_stock,
                'total_revenue': product.total_revenue or 0,
                'thumbnail': product.thumbnail.url if product.thumbnail else None
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_alerts(request):
    """
    Get inventory alerts for low stock products
    """
    try:
        # Products with low stock (less than 10 items)
        low_stock_threshold = 10
        
        low_stock_products = Product.objects.filter(
            in_stock__lt=low_stock_threshold,
            in_stock__gt=0
        ).order_by('in_stock')
        
        # Out of stock products
        out_of_stock_products = Product.objects.filter(
            in_stock=0
        )
        
        data = {
            'low_stock': [],
            'out_of_stock': [],
            'low_stock_count': low_stock_products.count(),
            'out_of_stock_count': out_of_stock_products.count()
        }
        
        # Add low stock products
        for product in low_stock_products[:10]:  # Limit to 10
            product_name = "Unknown Product"
            if product.name:
                try:
                    product_name = str(product.name)
                except:
                    product_name = f"Product #{product.id}"
            
            data['low_stock'].append({
                'id': product.id,
                'name': product_name,
                'in_stock': product.in_stock,
                'price': product.price
            })
        
        # Add out of stock products
        for product in out_of_stock_products[:10]:  # Limit to 10
            product_name = "Unknown Product"
            if product.name:
                try:
                    product_name = str(product.name)
                except:
                    product_name = f"Product #{product.id}"
            
            data['out_of_stock'].append({
                'id': product.id,
                'name': product_name,
                'in_stock': product.in_stock,
                'price': product.price
            })
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def calculate_growth_percentage(previous, current):
    """
    Calculate growth percentage between two values
    """
    if previous == 0:
        return 100 if current > 0 else 0
    
    growth = ((current - previous) / previous) * 100
    return round(growth, 1)
