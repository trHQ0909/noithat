import os
from django.shortcuts import render, redirect
from django.conf import settings
from products.models import *
from .services import *
from accounts.services import *
from order.services import *
from django.contrib import messages  # Thêm dòng này
def main_view(request, category_id=None):
    """Hiển thị danh sách danh mục và sản phẩm (có thể lọc theo danh mục hoặc tìm kiếm)"""
    # Xử lý sản phẩm
    search_query = request.GET.get("search")
    
    if search_query:
        products = search_and_format_products(search_query)
    elif category_id:
        products = get_products_by_category(category_id)
    else:
        products = get_all_products_with_main_image()
    
    # Lấy danh mục
    categories = get_all_category_with_subcategories()
    
    # Chuẩn bị dữ liệu context chung
    context = {
        "categories": categories,
        "products": products,
    }
    
    # Xử lý giỏ hàng nếu có customer
    customerid = get_session_data(request, "customerid")
    if customerid:
        customer = get_customer_by_id(customerid)
        carts, total_amount = get_cart_items(customer)
        
        context.update({
            "count_Cart": count_Cart(customerid),
            "carts": carts,
            "total_amount": total_amount,
            "customer": customer
        })
    
    return render(request, "products/main.html", context)

def searchView(request,s=None,categoryid=None):
    """Hiển thị danh sách danh mục và sản phẩm (có thể lọc theo danh mục hoặc tìm kiếm)"""
    # Xử lý sản phẩm
    search_query = request.GET.get("search")
    orderby = request.GET.get("orderby")
    min_price=request.GET.get("min_price")
    max_price=request.GET.get("max_price")
    if not search_query or str(search_query).lower() == 'none':
      search_query = None
    
    if search_query or orderby or min_price or max_price :
        products = search_and_format_products(search_query,orderby,min_price,max_price,categoryid)
    elif categoryid:
        products = search_and_format_products(s,orderby,min_price,max_price,categoryid)
        search_query=s
    else:
        products = get_all_products_with_main_image()
    
    # Lấy danh mục
    categories = get_all_category_with_subcategories()
    minmax=get_price_range()
    
    # Chuẩn bị dữ liệu context chung
    context = {
        "categories": categories,
        "products": products,
        "s":search_query,
        "min":minmax['min_price'],
        "max":minmax['max_price']
    }
    
    # Xử lý giỏ hàng nếu có customer
    customerid = get_session_data(request, "customerid")
    if customerid:
        customer = get_customer_by_id(customerid)
        carts, total_amount = get_cart_items(customer)
        
        context.update({
            "count_Cart": count_Cart(customerid),
            "carts": carts,
            "total_amount": total_amount,
            "customer": customer
        })
    
    return render(request, "products/productSearch.html", context)

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
    customerid=get_session_data(request,"customerid")
    categories = get_all_category_with_subcategories()
    product = get_product_detail(product_id)
    products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
    product_ratings=get_product_rating_details(product_id)
    category_of_product=product['category']
    if customerid:
        count_cart=count_Cart(customerid)
            #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        if product:
            return render(request, "products/productDetail.html", {
                "product": product,
                "products": products,
                "product_ratings":product_ratings,
                "customer_reviews":product_ratings['customer_reviews'],
                "categories": categories,
                "carts":carts,
                "total_amount":total_amount,
                "category_of_product":category_of_product
                })
    else:
        return render(request, "products/productDetail.html", {
                "product": product,
                "products": products,
                "product_ratings":product_ratings,
                "customer_reviews":product_ratings['customer_reviews'],
                "categories": categories,
                "category_of_product":category_of_product
                })    
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

# ---------------- RATING ----------------
def addRating(request, product_id):
    print("aaaaaaaaaaa")
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        customerid = get_session_data(request, 'customerid')
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            messages.error(request, "Giá trị rating không hợp lệ.")
            return redirect("products_by_product_id", product_id)
        status, message, _ = add_or_update_product_rating(product_id, customerid, rating, comment)
        print(status)
        print(message)
        if status:
            messages.success(request, message)
            return redirect("products_by_product_id", product_id)
        else:
            messages.error(request, message)
            return redirect("product-home")
    # ✅ Xử lý cả khi không phải POST
    return redirect("product-home")
    
    





