from django.shortcuts import render,redirect
from django.urls import reverse # Đây là dòng import đúng
from .services import *
from django.http import JsonResponse
from accounts.services import *
from .services import *
from accounts.services import *
from order.services import *
def InfomationCustomer(request,customerid):
    return render(request, "customer/Registercustomer.html",{"customerid": customerid})
def customer(request,category_id=None):
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        listOrder=getListOrder(customer)
        #----
        if category_id:
            products = get_products_by_category(category_id)  # Lọc sản phẩm theo danh mục
        else:
            products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        
        return render(request, "customer/Info_customer.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer,
            "Orders":listOrder
        })
    else :
        if category_id:
            products = get_products_by_category(category_id)  # Lọc sản phẩm theo danh mục
        else:
            products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        
        return render(request, "customer/Info_customer.html", {
            "categories": categories,
            "products": products,
        })
def registerCustomer(request,customerid=None):
 
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        date = request.POST.get("date")
        gender = request.POST.get("gender")
        sess=get_session_data(request,'customerid')

        success = update_customer(customerid, name, phone, address, date, gender)
        if success and sess==None:
            return redirect("MyAccount")
        else:
            return render(request, "customer/Registercustomer.html")

    return redirect('inputInfo', customerid)
def get_edit_form(request):
    customerid=get_session_data(request,'customerid')
    customer=get_customer_by_id(customerid)
    return render(request, "customer/editCustomer.html", {'customer': customer})
def updateCustomer(request):
    if request.method == 'POST':
        customerid = get_session_data(request, 'customerid')
        name = request.POST.get('name')
        address = request.POST.get('address')
        date = request.POST.get('date_of_birth')
        phone = request.POST.get('register_phone')
        gender = request.POST.get('gender')

        success = update_customer(customerid, name, phone, address, date, gender) # Gọi hàm service
        if success:
            return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công', 'redirect_url': reverse('customer')})
            # redirect('customes')
        else:
            return JsonResponse({'status': 'error', 'message': 'Lỗi khi cập nhật thông tin'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Phương thức không được hỗ trợ'}, status=400)
