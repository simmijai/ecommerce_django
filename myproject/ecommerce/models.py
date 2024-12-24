from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=False, default='1234567890')  # Example default value
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.email
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')  # Keep 'subcategories' for parent_category

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories_in_category', on_delete=models.CASCADE)  # Change related_name to 'subcategories_in_category'

    def __str__(self):
        return self.name

    
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Image field
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the cart item
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product added to the cart
    quantity = models.PositiveIntegerField(default=1)  # The quantity of this product in the cart

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.user.username}"
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
