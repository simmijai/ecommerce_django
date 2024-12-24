from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  # Only import authenticate and login once
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm,UserProfileForm
from .forms import ProductForm
from django.contrib import messages
from .models import Product  # Add CartItem here
from django.http import JsonResponse
from .models import  CartItem, Product
from .models import CartItem, UserProfile
from django.db import transaction
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LogoutView
from .forms import AddressForm,SubCategoryForm
from .models import Address
from .models import SubCategory, Category

def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'admin/subcategory_list.html', {'subcategories': subcategories})

from .forms import SubCategoryForm

def add_subcategory(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    else:
        form = SubCategoryForm()

    return render(request, 'admin/subcategory_form.html', {'form': form})

def edit_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    else:
        form = SubCategoryForm(instance=subcategory)

    return render(request, 'admin/subcategory_form.html', {'form': form})

def delete_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    subcategory.delete()
    return redirect('subcategory_list')


def user_logout(request):
    # Log the user out
    logout(request)

    # Redirect to the home page after logout
    return redirect('home')

def user_profile(request):
    return render(request, 'admin/user_profile.html')



from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        # Get data from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')  # Ensure you are getting username
        
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'ecommerce/register.html', {'error': 'Passwords do not match'})

        # Check if the email or username already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'ecommerce/register.html', {'error': 'Email already in use'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'ecommerce/register.html', {'error': 'Username already in use'})

        # Create the User object and save it
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create and save the UserProfile with additional data
        profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
        )

        # Redirect to the login page after successful registration
        return redirect('login')

    return render(request, 'ecommerce/register.html')



def login_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        try:
            # Find the user based on the phone number stored in the UserProfile model
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            user = user_profile.user  # Get the associated user object

            # Check if the password is correct
            if user.check_password(password):
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to the home page or any page you want
            else:
                messages.error(request, "Invalid phone number or password")
        except UserProfile.DoesNotExist:
            messages.error(request, "User with that phone number does not exist")

    return render(request, 'ecommerce/login.html')

def admin_portal(request):
    return render(request, 'admin/admin_portal.html')

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the category to the database
            return redirect('category_list')  # Redirect to the category list page
    else:
        form = CategoryForm()

    return render(request, 'admin/category_form.html', {'form': form})

# View to display the list of categories

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)  # Fetch the category by primary key
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  # Pre-fill the form with the category instance
        if form.is_valid():
            form.save()  # Save the updated category
            return redirect('category_list')  # Redirect to category list
    else:
        form = CategoryForm(instance=category)  # Display the pre-filled form
    return render(request, 'admin/category_form.html', {'form': form})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()  # Delete the category
    return redirect('category_list')  # Redirect back to the category list

# Add Product View

def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})


# View to delete a product
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        product.delete()  # Delete the product
        return redirect('product_list')  # Redirect to the product list after deletion
    
    return render(request, 'admin/delete_product.html', {'product': product})


def add_or_edit_product(request, product_id=None):
    if product_id:
        # Edit existing product
        product = get_object_or_404(Product, pk=product_id)
    else:
        # New product
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save product to database
            return redirect('product_list')  # Redirect to product list after saving
    else:
        form = ProductForm(instance=product)  # Pre-fill form for editing or empty form for new product

    return render(request, 'admin/product_form.html', {'form': form})


# def home(request):
#     category_id = request.GET.get('category', None)  # Get category ID from the query parameters
#     if category_id:
#         # Filter products by category ID
#         category = Category.objects.get(id=category_id)
#         products = Product.objects.filter(category=category)
#     else:
#         # Display all products if no category is selected
#         products = Product.objects.all()

#     categories = Category.objects.all()  # Get all categories for the navbar
#     return render(request, 'ecommerce/home.html', {'products': products, 'categories': categories})
def home(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if category_id:
        # If a category is selected, filter products by category
        category = Category.objects.get(id=category_id)
        products = category.products.all()
    elif subcategory_id:
        # If a subcategory is selected, filter products by subcategory
        subcategory = Subcategory.objects.get(id=subcategory_id)
        products = subcategory.products.all()
    else:
        # If no category or subcategory is selected, show all products
        products = Product.objects.all()

    categories = Category.objects.all()
    context = {'categories': categories, 'products': products}
    return render(request, 'ecommerce/home.html', context)


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You need to log in first!"}, status=401)  # 401 Unauthorized

    try:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"message": "Item added to cart!"}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    
@login_required    
def cart(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate the total price for each cart item and also calculate the total cart value
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Add this line to calculate the total price
    
    # Calculate the overall total price
    total_price = sum(item.total_price for item in cart_items)

    # Render the cart page with the cart items and total price
    return render(request, 'admin/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
            new_quantity = int(request.POST['quantity'])
            
            # Update the quantity and recalculate total price
            cart_item.quantity = new_quantity
            cart_item.total_price = cart_item.product.price * new_quantity
            cart_item.save()

            return redirect('cart')  # Redirect back to cart page
        except CartItem.DoesNotExist:
            return HttpResponse("Cart item not found.", status=404)

# Remove item from cart
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()  # Remove the item from the cart
        return redirect('cart')  # Redirect back to cart page
    except CartItem.DoesNotExist:
        return HttpResponse("Cart item not found.", status=404)


# If using Django's built-in LogoutView, you can set the 'next_page' attribute
class CustomLogoutView(LogoutView):
    next_page = '/'



def new(request):
    return render(request,'ecommerce/new.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get the current user and their profile
        user = request.user
        profile = user.userprofile

        # Create a form instance with POST data and the current user's profile instance
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save the form and update the user profile
            form.save()
            # Redirect back to the profile page or any other page after successful update
            return redirect('profile')  # Change 'profile' to the name of your profile page URL
    else:
        # If GET request, render the form with existing user data
        form = UserProfileForm(instance=request.user)

    return render(request, 'admin/edit_profile.html', {'form': form})


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Save the address and link it to the current logged-in user
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            # Return JSON response with address details
            return JsonResponse({
                'message': 'Address added successfully!',
                'address_id': address.id,
                'street_address': address.street_address,
                'city': address.city,
                'state': address.state,
                'zip_code': address.zip_code,
                'country': address.country
            })
        else:
            return JsonResponse({"message": "Error: Form submission failed!"}, status=400)
    else:
        # Get all addresses for the current user to display in the address list
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'admin/address.html', {'addresses': addresses})
    
    
def payment(request):
    return render(request,'admin/payment.html')


