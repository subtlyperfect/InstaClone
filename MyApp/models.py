# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models  # Import models from Django database.
import uuid  # Import uuid to generate unique IDs.


# Model to fetch the details from a new user and get them entered into database.

class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)


# Model to save the session related details in the database.

class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    def create_token(self):
        self.session_token = uuid.uuid4()


# Model to save the post related details in the database.

class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked = False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')

    @property
    def categories(self):
        return CategoryModel.objects.filter(post=self)


# Model to store details of a like.

class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Model to store details related to a comment.

class CommentModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# Model to sort tags using Clarifai.

class CategoryModel(models.Model):
    post = models.ForeignKey(PostModel)
    category_text = models.CharField(max_length=200)