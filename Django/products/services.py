from products.models import Category, CategoryMain, Product, ProductImage,ProductRating
from order.models import Cart
from customers.models import Customer
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.db.models import Count, Avg
from decimal import Decimal
from datetime import datetime
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models import Q, Prefetch
from django.db.models.functions import Coalesce
from django.db.models import Q, F, Case, When, Value, FloatField
from django.db.models import Max, Min
# --------------- CATEGORY MAIN -----------------
def get_all_category_mains():
    """Lấy tất cả danh mục chính (CategoryMain)"""
    return CategoryMain.objects.all()

def get_sub_categories_by_main(main_category_id):
    """Lấy danh sách Category phụ theo CategoryMain"""
    return Category.objects.filter(main_category_id=main_category_id)

def get_all_category_with_subcategories():
    """Lấy tất cả CategoryMain cùng danh sách Category phụ của nó"""
    category_data = []
    category_mains = get_all_category_mains()
    
    for main in category_mains:
        sub_categories = get_sub_categories_by_main(main.id)
        category_data.append({
            "main_category": main,
            "sub_categories": list(sub_categories)
        })
    
    return category_data

# --------------- CATEGORY -----------------
def get_all_categories():
    """Lấy tất cả danh mục"""
    return Category.objects.all()

def get_category_by_id(category_id):
    """Lấy danh mục theo ID"""
    try:
        return Category.objects.get(categoryid=category_id)
    except Category.DoesNotExist:
        return None

def create_category(category_obj):
    """Tạo danh mục mới từ một đối tượng Category"""
    return Category.objects.create(
        name=category_obj.name,
        description=category_obj.description
    )

def update_category(category_obj):
    """Cập nhật danh mục từ một đối tượng Category"""
    category = get_category_by_id(category_obj.categoryid)
    if category:
        category.name = category_obj.name
        category.description = category_obj.description
        category.save()
        return category
    return None

def delete_category(category_id):
    """Xóa danh mục và tất cả sản phẩm bên trong"""
    category = get_category_by_id(category_id)
    if category:
        category.product_set.all().delete()  # Xóa tất cả sản phẩm thuộc category này
        category.delete()

# --------------- PRODUCT -----------------
def get_all_products():
    """Lấy tất cả sản phẩm"""
    return Product.objects.all()
def get_all_products_with_main_image():
    """Lấy tất cả sản phẩm và ảnh chính của mỗi sản phẩm"""
    products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=ProductImage.objects.filter(is_main=True),
            to_attr='main_image'
        )
    )

    # Định dạng dữ liệu trả về
    result = []
    for product in products:
        image_url = product.main_image[0].image_url if product.main_image else None
        result.append({
            'productid': product.productid,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'stock': product.stock,
            'status': product.status,
            'image_url': image_url  # Đường dẫn ảnh chính (nếu có)
        })
    
    return result

def get_products_by_category(category_id):
    products = Product.objects.filter(categoryid=category_id).prefetch_related(
        Prefetch(
            'images',
            queryset=ProductImage.objects.filter(is_main=True),
            to_attr='main_image'
        )
    )

    result = []
    for product in products:
        image_url = product.main_image[0].image_url if product.main_image else None
        result.append({
            'productid': product.productid,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'stock': product.stock,
            'sold':product.sold,
            'status': product.status,
            'image_url': image_url
        })
    
    return result


def get_product_by_id(product_id):
    """Lấy sản phẩm theo ID"""
    try:
        return Product.objects.get(productid=product_id)
    except Product.DoesNotExist:
        return None

def get_product_detail(product_id):
    """Lấy thông tin sản phẩm, ảnh và category (gồm cả main_category)"""
    product = get_product_by_id(product_id)
    if product:
        images = list(ProductImage.objects.filter(productid=product).values('image_url', 'is_main'))
        category = product.categoryid
        main_category = category.main_category if category else None

        product_detail = {
            "productid": product.productid,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "sold": product.sold,
            "stock": product.stock,
            "status": product.status,
            "average_rating": product.average_rating,
            "total_reviews": product.total_reviews,
            "images": images,
            "category_id":category.categoryid,

            # Thông tin Category
            "category": {
                "categoryid": category.categoryid if category else None,
                "name": category.name if category else None,
                "description": category.description if category else None,
            } if category else None,

            # Thông tin Main Category (nếu có)
            "main_category": {
                "id": main_category.id,
                "name": main_category.name
            } if main_category else None,
        }
        return product_detail
    return None
