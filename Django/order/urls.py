from django.urls import path
from .views import *

urlpatterns = [
    path("addCart/<int:productid>/<int:quantity>/", addCart_view, name="add_Cart"),
    path("buyProduct/<int:productid>/<int:quantity>/", order_product_view, name="buyProduct"),
    path("buyCart/", order_cart_view, name="buyCart"),
    path("Buy/<int:productid>/",orderProduct,name="OrderProduct"),
    path("Buy/",orderCart,name="OrderCart"),
    path("viewCart/",cart_view,name="viewCart")
]   