# Create your views here.

from django.urls import reverse

from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


def homepage(request):
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'home_page.html', context)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("home_page"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })