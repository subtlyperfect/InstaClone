
# we create urls in django in url.py file
# for this we have to import urls from django.conf.url
from django.conf.urls import url

#admin panel is created which has a major control overdatabase
from django.contrib import admin
#from views we import pages which we are giving url to
from MyApp.views import sign_up_view, login_view, post_view, feed_view, like_view, comment_view,logout_view, posts_of_particular_user

# there are the pattenrs which we use to create url for a particular page
# r is the regular expression

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^login/feed/(?P<user_name>.+)/$', posts_of_particular_user),
    url('logout/',logout_view,name='logout'),
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url('login/', login_view),
    url('', sign_up_view),

]
