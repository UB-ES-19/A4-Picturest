# Create your models here.
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    name = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    name = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Pin(models.Model):
    pin_id = models.AutoField(primary_key=True)
    post = models.ImageField(upload_to='static/user_images')
    description = models.TextField()
    title = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class FriendList(models.Model):
    friend_list_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_friend_list')
    friend = models.ManyToManyField(User, related_name='user_friends')


class RequestList(models.Model):
    request_list_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_request_list')
    request = models.ManyToManyField(User, related_name='user_friend_requests')


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_author')
    message = models.TextField()
    receptor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_receptor')
