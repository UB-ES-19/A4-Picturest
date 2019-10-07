# Create your models here.
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager

from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import get_user_model


class PicturestUserManager(BaseUserManager):
    def create_user(self, email, age, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not age:
            raise ValueError("Users must introduce an age")

        user = self.model(
            email=self.normalize_email(email),
            age=age,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            age=age,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PicturestUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    about = models.CharField(max_length=500)
    location = models.CharField(max_length=60)
    photo = models.ImageField(default='default.jpg',
                              upload_to='profile_pics', blank=True)

    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age']

    objects = PicturestUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


User = PicturestUser
# = get_user_model()


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