#-----------RATING
def get_product_rating_details(product_id):
    try:
        product = Product.objects.get(productid=product_id)
        
        # Lấy số lượng từng loại rating (1-5 sao)
        rating_distribution = (
            ProductRating.objects
            .filter(productid=product_id)
            .values('rating')
            .annotate(count=Count('rating'))
            .order_by('rating')
        )
        
        # Chuyển đổi thành dict {rating: count} và tính phần trăm
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        rating_percents = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        total_reviews = product.total_reviews or 1  # Tránh chia cho 0
        
        for item in rating_distribution:
            rating = item['rating']
            if rating in rating_counts:
                count = item['count']
                rating_counts[rating] = count
                # Tính phần trăm và làm tròn 2 chữ số thập phân
                rating_percents[rating] = round((count / total_reviews) * 100, 2)
        
        # Lấy danh sách đánh giá của khách hàng
        customer_reviews = (
            ProductRating.objects
            .filter(productid=product_id)
            .select_related('customerid')
            .order_by('-created_at')
            .values(
                'customerid__name',
                'rating',
                'comment',
                'created_at'
            )
        )
        for review in customer_reviews:
            review['rating_percent'] = round((review['rating'] * 100 / 5), 2)
            
        avg_rating=float(product.average_rating) if product.average_rating else 0
        avg_rating_percent=round(avg_rating*100/5,2)
        return {
            'product_id': product_id,
            'product_name': product.name,
            'average_rating': avg_rating,
            'avg_rating_percent':avg_rating_percent,
            'total_reviews': product.total_reviews or 0,
            'rating_counts': rating_counts,
            'rating_percents': rating_percents,  # Thêm thông tin phần trăm
            'customer_reviews': list(customer_reviews)
        }
        
    except Product.DoesNotExist:
        return {
            'error': 'Product not found',
            'product_id': product_id
        }
# Thêm rating
def add_or_update_product_rating(product_id, customer_id, rating_value, comment=None):
    """
    Thêm hoặc cập nhật đánh giá sản phẩm
    Args:
        product_id: ID sản phẩm
        customer_id: ID khách hàng
        rating_value: Giá trị rating (1-5)
        comment: Bình luận (optional)
    Returns:
        Tuple (status, message, rating_obj)
        - status: True/False
        - message: Thông báo kết quả
        - rating_obj: Đối tượng rating được tạo/cập nhật
    """
    try:
        # Validate rating value
        if not 1 <= rating_value <= 5:
            return False, "Rating phải từ 1 đến 5 sao", None

        with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
            # Kiểm tra tồn tại sản phẩm và khách hàng
            product = Product.objects.get(productid=product_id)
            customer = Customer.objects.get(customerid=customer_id)

            # Kiểm tra xem khách hàng đã đánh giá sản phẩm chưa
            rating, created = ProductRating.objects.get_or_create(
                productid=product,
                customerid=customer,
                defaults={
                    'rating': rating_value,
                    'comment': comment,
                    'created_at': datetime.now()
                }
            )
            if not created:
                # Nếu đã tồn tại, cập nhật rating
                old_rating = rating.rating
                rating.rating = rating_value
                if comment is not None:
                    rating.comment = comment
                rating.save()
                message = f"Cập nhật đánh giá từ {old_rating} sao lên {rating_value} sao"
            else:
                message = "Thêm đánh giá mới thành công"

            # Cập nhật thống kê rating trên product
            update_product_rating_stats(product)

            return True, message, rating

    except Product.DoesNotExist:
        return False, "Sản phẩm không tồn tại", None
    except Customer.DoesNotExist:
        return False, "Khách hàng không tồn tại", None
    except Exception as e:
        return False, f"Lỗi hệ thống: {str(e)}", None

def update_product_rating_stats(product):
    stats = ProductRating.objects.filter(
        productid=product
    ).aggregate(
        average=Avg('rating'),
        total=Count('rating_id')  # Đếm theo khóa chính thực tế
    )
    product.average_rating = stats['average'] or 0
    product.total_reviews = stats['total'] or 0
    product.save()

def get_all_ratings():
    """
    Lấy tất cả các đánh giá trong hệ thống
    Trả về danh sách chứa các thông tin:
    - ID đánh giá
    - Số sao (rating)
    - Tỷ lệ phần trăm (sao*100/5)
    - Tên sản phẩm được đánh giá
    - Tên người đánh giá
    - Bình luận
    - Ngày đánh giá
    """
    ratings = ProductRating.objects.all().select_related('productid', 'customerid').annotate(
        percentage=ExpressionWrapper(
            F('rating') * 100 / 5,
            output_field=FloatField()
        ),
        product_name=F('productid__name'),
        customer_name=F('customerid__name')
    ).values(
        'rating_id',
        'rating',
        'percentage',
        'product_name',
        'customer_name',
        'comment',
        'created_at'
    ).order_by('-created_at')

    return list(ratings)

# SEARCH :TÌM KIẾM
# def search_and_format_products(search_query=None):
#     """
#     Tìm kiếm sản phẩm và trả về dữ liệu định dạng sẵn
#     Bao gồm ảnh chính của sản phẩm
#     """
#     # Tạo queryset cơ bản với prefetch_related để lấy ảnh chính
#     products = Product.objects.prefetch_related(
#         Prefetch(
#             'images',
#             queryset=ProductImage.objects.filter(is_main=True),
#             to_attr='main_image'
#         )
#     ).select_related('categoryid', 'categoryid__main_category')
    
