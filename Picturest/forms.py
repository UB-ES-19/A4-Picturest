from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import *

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


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email address', required=True)
    age = forms.IntegerField(label='Age', required=False)
    username = forms.CharField(label='Username', required=False)
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)
    about = forms.CharField(label='About your profile', required=False)
    location = forms.CharField(label='Location', required=False)
    photo = forms.ImageField(label='Photo', required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'age',
            'username',
            'first_name',
            'last_name',
            'about',
            'location',
            'photo',
        ]


class PinForm(forms.ModelForm):
    post = forms.ImageField(label='Post', required=True)
    title = forms.CharField(label="Title", max_length=50, required=True)
    description = forms.CharField(label="Description", required=False)
    board = forms.ModelChoiceField(label="Board", queryset=Board.objects.all(),
                                   empty_label=None)

    class Meta:
        model = Pin
        fields = ["post", "title", "description", "board"]
        # fields = ["post", "title", "description", "board", "section"]

    def __init__(self, *args, **kwargs):
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['post'].required = False
        #self.fields['author'].required = False
        #self.fields['board'].required = False
        #self.fields['section'].required = False


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name"]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "board"]


class SearchFriendForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ["friend", "creator"]
