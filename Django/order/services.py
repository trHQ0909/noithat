from accounts.services import *
from customers.services import *
from products.services import *
from .models import *
from django.db import transaction
from django.utils import timezone
from .models import Order, Customer
from django.db.models import Sum
from datetime import datetime

def create_order(customerid, payment_method,total_price, address,status="pending"):
    """
    Tạo một đơn hàng mới.
    Args:
        customer_id (int): ID của khách hàng.
        payment_method (str): Phương thức thanh toán (VD: "COD", "Bank", "MoMo").
        address (str): Địa chỉ giao hàng.
        status (str): Trạng thái đơn hàng (mặc định là "pending").
    Returns:
        Order: Đối tượng đơn hàng vừa tạo.
    """
    try:
        customer = Customer.objects.get(customerid=customerid)
        order = Order(
            customerid=customer,
            order_date=timezone.now(),
            payment_method=payment_method,
            address=address,
            status=status,
            created_at=timezone.now(),
            total_price=total_price  # Tổng tiền sẽ được cập nhật sau khi thêm chi tiết đơn hàng
        )
        order.save()
        return order
    except Customer.DoesNotExist:
        raise ValueError("Khách hàng không tồn tại.")
    except Exception as e:
        raise Exception(f"Lỗi khi tạo đơn hàng: {str(e)}")
def add_order_detail(order_id, product_id, quantity):
    """
    Thêm chi tiết đơn hàng (sản phẩm) vào đơn hàng.
    Args:
        order_id (int): ID của đơn hàng.
        product_id (int): ID của sản phẩm.
        quantity (int): Số lượng sản phẩm.
    Returns:
        OrderDetail: Đối tượng chi tiết đơn hàng vừa tạo.
    """
    try:
        order = Order.objects.get(orderid=order_id)
        product = Product.objects.get(productid=product_id)
        
        # Giả định rằng Product có trường `price` để lấy giá sản phẩm
        price = product.price
        subtotal = int(quantity) * price
        
        order_detail = OrderDetail(
            orderid=order,
            productid=product,
            quantity=quantity,
            price=price,
            subtotal=subtotal,
            created_at=timezone.now()
        )
        order_detail.save()
        
        # Cập nhật tổng tiền của đơn hàng
        update_order_total(order_id)
        return order_detail
    except Order.DoesNotExist:
        raise ValueError("Đơn hàng không tồn tại.")
    except Product.DoesNotExist:
        raise ValueError("Sản phẩm không tồn tại.")
    except Exception as e:
        raise Exception(f"Lỗi khi thêm chi tiết đơn hàng: {str(e)}")
def update_order_total(order_id):
    """
    Cập nhật tổng tiền của đơn hàng dựa trên các chi tiết đơn hàng.
    Args:
        order_id (int): ID của đơn hàng.
    """
    try:
        order = Order.objects.get(orderid=order_id)
        total = OrderDetail.objects.filter(orderid=order).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        order.total_price = total
        order.save()
    except Order.DoesNotExist:
        raise ValueError("Đơn hàng không tồn tại.")
    except Exception as e:
        raise Exception(f"Lỗi khi cập nhật tổng tiền: {str(e)}")
def get_order_details(order_id):
    """
    Lấy thông tin đơn hàng và chi tiết đơn hàng.
    Args:
        order_id (int): ID của đơn hàng.
    Returns:
        dict: Thông tin đơn hàng và danh sách chi tiết.
    """
    try:
        order = Order.objects.get(orderid=order_id)
        order_details = OrderDetail.objects.filter(orderid=order)
        
        return {
            "order": {
                "order_id": order.orderid,
                "customer_id": order.customerid.customerid if order.customerid else None,
                "order_date": order.order_date,
                "delivery_date": order.delivery_date,
                "total_price": order.total_price,
                "status": order.status,
                "payment_method": order.payment_method,
                "address": order.address,
                "created_at": order.created_at
            },
            "details": [
                {
                    "product_id": detail.productid.productid if detail.productid else None,
                    "quantity": detail.quantity,
                    "price": detail.price,
                    "subtotal": detail.subtotal
                } for detail in order_details
            ]
        }
    except Order.DoesNotExist:
        raise ValueError("Đơn hàng không tồn tại.")
    except Exception as e:
        raise Exception(f"Lỗi khi lấy thông tin đơn hàng: {str(e)}")
