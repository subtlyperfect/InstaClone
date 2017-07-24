from django import forms
from models import UserModel, SessionToken, PostModel, CommentModel, LikeModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["email", "name", "username", "password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']


class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']
