from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/', views.product, name="product"),
    path('userlogin/', views.login, name="userlogin"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('forgot/', views.forgot, name="forgot"),
    
    
]
