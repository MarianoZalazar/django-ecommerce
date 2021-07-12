from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_managment/forgot.html',
            email_template_name='password_managment/password_reset_email.html',
            success_url=reverse_lazy('user:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_managment/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_managment/reset.html',
             success_url=reverse_lazy('user:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_managment/password_reset_complete.html'),
         name='password_reset_complete'),
    path('logout/', views.log_out, name="log_out")
]