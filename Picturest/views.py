# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


@login_required
def homepage(request):
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'Picturest/home_page.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("Picturest/home_page"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
