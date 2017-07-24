from django import forms
from models import UserModel, SessionToken


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["email", "name", "username", "password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']
