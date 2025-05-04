from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("<int:customerid>/", InfomationCustomer, name="inputInfo"),
    path("registerCustomer/<int:customerid>/", registerCustomer, name="registerCustomer"),
    path("customer", customer, name="customer"),
    path("updateCustomer", updateCustomer, name="updateCustomer"),
    path('geteditform/', get_edit_form, name='getEditForm'),
]