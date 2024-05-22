
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Optional, for using default views
from django.urls import path, include  # For including authentication URLs


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Your existing login URL pattern
    path('logout/', views.logout_view, name='logout'),  # Your existing logout URL pattern
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/profile/', views.home, name='home'),
]
