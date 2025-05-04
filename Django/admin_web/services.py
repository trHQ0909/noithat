from products.models import Category, CategoryMain, Product, ProductImage
from django.db.models import Sum
from order.models import Order,OrderDetail  # Import model Order
from customers.models import Customer
from django.db.models import Sum
from products.services import ( get_category_by_id,get_product_by_id
)
def get_statistics():
    # Đếm số đơn hàng
    total_orders = Order.objects.count()

    # Tổng số hàng tồn kho
    total_stock = Product.objects.aggregate(total_stock=Sum('stock'))['total_stock'] or 0

    # Tổng số hàng đã bán
    total_sold = Product.objects.aggregate(total_sold=Sum('sold'))['total_sold'] or 0

    return {
        "total_orders": total_orders,
        "total_stock": total_stock,
        "total_sold": total_sold
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