# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_sessiontoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=555)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user_images')),
                ('image_url', models.CharField(max_length=255)),
                ('caption', models.CharField(max_length=240)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.UserModel')),
            ],
        ),
        migrations.AddField(
            model_name='likemodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.PostModel'),
        ),
        migrations.AddField(
            model_name='likemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.UserModel'),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.PostModel'),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.UserModel'),
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.PostModel'),
        ),
    ]
