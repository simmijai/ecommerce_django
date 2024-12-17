# ecommerce/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),   # This URL is now accessed at /register/
    path('', views.home, name='home'),                    # Home page URL
    path('add_products/', views.add_products, name='add_products'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('show_orders/', views.show_orders, name='show_orders'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('login/', views.login_view, name='login'),  # You will define login_view later


]

