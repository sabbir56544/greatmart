from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
          
        }