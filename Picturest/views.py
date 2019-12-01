# Create your views here.
import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .models import *


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

        form_board = BoardForm()
        board_default = form_board.save(commit=False)
        board_default.name = "Default"
        board_default.author = request.user
        board_default.save()

        form_interests = InterestsSimpleForm()
        interests = form_interests.save(commit=False)
        interests.user = request.user
        interests.save()

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
        new_board = None

        form = PinForm(request.POST, request.FILES)
        if 'board' in form.errors:
            form_board = BoardForm()
            new_board = form_board.save(commit=False)
            new_board.author = request.user
            new_board.name = request.POST['board_name']
            new_board.save()
            form.errors.pop('board')

        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.author = request.user
            new_pin.post = form.cleaned_data['post']

            if new_board:
                new_pin.board = new_board

            new_pin.save()
            return HttpResponseRedirect(reverse('pin', args=(new_pin.pin_id,)))

        else:
            print(form.errors)
            request.session["result"] = form.errors
        return HttpResponseRedirect(reverse('home_page'))

    else:
        form = PinForm(instance=request.user)
        user_interests = get_user_interests(request.user)
        interests_list = get_interests_list(user_interests)
        interests_list_hastag = add_hastag_to_interests(interests_list)
        pins = get_pins_from_interests(interests_list_hastag)
        boards_user = Board.objects.filter(author=request.user)

        context = {
            'pins': pins,
            'authenticated': request.user.is_authenticated,
            'username': request.user.email,
            'form': form,
            'boards_user': boards_user
        }
        return render(request, 'Picturest/home_page.html', context)


@login_required
def profile(request, user_search):
    user_aux = ""
    dis = True
    interests_list = []
    interest_values = []

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

    elif request.method == "POST":
        form = SearchFriendForm()
        if form.is_valid():
            freq = form.save(commit=False)
            freq.friend = user_aux
            freq.creator = request.user
            freq.save()
            request.session["result"] = "OK"

        form_request = NotificationAcceptedForm()
        freq_request = form_request.save(commit=False)
        freq_request.user = user_aux
        freq_request.type = "NewFollower"
        freq_request.friendship = request.user
        freq_request.save()

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

    interests = InterestsSimple.objects.filter(user=user_aux)

    if interests:
        temp = interests[0]
        interests_list = temp.interests_list
        interest_values = {}
        for elem in interests_list:
            interest_value = getattr(temp, elem)
            interest_values[elem] = interest_value

        form_interests = InterestsSimpleForm(instance=interests[0])
    else:
        form_interests = InterestsSimpleForm()

    user_boards = Board.objects.filter(author=user_aux)
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

    # pins = Pin.objects.filter(author__in=email_followers)
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
    if pin_search:
        try:
            result = Pin.objects.get(pin_id=pin_search)
            context = {
                'pin': result
            }
            return render(request, 'Picturest/picture_view.html', context)

        except Pin.DoesNotExist or Pin.MultipleObjectsReturned:
            return HttpResponseRedirect(reverse("friend_not_found"))

    else:
        return HttpResponseRedirect(reverse("home_page"))


@login_required
def board(request, board_search=""):
    result = Board.objects.get(board_id=board_search)

    if request.method == "POST":
        if "pin" in request.POST:
            pin_id = request.POST["pin"]
            Pin.objects.get(pin_id=pin_id).delete()

        else:
            form = PinForm(request.POST, request.FILES)

            if 'board' in form.errors:
                form.errors.pop('board')

            if form.is_valid():
                new_pin = form.save(commit=False)
                new_pin.author = request.user
                new_pin.post = form.cleaned_data['post']
                new_pin.board = result
                new_pin.save()

    if board_search:
        try:
            pins = Pin.objects.filter(board=result)

            context = {
                'board': result,
                'pins': pins
            }
            return render(request, 'Picturest/board_view.html', context)

        except Board.DoesNotExist or Board.MultipleObjectsReturned:
            return HttpResponseRedirect(reverse("friend_not_found"))

    else:
        return HttpResponseRedirect(reverse("home_page"))


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
            Friendship.objects.filter(id_friend=friend_id).update(accepted=True)

            form_accept = NotificationAcceptedForm()
            freq_accept = form_accept.save(commit=False)
            freq_accept.user = Friendship.objects.get(id_friend=friend_id).creator
            freq_accept.type = "FollowAccepted"
            freq_accept.friendship = request.user
            freq_accept.save()

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
    boards = Board.objects.filter(name__contains=word)

    context = {
        "users_username": users_username,
        "pins": pins,
        "boards": boards
    }

    return render(request, 'Picturest/search.html', context)


def notifications(request):
    notis = Notification.objects.filter(user=request.user).order_by('-date_insert')

    context = {
        "notifications": notis
    }

    return render(request, 'Picturest/notifications.html', context)


def get_user_interests(user):
    interest_values = {}
    interests = InterestsSimple.objects.filter(user=user)

    if interests:
        temp = interests[0]
        interests_list = temp.interests_list
        for elem in interests_list:
            interest_value = getattr(temp, elem)
            interest_values[elem] = interest_value

    return interest_values


def get_interests_list(interests):
    interests_list = []
    for interest, value in interests.items():
        if value:
            interests_list.append(interest)
    return interests_list


def add_hastag_to_interests(interests_list):
    interests_hastag = []
    for interest in interests_list:
        temp = "#"+interest
        interests_hastag.append(temp)
    return interests_hastag


def get_pins_from_interests(interests_list):
    # This method will show one Pin as many times as different interests contains.
    # Bad implementation. Pins shouldn't be repeated, but for now it's OK

    pins = []
    for interest in interests_list:
        pins += Pin.objects.filter(description__contains=interest)
    pins = list(dict.fromkeys(pins))

    return pins
