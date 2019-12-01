# Create your models here.
from __future__ import unicode_literals

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class PicturestUserManager(BaseUserManager):
    def create_user(self, email, age, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not age:
            raise ValueError("Users must introduce an age")
        if not username:
            raise ValueError("Users must introduce an username")

        user = self.model(
            email=self.normalize_email(email),
            age=age,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            age=age,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PicturestUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    age = models.PositiveIntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    about = models.CharField(max_length=500)
    location = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='profile_pics',
                              blank=True, default='profile_pics/default.png')

    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'username']

    objects = PicturestUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


User = PicturestUser


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    name = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    secret = models.BooleanField(default=False)

    def __str__(self):
        return str(self.board_id) + ": " + str(self.name) + " of " \
               + str(self.author.username)


class Pin(models.Model):
    pin_id = models.AutoField(primary_key=True)
    post = models.ImageField(upload_to='posts')
    description = models.TextField()
    title = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pin_id) + ": " + str(self.title) + " of " \
               + str(self.author.username)


class Friendship(models.Model):
    id_friend = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        User, related_name="friendship_creator_set", on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, related_name="friend_set", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.creator.username + " (" + self.creator.email + ") and " + \
            self.friend.username + \
            " (" + self.friend.email + "): " + str(self.accepted)


class Interests(models.Model):
    INTERESTS = [
        "Cinema", "Music", "Sports"
    ]

    CATEGORIES = (
        ("cin", "Cinema"),
        ("mus", "Music"),
        ("spo", "Sports")
    )
    interest = models.TextField(max_length=5, choices=CATEGORIES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # interest_id = models.AutoField(primary_key=True)
    # category = models.CharField(max_length=5, choices=CATEGORIES)
    # is_interested = models.BooleanField(default=False)


class InterestsSimple(models.Model):
    INTERESTS = [
        "cinema", "music", "sports"
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cinema = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    sports = models.BooleanField(default=False)

    interests_list = INTERESTS

    def __str__(self):
        return "Interests of " + str(self.user.username)
