"""ES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Picturest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.homepage, name='home_page'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/register/$', views.register_view, name='register'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<user_search>.*)/(?P<noti_id>.*)$', views.profile, name='profile'),
    url(r'^profile/(?P<user_search>.*)$', views.profile, name='profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^board/(?P<board_search>.*)$', views.board, name='board'),
    url(r'^pin/(?P<pin_search>.*)/(?P<noti_id>.*)$', views.pin, name='pin'),
    url(r'^pin/(?P<pin_search>.*)$', views.pin, name='pin'),
    url(r'^following/$', views.following, name="following"),
    url(r'^search_friends/(?P<noti_id>.*)$', views.search_friends, name='search_friends'),
    url(r'^search_friends/$', views.search_friends, name='search_friends'),
    url(r'^friend_not_found/$', views.friend_not_found, name='friend_not_found'),
    url(r'^search/$', views.search, name='search'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^interests/$', views.interests, name='interests'),
    url(r'^report/(?P<pin>.*)/(?P<cause>.*)$', views.report, name='report'),
    url(r'^FAQs/$', views.faq_view, name='FAQs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
