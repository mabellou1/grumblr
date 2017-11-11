"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from grumblr import views


urlpatterns = [
	url(r'^$', views.home),
	url(r'^add-item', views.add_item),
	url(r'^login$', auth_views.login, {'template_name' : 'grumblr/login.html'}, name = 'login'),
	url(r'^logout$', auth_views.logout_then_login),
	url(r'^register$', views.register),
    url(r'^global$', views.home, name="home"),
    url(r'^profile/(?P<user_id>\d+)$', views.profile, name = 'profile'),
    url(r'^edit-profile', views.edit_profile, name= 'edit'),
    url(r'^follow/(?P<user_id>\d+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<user_id>\d+)$', views.unfollow, name='unfollow'),
    url(r'^followingpage', views.followinghome, name='followingpage'),
    url(r'^change_password/(?P<username>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
            views.change_password, name='changepassword'),
    url(r'^comfirmation/(?P<username>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
            views.confirm, name='confirm'),
    url(r'^confirmation-email', views.send_confirm_email, name="resendemail"),
    url(r'^email_sent', views.send_change_email, name="sendemail"),
    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    url(r'^add-comment/(?P<item_id>\d+)$', views.add_comment, name="addcomment"),
    url(r'^get-comment/(?P<item_id>\d+)$', views.get_comment),
    url(r'^get-following', views.get_following),
    url(r'^get-profile/(?P<user_id>\d+)$', views.get_profile),
]
