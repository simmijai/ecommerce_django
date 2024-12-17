from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  # Only import authenticate and login once
from .models import UserProfile
from .forms import RegistrationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        # Get data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Create the User object and save it
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create and save the UserProfile with additional data
        profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address
        )

        # Redirect to the login page or any page you want after successful registration
        return redirect('login')

    return render(request, 'ecommerce/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page or a success page
        else:
            messages.error(request, "Invalid username or password")  # Add error message

    return render(request, 'ecommerce/login.html')  # Render the login form



def home(request):
    return render(request, 'ecommerce/home.html')

def add_products(request):
    return render(request, 'ecommerce/add_products.html')


def admin_portal(request):
    return render(request, 'ecommerce/admin_portal.html')

def show_orders(request):
    return render(request, 'ecommerce/show_orders.html')

def admin_profile(request):
    return render(request, 'ecommerce/admin_profile.html')

