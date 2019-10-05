from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PicturestUserManager(BaseUserManager):
    def create_user(self, email, age, password= None):
        if not email:
            raise ValueError("Users must have an email address")
        if not age:
            raise ValueError("Users must introduce an age")

        user = self.model(
            email = self.normalize_email(email),
            age = age,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            age = age,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class PicturestUser(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username        = models.CharField(max_length=30)
    age             = models.PositiveIntegerField()

    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age']

    objects = PicturestUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
