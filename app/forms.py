from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    # Añade cualquier otro campo que necesites

    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'password1', 'password2',)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)