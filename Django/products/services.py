from products.models import Category, CategoryMain, Product, ProductImage
from order.models import Cart
from customers.models import Customer
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

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
    """Lấy thông tin sản phẩm và tất cả ảnh của sản phẩm đó"""
    product = get_product_by_id(product_id)
    if product:
        images = list(ProductImage.objects.filter(productid=product).values('image_url', 'is_main'))
        product_detail = {
            "product_id": product.productid,
            "name": product.name,
            "category_id": product.categoryid.categoryid if product.categoryid else None,
            "category_name": product.categoryid.name if product.categoryid else None,
            "price": product.price,
            "description": product.description,
            "sold": product.sold,
            "stock": product.stock,
            "status": product.status,
            "images": images
        }
        return product_detail
    return None
#-----------CART
