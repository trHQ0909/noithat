from django.urls import path
from .views import*
urlpatterns = [
    path("MyAccount/",MyAccount, name="MyAccount"),
    path("login/",Login, name="login"),
    path("register/",Register, name="register"),
    path("check_register/",register_view, name="check_register"),
    path("check_login/",login_view, name="check_login"),
    path("Logout/",logout_view, name="Logout"),
    path("updatePassword/",update_password, name="updatePassword"),
]