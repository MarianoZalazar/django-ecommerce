from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('userlogin/', views.login, name="userlogin"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('forgot/', views.forgot, name="forgot"),
    
]