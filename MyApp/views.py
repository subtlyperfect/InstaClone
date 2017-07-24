# -*- coding: utf-8 -*-

# Importing necessary modules and functions.

from __future__ import unicode_literals
from models import UserModel
from django.http import HttpResponse
from datetime import timedelta
from clarifai.rest import ClarifaiApp
from django.utils import timezone
from django.shortcuts import render, redirect
from forms import SignUpForm
from django.contrib.auth.hashers import make_password, check_password
from InstaClone.settings import BASE_DIR
from imgurpython import ImgurClient
import sendgrid
import ctypes
from sendgrid.helpers.mail import *


# Controller for sign-up.

def sign_up_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data['username']) < 5 or len(form.cleaned_data['password']) < 6 :
                ctypes.windll.user32.MessageBoxW(0, u" Kindly re-enter username and password!", u"INSUFFICIENT CHARACTERS.", 0)

            else:
                username = form.cleaned_data['username']
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Saving data to database.

                user = UserModel(name=name, password=make_password(password), email=email, username=username)
                user.save()

                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
                from_email = Email("surbhi.sood2@gmail.com")
                to_email = Email(form.cleaned_data["email"])
                subject = "Ready to earn!"
                content = Content("text/plain", "Congratulations on your first step towards rewards and prizes!")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)

                response = redirect('feed/')
                return response
    elif request.method == "GET":
        form = SignUpForm()

    return render(request, 'index.html', {'form' : form})