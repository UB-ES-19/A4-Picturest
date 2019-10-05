from django import forms
import django.contrib.auth.models
from django.contrib.auth import authenticate, get_user_model
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings


User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    age = forms.IntegerField(label='Age')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'age',
            'password'
        ]


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
