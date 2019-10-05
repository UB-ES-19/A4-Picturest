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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf import settings

from Picturest import views

# El registre agafa el CustomUser, no el nou PicturestUser!

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.homepage, name='home_page'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/register/$', views.register_view, name='register'),
    url(r'^profile/$', views.profile, name='register'),
    url(r'^board/$', views.board, name='board'),
    url(r'^section/$', views.section, name='section'),
    url(r'^pin/$', views.pin, name='pin'),


]
