from products.models import Category, CategoryMain, Product, ProductImage
from django.db.models import Sum
from order.models import Order,OrderDetail  # Import model Order
from customers.models import Customer
from django.db.models import Sum
from products.services import *
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta

def get_statistics():
    total_orders = Order.objects.count()
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
    total_sold = Product.objects.aggregate(total=Sum('sold'))['total'] or 0
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    return {
        "total_orders": total_orders,
        "total_stock": total_stock,
        "total_sold": total_sold,
        "total_revenue": total_revenue
    }

def get_order_status_stats():
    pending = Order.objects.filter(status='Pending').count()
    shipped = Order.objects.filter(status='Shipped').count()
    completed = Order.objects.filter(status='Completed').count()
    cancelled = Order.objects.filter(status='Cancelled').count()
    result = {
        'labels': ['Đang chờ', 'Đã giao', 'Hoàn thành', 'Đã hủy'],
        'data': [pending, shipped, completed, cancelled]
    }
    print("Debug order_status_stats:", result)
    return result

def get_order_trend_data(days=30):
    date_from = timezone.now() - timedelta(days=days)
    daily_orders = (
        Order.objects
        .filter(order_date__gte=date_from)
        .annotate(date=TruncDay('order_date'))
        .values('date')
        .annotate(count=Count('orderid'), total=Sum('total_price'))
        .order_by('date')
    )
    
    labels = [entry['date'].strftime("%d-%m") for entry in daily_orders]
    order_counts = [entry['count'] for entry in daily_orders]
    revenues = [float(entry['total']) for entry in daily_orders]
    
    return {
        'labels': labels,
        'order_counts': order_counts,
        'revenues': revenues
    }

def get_top_products(limit=5):
    top_products = (
        OrderDetail.objects
        .values('productid__name')
        .annotate(total_sold=Sum('quantity'), revenue=Sum('subtotal'))
        .order_by('-total_sold')[:limit]
    )
    
    labels = [entry['productid__name'] for entry in top_products]
    total_sold = [entry['total_sold'] for entry in top_products]
    revenues = [float(entry['revenue']) for entry in top_products]
    
    return {
        'labels': labels,
        'total_sold': total_sold,
        'revenues': revenues
    }

def get_inventory_data():
    inventory_products = (
        Product.objects
        .order_by('-stock')[:10]
        .values('name', 'stock', 'sold')
    )
    
    labels = [entry['name'] for entry in inventory_products]
    stock = [entry['stock'] for entry in inventory_products]
    sold = [entry['sold'] for entry in inventory_products]
    
    return {
        'labels': labels,
        'stock': stock,
        'sold': sold
    }

def create_product(product_obj):
    """Tạo sản phẩm mới từ một đối tượng Product"""
    if product_obj.categoryid:
        product = Product.objects.create(
            name=product_obj.name,
            categoryid=product_obj.categoryid,
            price=product_obj.price,
            description=product_obj.description,
            sold=product_obj.sold,
            stock=product_obj.stock,
            status=product_obj.status
        )
        return product
    return None


def update_product(product_obj):
    if product_obj:
        product_obj.save()
        print("Sau khi cập nhật",product_obj)
        return product_obj
    return None

def delete_product(product_id):
    """Xóa sản phẩm và ảnh liên quan"""
    product = get_product_by_id(product_id)
    if product:
        # Xóa ảnh trước khi xóa sản phẩm
        ProductImage.objects.filter(productid=product).delete()
        product.delete()
        return True
    return False

# --------------- PRODUCT IMAGE -----------------
def get_product_images(product_id):
    """Lấy danh sách ảnh của sản phẩm"""
    return ProductImage.objects.filter(productid=product_id)
#----ORDER-----
def get_order_list():
    orders = Order.objects.select_related('customerid').values(
        'orderid',
        'customerid__name',  # Lấy tên khách hàng từ bảng Customer 
        # Django ORM hỗ trợ truy vấn qua khóa ngoại bằng cách sử dụng dấu hai gạch dưới (__).
        'order_date',
        'delivery_date',
        'total_price',
        'status'
    )

    return list(orders)


# -------------SOLD
def get_sold_products():
    sold_products = (
        OrderDetail.objects
        .select_related('productid')  # Lấy thông tin sản phẩm từ khóa ngoại
        .values('productid' ,'productid__name', 'quantity', 'price', 'subtotal', 'created_at')  # Thêm created_at
        .order_by('-created_at')  # Sắp xếp theo created_at giảm dần (mới nhất trước)
    )
    
    return sold_products
def get_total_revenue():
    total = OrderDetail.objects.aggregate(total_revenue=Sum('subtotal'))['total_revenue']
    return total or 0  # Trả về 0 nếu không có dữ liệu
#----------STOCK------
def get_stock_products():
    stock_products = (
        Product.objects
        .filter(stock__gt=0)  # Lọc sản phẩm còn hàng
        .values('productid', 'name','price','sold', 'stock','status')  # Lấy các trường cần thiết
        .order_by('-stock')  # Sắp xếp theo số lượng tồn kho giảm dần
    )
    return list(stock_products)
def get_total_stock():
    total_stock = Product.objects.aggregate(total_stock=Sum('stock'))['total_stock']
    return total_stock or 0  # Trả về 0 nếu không có dữ liệu