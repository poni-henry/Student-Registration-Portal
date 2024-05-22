"""
URL configuration for student_registration_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    # ... other URL patterns for your application ...
    path('', views.home, name='home'),  # Map root URL ('/') to the 'home' view function
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