def addCart(customerid, productid, quantity=1):
    """Thêm sản phẩm vào giỏ hàng hoặc cập nhật số lượng nếu đã tồn tại"""
    customer=get_customer_by_id(customerid)
    product=get_product_by_id(productid)
    try:
        with transaction.atomic():
            cart_item = Cart.objects.filter(customerid=customerid, productid=product).first()
            
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item = Cart.objects.create(
                    customerid=customer,
                    productid=product,
                    quantity=quantity
                )
            
            return cart_item
    except Exception as e:
        raise ValueError(f"Error adding product to cart: {e}")
def getListOrder(customer_id):
    """
    Lấy danh sách các orderDetail của khách hàng, bao gồm:
    - Thông tin sản phẩm (tên, ảnh chính, ID)
    - Chi tiết đơn hàng (orderdetail_id, quantity, price, subtotal, order_id, order_date)
    
    Args:
        customer_id (int): ID của khách hàng.
    
    Returns:
        list: Danh sách các dictionary chứa thông tin orderDetail và sản phẩm tương ứng.
    """
    order_details = OrderDetail.objects.filter(
        orderid__customerid=customer_id
    ).select_related(
        'productid',
        'orderid'
    ).prefetch_related(
        Prefetch('productid__images', queryset=ProductImage.objects.filter(is_main=True), to_attr='main_images')
    )

    results = []
    for order_detail in order_details:
        product = order_detail.productid
        main_image_url = product.main_images[0].image_url if hasattr(product, 'main_images') and product.main_images else None
        
        results.append({
            'product_id': product.productid,
            'product_name': product.name,
            'image_url': main_image_url,
            'orderdetail_id': order_detail.orderdetailid,
            'quantity': order_detail.quantity,
            'price': order_detail.price,
            'subtotal': order_detail.subtotal,
            'order_id': order_detail.orderid.orderid,
            'order_date': order_detail.orderid.order_date,
            'status': order_detail.orderid.status  # Thêm trường status từ Order
        })

    return results
# CART


def get_cart_items(customer):
    """Lấy danh sách sản phẩm trong giỏ hàng của khách hàng và tổng giá"""
    cart_items = Cart.objects.filter(customerid=customer).select_related("productid")
    
    result = []
    total_amount = 0  # Biến lưu tổng tiền

    for item in cart_items:
        main_image = item.productid.images.filter(is_main=True).first()
        total_price = int(item.quantity) * item.productid.price
        total_amount += total_price  # Cộng dồn vào tổng tiền

        result.append({
            "cartid":item.cartid,
            "product_name": item.productid.name,
            "productid":item.productid.productid,
            "price": item.productid.price,
            "quantity": item.quantity,
            "total_price": total_price,
            "image_url": main_image.image_url if main_image else None
        })  
    
    return result, total_amount  # Trả về cả danh sách và tổng tiền
def get_carts_by_ids(customer, cart_ids=None):
    """Lấy danh sách sản phẩm trong giỏ hàng của khách hàng và tổng giá, lọc theo cart_ids nếu có"""
    # Nếu cart_ids không được cung cấp, lấy tất cả giỏ hàng của khách hàng
    if cart_ids:
        cart_items = Cart.objects.filter(
            customerid=customer,
            cartid__in=cart_ids
        ).select_related("productid")
    else:
        cart_items = Cart.objects.filter(
            customerid=customer
        ).select_related("productid")
    
    result = []
    total_amount = 0  # Biến lưu tổng tiền

    for item in cart_items:
        main_image = item.productid.images.filter(is_main=True).first()
        total_price = int(item.quantity) * item.productid.price
        total_amount += total_price  # Cộng dồn vào tổng tiền

        result.append({
            "cartid": item.cartid,
            "product_name": item.productid.name,
            "productid": item.productid.productid,
            "price": item.productid.price,
            "quantity": item.quantity,
            "total_price": total_price,
            "image_url": main_image.image_url if main_image else None
        })
    
    return result, total_amount
def count_Cart(customerid):
    """Đếm số lượng sản phẩm trong giỏ hàng của khách hàng"""
    return Cart.objects.filter(customerid=customerid).count()
def update_cart(customer, quantity, cartid):
    try:
        # Lấy đối tượng Cart cần cập nhật bằng cartid
        cart = Cart.objects.get(cartid=cartid)

        # Kiểm tra nếu customer_id có trùng với customer của cart, nếu không thì thông báo lỗi
        if cart.customerid != customer:
            raise ValueError("Customer không trùng với cart hiện tại.")

        # Cập nhật số lượng (quantity)
        cart.quantity = quantity

        # Lưu lại các thay đổi vào cơ sở dữ liệu
        cart.save()

        return cart
    except Cart.DoesNotExist:
        print(f"Không tìm thấy cart với ID {cartid}.")
        return None
    except ValueError as ve:
        print(ve)
        return None
#   Thêm rating
