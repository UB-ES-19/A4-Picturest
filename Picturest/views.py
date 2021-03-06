# Create your views here.
import operator

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

        # if next:
        #     # return HttpResponseRedirect(reverse("homepage"))
        #     return redirect("interests")

        return redirect("interests")
        # return redirect('/')

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
            new_board.secret = 'secret' in request.POST
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
        pins = get_pins_from_interests(interests_list_hastag, request.user)
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
def profile(request, user_search="", noti_id=""):
    if noti_id:
        try:
            Notification.objects.filter(
                id=noti_id, user=request.user).update(seen=True)

        except Notification.DoesNotExist:
            pass

        return HttpResponseRedirect(reverse('profile', args=(user_search,)))

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

    if not user_aux:
        user_aux = request.user

    if request.method == "POST":
        if user_search:
            form = SearchFriendForm()
            freq = form.save(commit=False)
            freq.friend = user_aux
            freq.creator = request.user
            freq.save()

            form_request = NotificationAcceptedForm()
            freq_request = form_request.save(commit=False)
            freq_request.user = user_aux
            freq_request.type = "NewFollower"
            freq_request.friendship = request.user
            freq_request.save()

        else:
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
    friendships = Friendship.objects.filter(creator=request.user)
    # email_followers = []
    #
    # for friendship in friendships:
    #     email_followers.append(friendship.friend)
    #
    # pins = sorted(Pin.objects.filter(author__in=email_followers, board__secret=False),
    #               key=lambda x: random.random())

    pins = []
    for friendship in friendships:
        pins += Pin.objects.filter(author=friendship.friend,
                                   board__secret=False)
        for repin in RePin.objects.filter(board__secret=False, board__author=friendship.friend).exclude(pin__author=request.user):
            if repin.pin not in pins:
                pins.append(repin.pin)

    context = {
        'pins': pins,
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'form': form
    }
    return render(request, 'Picturest/home_page.html', context)


@login_required
def pin(request, pin_search="", noti_id=""):
    if noti_id:
        try:
            Notification.objects.filter(
                id=noti_id, user=request.user).update(seen=True)

        except Notification.DoesNotExist:
            pass

        return HttpResponseRedirect(reverse('pin', args=(pin_search,)))

    if pin_search:
        try:
            result = Pin.objects.get(pin_id=pin_search)
            if result.author != request.user and result.board.secret:
                return HttpResponseRedirect(reverse("home_page"))

        except Pin.DoesNotExist or Pin.MultipleObjectsReturned:
            return HttpResponseRedirect(reverse("friend_not_found"))

    else:
        return HttpResponseRedirect(reverse("home_page"))

    if request.method == "POST":
        new_board = None

        form = RePinForm(request.POST)
        if 'board' in form.errors:
            form_board = BoardForm()
            new_board = form_board.save(commit=False)
            new_board.author = request.user
            new_board.name = request.POST['board_name']
            new_board.secret = 'secret' in request.POST
            new_board.save()
            form.errors.pop('board')

        new_repin = form.save(commit=False)
        new_repin.pin = result

        if new_board:
            new_repin.board = new_board

        new_repin.save()

        form_request = NotificationRePinForm()
        freq_request = form_request.save(commit=False)
        freq_request.user = result.author
        freq_request.type = "RePin"
        freq_request.pin = result
        freq_request.friendship = request.user
        freq_request.save()
        return HttpResponseRedirect(reverse('pin', args=(pin_search,)))

    boards = Board.objects.filter(author=request.user)

    context = {
        'pin': result,
        'boards_user': boards
    }
    return render(request, 'Picturest/picture_view.html', context)


@login_required
def board(request, board_search=""):
    try:
        result = Board.objects.get(board_id=board_search)
        yours = result.author == request.user
    except Board.DoesNotExist or Board.MultipleObjectsReturned:
        return HttpResponseRedirect(reverse("friend_not_found"))

    if request.method == "POST":
        if "pin" in request.POST:
            pin_id = request.POST["pin"]
            del_pin = Pin.objects.get(pin_id=pin_id)

            if del_pin.board == result:
                del_pin.delete()

            else:
                RePin.objects.filter(pin=del_pin, board=result).delete()

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

    if board_search and (yours or not result.secret):
        pins = list(Pin.objects.filter(board=result))
        repins = list(RePin.objects.filter(board=result))

        for repin in repins:
            pins.append(repin.pin)

        context = {
            'board': result,
            'pins': pins,
            'yours': yours
        }
        return render(request, 'Picturest/board_view.html', context)

    else:
        return HttpResponseRedirect(reverse("home_page"))


@login_required
def search_friends(request, noti_id=""):
    if noti_id:
        try:
            Notification.objects.filter(id=noti_id, user=request.user).delete()

        except Notification.DoesNotExist:
            pass

        return HttpResponseRedirect(reverse('search_friends'))

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

            form_accept = NotificationAcceptedForm()
            freq_accept = form_accept.save(commit=False)
            freq_accept.user = Friendship.objects.get(
                id_friend=friend_id).creator
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
    users = PicturestUser.objects.filter(
        username__contains=word).exclude(username=you)
    pins = []
    pins += Pin.objects.filter(title__contains=word, board__secret=False)
    pins += Pin.objects.filter(author=request.user, board__secret=True)
    boards = []
    boards += Board.objects.filter(name__contains=word, secret=False)
    boards += Board.objects.filter(author=request.user, secret=True)

    context = {
        "users_username": users,
        "pins": sorted(pins, key=operator.attrgetter('pk')),
        "boards": sorted(boards, key=operator.attrgetter('pk'))
    }

    return render(request, 'Picturest/search.html', context)


def notifications(request):
    notis = Notification.objects.filter(
        user=request.user).order_by('-date_insert')

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


def get_pins_from_interests(interests_list, user):
    # This method will show one Pin as many times as different interests contains.
    # Bad implementation. Pins shouldn't be repeated, but for now it's OK

    pins = []
    for interest in interests_list:
        pins += Pin.objects.filter(description__contains=interest,
                                   board__secret=False).exclude(author=user)
    pins = list(dict.fromkeys(pins))

    return pins


def interests(request):
    interests_list = []
    interest_values = []

    if request.method == "GET":
        interests = InterestsSimple.objects.filter(user=request.user)

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

    elif request.method == "POST":

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

            return redirect("home_page")
            # return HttpResponseRedirect(reverse("homepage"))

        else:
            request.session["result"] = form.errors

        return redirect("home_page")
        # return HttpResponseRedirect(reverse('profile'))

    context = {
        'form_interests': form_interests,
        'interests_list': interests_list,
        'interest_values': interest_values
    }
    return render(request, 'registration/interests.html', context)
