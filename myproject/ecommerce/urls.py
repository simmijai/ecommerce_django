# ecommerce/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLogoutView


urlpatterns = [
    path('register/', views.register, name='register'),   # This URL is now accessed at /register/
    path('', views.home, name='home'),                    # Home page URL
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('login/', views.login_view, name='login'),  # You will define login_view later
    
    path('add-category/', views.add_category, name='category_add'),
    path('category-list/', views.category_list, name='category_list'),
    path('edit-category/<int:pk>/', views.edit_category, name='category_edit'),
    path('delete-category/<int:pk>/', views.delete_category, name='category_delete'),  # Delete URL pattern
    
    path('product/list/', views.product_list, name='product_list'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    path('product/add/', views.add_or_edit_product, name='add_product'),
    path('product/edit/<int:product_id>/', views.add_or_edit_product, name='edit_product'),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # path('checkout/', views.checkout, name='checkout'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),  # Use 'profile/' for the user profile URL
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    path('new/', views.new, name='new'),  # Use 'profile/' for the user profile URL
    path('add-address/', views.add_address, name='add_address'),
    path('payment/',views.payment,name='payment'),
    path('subcategory/list/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategory/edit/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategory/delete/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
]
    
    





