import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
from products.models import Category, CategoryMain, Product, ProductImage
from products.services import *
from admin_web.services import *
from accounts.services import *
from order.services import *
def main_view(request, category_id=None):
    """Hiển thị danh sách danh mục và sản phẩm (có thể lọc theo danh mục)"""
    statistics=get_statistics()
    orders=get_order_list()
    sold_products=get_sold_products()
    stock_products=get_stock_products()
    total_stock=get_total_stock()
    total_revenue=get_total_revenue()

    
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    
    if category_id:
        products = get_products_by_category(category_id)  # Lọc sản phẩm theo danh mục
    else:
        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
    
    return render(request, "admin_web/manage.html", {
        "categories": categories,
        "products": products,
        "statistics":statistics,
        "orders":orders,
        "sold_products":sold_products,
        "stock_products":stock_products,
        "total_revenue":total_revenue,
        "total_stock":total_stock,
    })
def get_next_folder_number(base_path):
    """Tìm thư mục có số thứ tự cao nhất và trả về số tiếp theo."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)  # Tạo thư mục nếu chưa tồn tại
        return 1
    
    existing_folders = [int(folder) for folder in os.listdir(base_path) if folder.isdigit()]
    return max(existing_folders, default=0) + 1  # Nếu không có thư mục nào thì bắt đầu từ 1

def create_product_view(request):
    """Tạo sản phẩm mới và lưu ảnh vào thư mục riêng."""
    categories = get_all_categories()
    
    if request.method == "POST":
        name = request.POST.get("name")
        category_id =request.POST.get("category_id")
        price = request.POST.get("price")
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        sold=0
        status = 1
        images = request.FILES.getlist("images")  # Lấy danh sách file ảnh
        # Tạo sản phẩm trong database
        print(f"DEBUG: category_id = {category_id}")
        try:
            category_id = int(category_id)
            category = Category.objects.get(pk=category_id)  # Lấy đối tượng Category
        except (ValueError, Category.DoesNotExist):
            return render(request, "products/main.html", {
                "categories": categories,
                "error": "Danh mục không hợp lệ hoặc không tồn tại."
            })
        product_obj = create_product(Product(
            name=name, categoryid=category, price=price,
            description=description, stock=stock, status=status,sold=sold
        ))

        if product_obj:
            for index, image in enumerate(images):
                # Tạo đường dẫn lưu file ảnh
                image_filename = f"{index}_{image.name}"  # Đặt tên file theo số thứ tự
                image_path = os.path.join(settings.MEDIA_ROOT, image_filename)

                # Lưu file ảnh vào thư mục
                with open(image_path, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                # Lưu đường dẫn vào database
                is_main = (index == 0)  # Ảnh đầu tiên sẽ là ảnh chính
                ProductImage.objects.create(
                    productid=product_obj,
                    image_url=f"{image_filename}",
                    is_main=is_main
                )

            return redirect("product-list")

    return render(request, "products/main.html", {"categories": categories})


def update_product_view(request, product_id):
    """Cập nhật sản phẩm, đối chiếu ảnh để xóa, giữ hoặc thêm mới."""
    product=get_product_by_id(product_id)
    productdetail = get_product_detail(product_id)
    categories = get_all_categories()
 
    if request.method == "POST":
        # Lấy dữ liệu từ form
        name = request.POST.get("name")
        category_id = request.POST.get("category_id")
        price = request.POST.get("price")
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        soldtest = request.POST.get("sold","0")
        if soldtest=="":
            sold=0
        else : sold=soldtest
        status = request.POST.get("status", 1)  # Nếu không có, mặc định là 1
        new_images = request.FILES.getlist("images")  # Danh sách ảnh từ form
        
        # Cập nhật thông tin sản phẩm
        product.name = name
        product.categoryid = get_category_by_id(category_id)
        product.price = price
        product.description = description
        product.stock = stock
        product.sold = sold
        product.status = status
        update_product(product)

        # **Xử lý ảnh**
        existing_images = list(ProductImage.objects.filter(productid=product).values_list("image_url", flat=True))
        new_image_names = [image.name for image in new_images]

        # **Xóa ảnh không còn sử dụng**
        for image_url in existing_images:
                ProductImage.objects.filter(productid=product, image_url=image_url).delete()
                image_path = os.path.join(settings.MEDIA_ROOT, image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)  # Xóa file ảnh thực tế

        # **Thêm ảnh mới**
        for index, image in enumerate(new_images):
                image_filename = f"{index}_{image.name}"
                image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
                
                with open(image_path, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)

                is_main = (index == 0)  # Ảnh đầu tiên sẽ là ảnh chính
                ProductImage.objects.create(
                    productid=product,
                    image_url=image_filename,
                    is_main=is_main
                )

        return redirect("product-list")

    return render(request, "products/update_product.html", {
        "product": product,
        "categories": categories
    })


@csrf_exempt  # Nếu dùng fetch API mà không có CSRF token
def delete_product_view(request, product_id):
    """Xóa sản phẩm"""
    if request.method == "DELETE":  # Chỉ chấp nhận DELETE request
        delete_product(product_id)
        return JsonResponse({"message": f"Đã xóa sản phẩm {product_id}"})
    return JsonResponse({"error": "Phương thức không được phép"}, status=405)  # Trả về lỗi nếu không phải DELETE
def get_product_detail_update(request,product_id):
    product=get_product_detail(product_id)
    categories = get_all_category_with_subcategories()
    return render(request, "admin_web/update_product.html", {
        "categories": categories,
        "product": product
    })
def get_product_detail_view(request,product_id):
    product=get_product_detail(product_id)
    categories = get_all_category_with_subcategories()
    return render(request, "admin_web/update_product.html", {
        "categories": categories,
        "product": product
    })
    
    
# ABOUT US
def aboutus(request):
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        ratings=get_all_ratings()

        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/aboutus.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer,
            "ratings":ratings
        })
    else :
        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/aboutus.html", {
            "categories": categories,
            "products": products,
        })
def contactUs(request):
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        ratings=get_all_ratings()

        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/contactUs.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer,
            "ratings":ratings
        })
    else :
        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/contactUs.html", {
            "categories": categories,
            "products": products,
        })
def FAQ(request):
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        ratings=get_all_ratings()

        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/FAQ.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer,
            "ratings":ratings
        })
    else :
        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/FAQ.html", {
            "categories": categories,
            "products": products,
        })
def Ship_return(request):
    categories = get_all_category_with_subcategories()  # Lấy danh mục chính và danh mục phụ
    customerid=get_session_data(request,"customerid")
    if customerid:
        count_cart=count_Cart(customerid)
        #---CART
        customer=get_customer_by_id(customerid)
        carts,total_amount=get_cart_items(customer)
        ratings=get_all_ratings()

        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/ship_return.html", {
            "categories": categories,
            "products": products,
            "count_Cart":count_cart,
            "carts":carts,
            "total_amount":total_amount,
            "customer":customer,
            "ratings":ratings
        })
    else :
        products = get_all_products_with_main_image()  # Lấy tất cả sản phẩm nếu không lọc
        return render(request, "admin_web/ship_return.html", {
            "categories": categories,
            "products": products,
        })