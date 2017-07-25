# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from models import PostModel, UserModel, LikeModel, CommentModel
from django.contrib import admin

# Register your models here.
admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)
admin.site.register(UserModel)



