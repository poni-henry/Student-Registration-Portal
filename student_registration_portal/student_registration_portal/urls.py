from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('enroll/', views.enroll, name='enroll'),
    path('confirm-enrollment/', views.confirm_enrollment, name='confirm_enrollment'),
    path('register/', views.register_page, name='register_page'),
    path('', views.login_view, name='login'),  # Default route to login view
]
