from django import forms
from django.contrib.auth.models import User
from .models import Category,Product,UserProfile,Address


from .models import SubCategory, Category

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmpassword = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User  # Link the form to the built-in User model
        fields = ['username', 'email']  # Only username and email for registration

    def clean_confirmpassword(self):
        # Validate that password and confirm password match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirmpassword")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        # Create the User object and set the password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the User object to the database
        return user
           
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category','subcategory','image']
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [ 'city', 'state', 'zip_code', 'country']
        
        



