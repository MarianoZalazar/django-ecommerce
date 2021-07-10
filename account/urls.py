from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('forgot/', views.forgot, name="forgot"),
    path('logout/', views.log_out, name="log_out")
    
]