from django.urls import path
from .views import category_list_view, product_list_view, products_by_category_view,main_view,product_detail_view

urlpatterns = [
    path("categories/", category_list_view, name="category-list"),
    path("category/<int:category_id>/", main_view, name="products_by_category"),  # Lọc sản phẩm theo danh mục
    path("<int:product_id>/", product_detail_view, name="products_by_product_id"),  # Lọc sản phẩm theo danh mục
    
]