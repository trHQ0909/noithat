from django.urls import path
from django.urls import re_path
from admin_web.views import main_view,update_product_view,create_product_view,delete_product_view,get_product_detail_view

urlpatterns = [
    path("manageProduct/", main_view, name="product-list"),
    path("manageProduct/<int:category_id>/", main_view, name="product-list-by-category"),  # Có category_id
    path("addProduct/", create_product_view, name="create_product"),
    path("delete-product/<int:product_id>/", delete_product_view, name="delete_product"),
    path("update-product/<int:product_id>/", get_product_detail_view, name="update_product"),
    path("update/<int:product_id>/", update_product_view, name="update"),
    # re_path(r"^category/(?P<category_id>\d+)?/?$", main_view, name="products_by_category"),
]
