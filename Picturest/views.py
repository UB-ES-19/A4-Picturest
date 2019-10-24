# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .models import *
import random


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

    if request.method == "POST":
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.author = request.user
            new_pin.post = form.cleaned_data['post']
            new_pin.save()
            return HttpResponseRedirect(reverse("profile"))

        else:
            print(form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = PinForm(instance=request.user)

        pins = Pin.objects.all()
        #boards = Board.objects.all()
        #sections = Section.objects.all()
        #users = User.objects.all()

        context = {
            'pins': pins,
            'authenticated': request.user.is_authenticated,
            'username': request.user.email,
            'form': form
        }
        return render(request, 'Picturest/home_page.html', context)


@login_required
def profile(request, user_search):
    user_aux = ""
    dis = True

    if 'user_search' in request.GET:
        user_search = request.GET["user_search"]

    if user_search:
        try:
            if "@" in user_search:
                user_aux = PicturestUser.objects.get(email=user_search)
            else:
                user_aux = PicturestUser.objects.get(username=user_search)
        except PicturestUser.DoesNotExist:
            return HttpResponseRedirect(reverse("friend_not_found"))

    if request.method == "GET" and not user_aux:
        user_aux = request.user
        interests = InterestsSimple.objects.filter(user=request.user)

        if interests:

            temp = interests[0]
            interests_list = temp.interests_list
            interest_values = {}
            for elem in interests_list:
                interest_value = getattr(temp, elem)
                interest_values[elem] = interest_value
            print(interests_list)
            print(interest_values)

            form_interests = InterestsSimpleForm(instance=interests[0])
        else:
            form_interests = InterestsSimpleForm()

    elif request.method == "POST":
        form = SearchFriendForm()
        if form.is_valid():
            freq = form.save(commit=False)
            freq.friend = user_aux
            freq.creator = request.user
            freq.save()
            request.session["result"] = "OK"

        interests = InterestsSimple.objects.filter(user=request.user)
        if interests:
            form_interests = InterestsSimpleForm(
                request.POST or None, instance=interests[0])
        else:
            form_interests = InterestsSimpleForm(request.POST or None)

        if form_interests.is_valid():
            interests = form_interests.save(commit=False)
            interests.user = request.user
            interests.save()

            return HttpResponseRedirect(reverse("profile"))

        else:
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('profile'))

    user_boards = Board.objects.filter(author=user_aux)
    user_sections = Section.objects.filter(author=user_aux)
    user_pins = Pin.objects.filter(author=user_aux)
    following = Friendship.objects.filter(
        creator=user_aux, accepted=True).count()
    followers = Friendship.objects.filter(
        friend=user_aux, accepted=True).count()

    if user_aux != request.user:
        try:
            Friendship.objects.get(friend=user_aux, creator=request.user)
            dis = True
        except Friendship.DoesNotExist:
            dis = False

    context = {
        'authenticated': request.user.is_authenticated,
        'user': user_aux,
        'user_boards': user_boards,
        'user_sections': user_sections,
        'user_pins': user_pins,
        'you': user_aux == request.user,
        'followers': followers,
        'followings': following,
        'disabled': dis,
        'form_interests': form_interests,
        'interests_list': interests_list,
        'interest_values': interest_values
    }

    return render(request, 'Picturest/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))

        else:
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
def following(request):
    form = PinForm(instance=request.user)
    email_followers = []
    friendships = Friendship.objects.filter(creator=request.user)

    for friendship in friendships:
        email_followers.append(friendship.friend)

    #pins = Pin.objects.filter(author__in=email_followers)
    pins = sorted(Pin.objects.filter(author__in=email_followers),
                  key=lambda x: random.random())

    context = {
        'pins': pins,
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'form': form
    }
    return render(request, 'Picturest/home_page.html', context)


@login_required
def pin(request, pin_search=""):
    if request.method == "POST":
        form = PinForm(request.POST)
        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.author = request.user
            new_pin.save()

            return HttpResponseRedirect(reverse("home_page"))

        else:
            print(form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    elif pin_search:
        try:
            result = Pin.objects.get(pin_id=pin_search)
            context = {
                'pin': result
            }
            return render(request, 'Picturest/picture_view.html', context)

        except Pin.DoesNotExist or Pin.MultipleObjectsReturned:
            return HttpResponseRedirect(reverse("friend_not_found"))

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
            new_board = form.save(commit=False)
            new_board.author = request.user
            new_board.save()

            return HttpResponseRedirect(reverse("home_page"))

        else:
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


@login_required
def search_friends(request):
    if request.method == "POST":
        if "friend" in request.POST.keys():
            friend_name = request.POST["friend"]
            if friend_name:
                try:
                    form = SearchFriendForm()
                    freq = form.save(commit=False)
                    freq.friend = User.objects.get(username=friend_name)
                    freq.creator = request.user
                    freq.save()
                    request.session["result"] = "OK"
                except User.DoesNotExist:
                    request.session["result"] = "KO"

        elif "accept" in request.POST.keys():
            friend_id = request.POST["accept"]
            Friendship.objects.filter(
                id_friend=friend_id).update(accepted=True)

        elif "refuse" in request.POST.keys():
            friend_id = request.POST["refuse"]
            Friendship.objects.filter(id_friend=friend_id).delete()

        return HttpResponseRedirect(reverse("search_friends"))

    elif request.method == "GET":
        accepted = Friendship.objects.filter(
            creator=request.user, accepted=True)
        accepted_yours = Friendship.objects.filter(
            friend=request.user, accepted=True)
        pending = Friendship.objects.filter(
            creator=request.user, accepted=False)
        pending_yours = Friendship.objects.filter(
            friend=request.user, accepted=False)

        context = {
            "accepted": accepted,
            "accepted_yours": accepted_yours,
            "pending": pending,
            "pending_yours": pending_yours,
        }
        return render(request, 'Picturest/search_friends.html', context)


def friend_not_found(request):
    return render(request, 'Picturest/user_not_found.html', {})


def search(request):
    word = request.GET["word_search"]
    you = request.user.username
    users_username = PicturestUser.objects.filter(username__contains=word).\
        exclude(username=you)
    pins = Pin.objects.filter(title__contains=word)

    context = {
        "users_username": users_username,
        "pins": pins
    }

    return render(request, 'Picturest/search.html', context)


def interests(request):
    if request.method == "POST":
        # form = InterestsForm(request.POST or None)
        interests = InterestsSimple.objects.filter(user=request.user)
        if interests:
            form = InterestsSimpleForm(
                request.POST or None, instance=interests[0])
        else:
            form = InterestsSimpleForm(request.POST or None)

        if form.is_valid():
            interests = form.save(commit=False)
            interests.user = request.user
            interests.save()

            return HttpResponseRedirect(reverse("profile"))

        else:
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('profile'))

    else:
        interests = InterestsSimple.objects.filter(user=request.user)

        # form = InterestsForm(instance=request.user)
        if interests:
            form_simple = InterestsSimpleForm(instance=interests[0])
        else:
            form_simple = InterestsSimpleForm()

        print(form_simple)
        context = {
            # 'form': form,
            'form_simple': form_simple,
            'authenticated': request.user.is_authenticated
        }

    return render(request, 'Picturest/interests.html', context)