#     # Áp dụng tìm kiếm nếu có search_query
#     if search_query:
#         query = (
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query) |
#             Q(categoryid__name__icontains=search_query) |
#             Q(categoryid__description__icontains=search_query) |
#             Q(categoryid__main_category__name__icontains=search_query)
#         )
#         products = products.filter(query)
    
#     # Sắp xếp theo số lượng bán được (sold) giảm dần
#     products = products.order_by(Coalesce('sold', 0).desc())
    
#     # Định dạng dữ liệu trả về
#     result = []
#     for product in products:
#         # Lấy ảnh chính (nếu có)
#         main_image = product.main_image[0] if product.main_image else None
#         image_url = main_image.image_url if main_image else None
        
#         # Thêm thông tin category nếu cần
#         category_info = {
#             'category_id': product.categoryid.categoryid if product.categoryid else None,
#             'category_name': product.categoryid.name if product.categoryid else None,
#             'main_category_id': product.categoryid.main_category.id if product.categoryid and product.categoryid.main_category else None,
#             'main_category_name': product.categoryid.main_category.name if product.categoryid and product.categoryid.main_category else None,
#         }
        
#         result.append({
#             'productid': product.productid,
#             'name': product.name,
#             'price': float(product.price),  # Chuyển Decimal sang float để json serialize
#             'description': product.description,
#             'stock': product.stock,
#             'status': product.status,
#             'sold': product.sold or 0,
#             'average_rating': product.average_rating,
#             'total_reviews': product.total_reviews,
#             'image_url': image_url,
#             'category_info': category_info,
#         })
    
#     return result
from django.db.models import Q, F, Case, When, Value, FloatField
from django.db.models.functions import Coalesce

def search_and_format_products(
    search_query=None, 
    orderby=None,
    min_price=None, 
    max_price=None,
    categoryid=None
):
    """
    Tìm kiếm và lọc sản phẩm với đầy đủ tính năng:
    - Tìm kiếm theo tên/mô tả/danh mục
    - Sắp xếp theo rating/giá/sold
    - Lọc theo khoảng giá
    
    Tham số:
    - search_query: Chuỗi tìm kiếm (optional)
    - orderby: 'rating', 'price', 'price-desc' (optional)
    - min_price: Giá tối thiểu (optional)
    - max_price: Giá tối đa (optional)
    """
    # Tạo queryset cơ bản
    products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=ProductImage.objects.filter(is_main=True),
            to_attr='main_image'
        )
    ).select_related('categoryid', 'categoryid__main_category')
    # Áp dụng tìm kiếm nếu có search_query
    if search_query:
        print("vao luon")
        query = (
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(categoryid__name__icontains=search_query) |
            Q(categoryid__description__icontains=search_query) |
            Q(categoryid__main_category__name__icontains=search_query)
        )
        products = products.filter(query)
    # Lọc theo khoảng giá
    if categoryid is not None:
        products = products.filter(categoryid=categoryid)
    if min_price is not None:
        products = products.filter(price__gte=float(min_price))
    if max_price is not None:
        products = products.filter(price__lte=float(max_price))
    
    # Sắp xếp
    if orderby == 'rating':
        products = products.order_by(
            Coalesce('average_rating', 0).desc(), 
            Coalesce('total_reviews', 0).desc()
        )
    elif orderby == 'price':
        products = products.order_by('price')
        
    elif orderby == 'price-desc':
        products = products.order_by('-price')
    else:  # Mặc định sắp xếp theo sold
        products = products.order_by(Coalesce('sold', 0).desc())
    
    # Định dạng kết quả
    result = []
    for product in products:
        main_image = product.main_image[0] if product.main_image else None
        result.append({
            'productid': product.productid,
            'name': product.name,
            'price': float(product.price),
            'description': product.description,
            'stock': product.stock,
            'status': product.status,
            'sold': product.sold or 0,
            'average_rating': product.average_rating,
            'total_reviews': product.total_reviews,
            'image_url': main_image.image_url if main_image else None,
            'category_info': {
                'category_id': product.categoryid.categoryid if product.categoryid else None,
                'category_name': product.categoryid.name if product.categoryid else None,
                'main_category_id': product.categoryid.main_category.id if product.categoryid and product.categoryid.main_category else None,
                'main_category_name': product.categoryid.main_category.name if product.categoryid and product.categoryid.main_category else None,
            }
        })
    return result

def get_price_range():
    """
    Lấy giá cao nhất và thấp nhất từ tất cả sản phẩm
    Trả về: {'min_price': giá thấp nhất, 'max_price': giá cao nhất}
    """
    price_range = Product.objects.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    return {
        'min_price': float(price_range['min_price']) if price_range['min_price'] else 0,
        'max_price': float(price_range['max_price']) if price_range['max_price'] else 0
    }