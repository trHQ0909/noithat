from django.shortcuts import render,redirect
from accounts.services import *
from .services import * # Nếu addCart nằm trong services.py
from django.http import JsonResponse
from products.services import *
from accounts.services import *
from django.db.models import Sum
def addCart_view(request, productid,quantity):
    # Lấy customerid từ session
    customerid = get_session_data(request, 'customerid')

    if not customerid:  # Kiểm tra nếu chưa đăng nhập
        return redirect("MyAccount")  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập

    # Gọi hàm addCart (đã import)
    addCart(customerid,productid,quantity)

    return redirect("product-home")  # Chuyển hướng về trang chủ sau khi thêm vào giỏ hàng
def order_product_view(request,productid,quantity):
    customerid=get_session_data(request,'customerid')
    customer=get_customer_by_id(customerid)
    product=get_product_detail(productid)
    total_price=int(quantity)*int(product["price"])+30000
    return render(request, "order/order.html", {"customer":customer,"product": product, "quantity": quantity,"total_price":total_price})
def order_cart_view(request):
    customerid = get_session_data(request, "customerid")
    if request.method=='POST':
        if customerid:
            cart_ids=request.POST.getlist('cart_items[]')
            customer = get_customer_by_id(customerid)
            carts, total_amount=get_carts_by_ids(customer,cart_ids)
            return render(request, "order/orderCart.html", {"customer":customer,"carts": carts, "total_amount": total_amount})
        return redirect("MyAccount")
    return redirect("product-home")

def orderProduct(request,productid):
    customerid=get_session_data(request,'customerid')
    payment_method = request.POST.get("paymentMethod")
    address = request.POST.get("address")
    quantity=request.POST.get("quantity")
    product=get_product_detail(productid)
    total_price=0
    try:
        order = create_order(customerid, payment_method,total_price, address,status="pending")
        add_order_detail(order.orderid, productid,quantity)
        return redirect("product-home")
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
def orderCart(request):
    customerid=get_session_data(request,'customerid')
    payment_method = request.POST.get("paymentMethod")
    address = request.POST.get("address")
    quantity=request.POST.get("quantity")
    cart_ids = request.POST.getlist('cart_items[]')
    customer = get_customer_by_id(customerid)
    carts, total_amount=get_carts_by_ids(customer,cart_ids)
    total_price=0
    for cart in carts:
        product=get_product_detail(cart['productid'])
        qty = request.POST.get(f'cart[{cart["cartid"]}][qty]', cart['quantity'])
        qty = int(qty) if qty.isdigit() else cart['quantity']
        order = create_order(customerid, payment_method,total_price, address,status="pending")
        add_order_detail(order.orderid, cart['productid'],qty) 
    return redirect("product-home")
def cart_view(request):
    customerid = get_session_data(request, "customerid")
    
    # Kiểm tra nếu có customerid
    if customerid:
        count_cart = count_Cart(customerid)
        customer = get_customer_by_id(customerid)
        carts, total_amount = get_cart_items(customer)
        
        # Trả về render với context gồm giỏ hàng và thông tin tổng số tiền
        return render(request, "order/viewCart.html", {"carts": carts, "total_amount": total_amount, "count_Cart": count_cart})
    
    # Nếu không có customerid, chuyển hướng đến trang "MyAccount"
    return redirect("MyAccount")
