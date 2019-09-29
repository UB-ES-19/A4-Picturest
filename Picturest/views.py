# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import * 
from .forms import *


@login_required
def homepage(request):

    pins = Pin.objects.all()
    boards = Board.objects.all()
    sections = Section.objects.all()
    users = User.objects.all()

    print ("Pins: ",list(pins))
    print ("Boards: ", list(boards))
    for board in list(boards):
        print(board.name)
        print(board.author)
    print ("Sections", list(sections))
    print ("Users", list(users))



    context = {
        'pins': pins,
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'Picturest/home_page.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()


            return HttpResponseRedirect(reverse("home_page"))

        else:
            print("BAD PIN CREATION")
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = UserCreationForm()
        
        context = {
            'form': form
            }

    return render(request, "registration/register.html", context)



def profile(request):

    #user_age = Age.objects.filter(user = request.user)
    #print ("USER_AGE: ",user_age)

    user_boards = Board.objects.filter(author = request.user)
    user_sections = Section.objects.filter(author = request.user)
    user_pins = Pin.objects.filter(author = request.user)
    
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'user': request.user,
        'user_boards': user_boards,
        'user_sections': user_sections,
        'user_pins': user_pins

    }
    return render(request, 'Picturest/profile.html', context)



@login_required
def pin(request):
    if request.method == "POST":
        form = PinForm(request.POST)
        print (form)
        if form.is_valid():
            
            new_pin = form.save(commit=False)
            new_pin.author = request.user
            new_pin.save()

            return HttpResponseRedirect(reverse("home_page"))

        else:
            print("BAD PIN CREATION")
            print (form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = PinForm()
        context = {
            'form': form,
            'authenticated': request.user.is_authenticated,
            'username': request.user.username
        }

    return render(request, 'Picturest/pin.html', context)

@login_required
def board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data['name']

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
            'username': request.user.username
        }

    return render(request, 'Picturest/board.html', context)


@login_required
def section(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        print (form)
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
            'username': request.user.username
        }

    return render(request, 'Picturest/section.html', context)

