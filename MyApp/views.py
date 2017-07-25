# -*- coding: utf-8 -*-

# Importing necessary modules and functions.

from __future__ import unicode_literals
from models import UserModel, SessionToken, LikeModel, CommentModel, CategoryModel, PostModel
from datetime import timedelta
from clarifai.rest import ClarifaiApp
from django.utils import timezone
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, LikeForm, CommentForm, PostForm
from django.contrib.auth.hashers import make_password, check_password
from InstaClone.settings import BASE_DIR
from keys import CLARIFAI_API_KEY, CLIENT_SECRET, CLIENT_ID, SENDGRID_API_KEY
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

                ctypes.windll.user32.MessageBoxW(0, u"You have successfully signed up.",
                                                 u"Congratulations!", 0)

                response = redirect('feed/')
                return response
    elif request.method == "GET":
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})


# Controller for user login.

def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:

                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response

                else:
                    ctypes.windll.user32.MessageBoxW(0, u"Invalid Credentials!", u"Error", 0)
                    response_data['message'] = 'Please try again!'
            else:
                ctypes.windll.user32.MessageBoxW(0, u"Invalid Credentials!", u"Error", 0)

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


# Controller for adding a new category.

def add_category(post):
    app = ClarifaiApp(api_key=CLARIFAI_API_KEY)

    # Logo model

    model = app.models.get('general-v1.3')
    response = model.predict_by_url(url=post.image_url)

    if response["status"]["code"] == 10000:
        if response["outputs"]:
            if response["outputs"][0]["data"]:
                if response["outputs"][0]["data"]["concepts"]:
                    for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                        category = CategoryModel(post=post, category_text = response["outputs"][0]["data"]["concepts"][index]["name"])
                        category.save()
                else:
                    print "No concepts list error."
            else:
                print "No data list error."
        else:
            print "No output lists error."
    else:
        print "Response code error."


# Controller for creating a new post.

def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)["link"]
                post.save()

                add_category(post)

                ctypes.windll.user32.MessageBoxW(0, u"Your new post is ready.",
                                                 u"Well done!", 0)

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


# Controller for redirecting the user to news feed once he logs in.

def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')


# Controller for posting a like.

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                like = LikeModel.objects.create(post_id=post_id, user=user)

                ctypes.windll.user32.MessageBoxW(0, u"Keep scrolling for more.",
                                                 u"Liked!", 0)

                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
                from_email = Email("surbhi.sood2@gmail.com")
                to_email = Email(like.post.user.email)
                subject = "Upload to win!"
                content = Content("text/plain", "You have a new like on your post. Keep posting!")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)

            else:
                existing_like.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')


# Controller for posting a comment.

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()

            ctypes.windll.user32.MessageBoxW(0, u"Keep scrolling for more.",
                                             u"Comment added!", 0)

            sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
            from_email = Email("surbhi.sood2@gmail.com")
            to_email = Email(comment.post.user.email)
            subject = "Upload to win!"
            content = Content("text/plain", "You have a new comment on your post. Keep posting!")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)

            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


# For destroying a session

def logout_view(request):
    request.session.modified = True
    response = redirect("/login/")

    ctypes.windll.user32.MessageBoxW(0, u"You've been logged out successfully!",
                                     u"Thank you!", 0)

    response.delete_cookie(key="session_token")
    return response


# For viewing posts by a particular user


def posts_of_particular_user(request,user_name):
    user = check_validation(request)
    if user:
        posts=PostModel.objects.all().filter(user__username=user_name)
        return render(request,'postofuser.html',{'posts':posts,'user_name':user_name})
    else:
        return redirect('/login/')