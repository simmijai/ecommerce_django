
from django.contrib import admin
from .models import UserProfile, Category, Product, CartItem, Address

# Register the models
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Address)
