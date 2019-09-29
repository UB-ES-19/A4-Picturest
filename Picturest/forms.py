from django import forms
import django.contrib.auth.models

from .models import *

from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.forms import UserCreationForm


class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ["post", "title", "description", "board", "section"]

    def __init__(self, *args, **kwargs):
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['post'].required = False
        #self.fields['author'].required = False
        self.fields['board'].required = False
        self.fields['section'].required = False
       

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name"]

       
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "board"]

      


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']


