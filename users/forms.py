from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # Custom email validation to prevent duplicate emails
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(label=('Image'), error_messages={'invalid': ("Image files only")}, widget=forms.FileInput, required=False)
   
    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'image', 'github', 'linkedin', 'buy_me_coffee']
        widgets = {
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'buy_me_coffee': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.buymeacoffee.com/username'
            })
        }

    def clean_github(self):
        github = self.cleaned_data.get('github')
        if github and not github.startswith(('http://', 'https://')):
            github = 'https://' + github
        return github

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get('linkedin')
        if linkedin and not linkedin.startswith(('http://', 'https://')):
            linkedin = 'https://' + linkedin
        return linkedin

    def clean_buy_me_coffee(self):
        buy_me_coffee = self.cleaned_data.get('buy_me_coffee')
        if buy_me_coffee and not buy_me_coffee.startswith(('http://', 'https://')):
            buy_me_coffee = 'https://' + buy_me_coffee
        return buy_me_coffee