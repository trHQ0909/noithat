import os
from django.shortcuts import render, redirect
from django.conf import settings
from products.models import *
from .services import *
from accounts.services import *
from order.services import *
def main_view(request, category_id=None):
    """Hiển thị danh sách danh mục và sản phẩm (có thể lọc theo danh mục)"""
    
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        #----
        if category_id:
            products = get_products_by_category(category_id)  # Lọc sản phẩm theo danh mục
        else:
            products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        
        return render(request, "products/main.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer
        })
    else :
        if category_id:
            products = get_products_by_category(category_id)  # Lọc sản phẩm theo danh mục
        else:
            products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        
        return render(request, "products/main.html", {
            "categories": categories,
            "products": products,
        })


# ---------------- CATEGORY VIEWS ----------------
def category_list_view(request):
    """Hiển thị danh sách danh mục chính và danh mục phụ"""
    categories = get_all_category_with_subcategories()
    return render(request, "products/main.html", {"categories": categories})

# ---------------- PRODUCT VIEWS ----------------
def product_list_view(request):
    products = get_all_products_with_main_image()
    return render(request, "products/product_list.html", {"products": products})
def products_by_category_view(request, category_id):
    """Hiển thị danh sách sản phẩm theo danh mục"""
    products = get_products_by_category(category_id)
    return render(request, "products/main.html", {"products": products})

def product_detail_view(request, product_id):
    """Hiển thị chi tiết sản phẩm"""
    product = get_product_detail(product_id)
    if product:
        return render(request, "products/detail.html", {"product": product})
    return redirect("product-home")

# ---------------- CATEGORY MANAGEMENT ----------------
def create_category_view(request):
    """Tạo danh mục mới"""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_obj = Category(name=name, description=description)
        create_category(category_obj)
        return redirect("category_list")
    return render(request, "products/create_category.html")

def update_category_view(request, category_id):
    """Cập nhật danh mục"""
    category = get_category_by_id(category_id)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.description = request.POST.get("description")
        update_category(category)
        return redirect("category_list")
    return render(request, "products/update_category.html", {"category": category})

def delete_category_view(request, category_id):
    """Xóa danh mục"""
    delete_category(category_id)
    return redirect("category_list")

# ---------------- CART ----------------





