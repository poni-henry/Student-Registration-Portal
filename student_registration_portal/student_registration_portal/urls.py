from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('enroll/', views.enroll, name='enroll'),
    path('confirm-enrollment/', views.confirm_enrollment, name='confirm_enrollment'),
    path('register/', views.register_page, name='register_page'),
    path('register/<str:department>/<str:program>/<int:year_of_study>/<int:semester>/', views.register_page, name='register_page'),
    path('generate-invoice/<str:department>/<str:program>/<int:year_of_study>/<int:semester>/', views.generate_invoice, name='generate_invoice'),
    path('', views.login_view, name='login'),
]
