from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from adminpanel.models import Profile,Property,Report,Rating

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name=forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email=forms.EmailField(
        max_length=30,
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    username=forms.CharField(
        max_length=30,
        required=True,
        label='User Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password1=forms.CharField(
        max_length=30,
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})

    )
    password2=forms.CharField(
        max_length=30,
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )


    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    first_name=forms.CharField(
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    
    last_name=forms.CharField(
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    profile_description=forms.CharField(
        required=True,
        label="Description",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    phone=forms.CharField(
        required=True,
        label="Phone",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    profile_image=forms.ImageField(
        required=True,
        label='Profile Image',
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})    
    )

    class Meta:
        model=Profile
        fields='first_name','last_name','profile_description','phone','profile_image'

class LoginForm(forms.Form):

    username=forms.CharField(
        max_length=30,
        required=True,
        label='User Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password=forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

class PropertyForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property title'})
    )
    description = forms.CharField(
        required=True,
        label="Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter property description', 'rows': 4})
    )
    location = forms.CharField(
        required=True,
        label="Location",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property location'})
    
    )
    google=forms.CharField(
        required=True,
        label='Add Google Maps link',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add your link here'})

    )
    price = forms.DecimalField(
        required=True,
        label="Price",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in USD'})
    )
    property_type = forms.ChoiceField(
        required=True,
        label="Property Type",
        choices=Property.status_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    images = forms.ImageField(
        required=True,
        label="Images",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'google','price', 'property_type', 'images']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'screenshot']  # Add other fields if necessary
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }
class Changepassword(PasswordChangeForm):


    class Meta:
        model = Report
        fields="__all__"

class Ratingform(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['value','comment']
        widgets={
            'value': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }


class Paymentform(forms.Form):
    amount=forms.DecimalField(max_digits=6, decimal_places=2, initial=100.0, widget=forms.HiddenInput)
