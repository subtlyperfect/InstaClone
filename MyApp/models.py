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
