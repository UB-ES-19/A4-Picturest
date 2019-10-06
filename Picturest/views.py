# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.conf import settings
from .models import *
from .forms import *


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form
    }
    return render(request, "registration/login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form
    }
    return render(request, "registration/register.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def homepage(request):

    pins = Pin.objects.all()
    boards = Board.objects.all()
    sections = Section.objects.all()
    users = User.objects.all()

    print("Pins: ", list(pins))
    print("Boards: ", list(boards))
    for board in list(boards):
        print(board.name)
        print(board.author)
    print("Sections", list(sections))
    print("Users", list(users))

    context = {
        'pins': pins,
        'authenticated': request.user.is_authenticated,
        'username': request.user.email
    }
    return render(request, 'Picturest/home_page.html', context)


def profile(request):

    # user_age = Age.objects.filter(user = request.user)
    # print ("USER_AGE: ",user_age)

    user_boards = Board.objects.filter(author=request.user)
    user_sections = Section.objects.filter(author=request.user)
    user_pins = Pin.objects.filter(author=request.user)

    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'user': request.user,
        'user_boards': user_boards,
        'user_sections': user_sections,
        'user_pins': user_pins

    }
    return render(request, 'Picturest/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, instance=request.user)  # request.FILES
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))

        else:
            print("BAD EDIT PROFILE")
            print(form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('profile'))

    else:
        form = EditProfileForm(instance=request.user)
        context = {
            'form': form
        }

    return render(request, "Picturest/edit_profile.html", context)


@login_required
def pin(request):
    if request.method == "POST":
        form = PinForm(request.POST)
        print(form)
        if form.is_valid():

            new_pin = form.save(commit=False)
            new_pin.author = request.user
            new_pin.save()

            return HttpResponseRedirect(reverse("home_page"))

        else:
            print("BAD PIN CREATION")
            print(form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = PinForm()
        context = {
            'form': form,
            'authenticated': request.user.is_authenticated,
            'username': request.user.email
        }

    return render(request, 'Picturest/pin.html', context)


@login_required
def board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']

            new_board = form.save(commit=False)
            new_board.author = request.user
            new_board.save()

            return HttpResponseRedirect(reverse("home_page"))

        else:
            print("BAD BOARD CREATION")
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = BoardForm()
        context = {
            'form': form,
            'authenticated': request.user.is_authenticated,
            'username': request.user.email
        }

    return render(request, 'Picturest/board.html', context)


@login_required
def section(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        print(form)
        if form.is_valid():

            new_section = form.save(commit=False)
            new_section.author = request.user
            new_section.save()
            return HttpResponseRedirect(reverse("home_page"))

        else:
            print("BAD SECTION CREATION")
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = SectionForm()
        context = {
            'form': form,
            'authenticated': request.user.is_authenticated,
            'username': request.user.email
        }

    return render(request, 'Picturest/section.html', context)
