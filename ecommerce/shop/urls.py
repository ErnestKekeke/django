from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('product/<int:id>/', views.product_detail, name="product"),
    path('add-cart/<int:id>/', views.add_cart, name="add-cart"),
    path('cart/', views.cart, name="cart"),

    path('add-item/<int:id>/', views.add_item, name="add-item"),
    path('remove-item/<int:id>/', views.remove_item, name="remove-item"),

    path('checkout/', views.checkout, name="checkout"),

    path('register/', views.register_view, name="register"),
    path('register-user/', views.register_user, name="register-user"),

    path('login/', views.login_view, name="login"), # login is inbuilt function
    path('login-user/', views.login_user, name="login-user"),

    path('logout-user/', views.logout_user, name="logout-user"),

]