from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import category_list_view,main_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_view, name="product-home"),
    path("products/", include("products.urls")),  # Đảm bảo include đúng
    path("admin_web/", include("admin_web.urls")),
    path("accounts/", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("order/", include("order.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])