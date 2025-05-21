from django.urls import path
from django.urls import re_path
from admin_web.views import *

urlpatterns = [
    path("manageProduct/", main_view, name="product-list"),
    path("manageProduct/<int:category_id>/", main_view, name="product-list-by-category"),  # Có category_id
    path("addProduct/", create_product_view, name="create_product"),
    path("delete-product/<int:product_id>/", delete_product_view, name="delete_product"),
    path("update-product/<int:product_id>/", get_product_detail_view, name="update_product"),
    path("update/<int:product_id>/", update_product_view, name="update"),
    path("aboutus/", aboutus, name="aboutus"),
    path("contactus/", contactUs, name="contactus"),
    path("FAQ/", FAQ, name="FAQ"),
    path("sh_r/", Ship_return, name="ship_return"),
    # re_path(r"^category/(?P<category_id>\d+)?/?$", main_view, name="products_by_category"),
]
