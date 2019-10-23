# Create your views here.
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

        pins = Pin.objects.all()
        boards_user = Board.objects.filter(author=request.user)
        #boards = Board.objects.all()
        #sections = Section.objects.all()
        #users = User.objects.all()

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
    you = False
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
        you = True

    elif request.method == "POST":
        form = SearchFriendForm()
        freq = form.save(commit=False)
        freq.friend = user_aux
        freq.creator = request.user
        freq.save()
        request.session["result"] = "OK"

    user_boards = Board.objects.filter(author=user_aux)
    user_sections = Section.objects.filter(author=user_aux)
    user_pins = Pin.objects.filter(author=user_aux)

    if not you:
        try:
            Friendship.objects.get(friend=user_aux, creator=request.user)
            dis = True
        except Friendship.DoesNotExist:
            dis = False

    context = {
        'authenticated': request.user.is_authenticated,
        'username': user_aux.username,
        'first_name': user_aux.first_name,
        'user': user_aux,
        'user_boards': user_boards,
        'user_sections': user_sections,
        'user_pins': user_pins,
        'you': you,
        'followers': 0,
        'followings': 0,
        'disabled': dis
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
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'Picturest/following_posts.html', context)


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
    if request.method == "POST":
        pin_id = request.POST["pin"]
        Pin.objects.get(pin_id=pin_id).delete()

    if board_search:
        try:
            result = Board.objects.get(board_id=board_search)
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
