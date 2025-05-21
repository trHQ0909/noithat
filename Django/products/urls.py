from django.urls import path
from .views import *

urlpatterns = [
    path("categories/", category_list_view, name="category-list"),
    path("category/<int:category_id>/", main_view, name="products_by_category"),  # Lọc sản phẩm theo danh mục
    path("<int:product_id>/", product_detail_view, name="products_by_product_id"),  # Lọc sản phẩm theo danh mục
    path("addRating/<int:product_id>/", addRating, name="addRating"),  # Lọc sản phẩm theo danh mục
    path("search/", searchView, name="search"),
    path("searchCategory/<str:s>/<int:categoryid>/", searchView, name="searchCategory"),

    
]