from Picturest.models import *
import django
import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

django.setup()


def populate():

    users = {
        "user_1": {"username": "ico", "age": 23, "email": "quim@gmail.com", "password": "quim"},
        "user_2": {"username": "carol", "age": 23, "email": "carolina@gmail.com", "password": "carolina"},
        "user_3": {"username": "fran", "age": 23, "email": "fran@gmail.com", "password": "fran"},
        "user_4": {"username": "pere", "age": 23, "email": "pere@gmail.com", "password": "pere"},
        "user_5": {"username": "vicent", "age": 23, "email": "vicent@gmail.com", "password": "vicent"},
    }

    pins = {
        "pin_1": {"post": "populate_script/flower.jpg", "title": "Flower", "description": "the description #cinema", "pin_id": "Default"},
        "pin_2": {"post": "populate_script/eye.jpeg", "title": "Dibujo a lapiz", "description": "One year going #music", "pin_id": "Default"},
        "pin_3": {"post": "populate_script/drawing.jpeg", "title": "The rain is here", "description": "Another draw copied from Pinterest #music", "pin_id": "Default"},
        "pin_4": {"post": "populate_script/estanteria.jpeg", "title": "Pinteres.Estanteria", "description": "Snake #sports", "pin_id": "Default"},
        "pin_5": {"post": "populate_script/faces.jpeg", "title": "Intentant-ho", "description": "estan molt be #sports", "pin_id": "Default"},
        "pin_6": {"post": "populate_script/hands.jpeg", "title": "hanDs topo", "description": "Quan la munyeca fa crec #cinema", "pin_id": "Default"},
        "pin_7": {"post": "populate_script/portrait.jpeg", "title": "Camarada Dimitri Petrenko", "description": "One big and great #cinema", "pin_id": "Default"},
    }

    for user, user_data in users.items():
        username = user_data["username"]
        age = user_data["age"]
        email = user_data["email"]
        password = user_data["password"]

        add_user(username, age, email, password)

    add_user_admin("admin", 33, "admin@gmail.com", "admin")

    users = list(User.objects.all())

    for pin, pin_data in pins.items():
        post = pin_data["post"]
        title = pin_data["title"]
        description = pin_data["description"]
        author = random.choice(users)
        user_board_default = Board.objects.filter(
            author=author, name="Default")
        board = user_board_default[0]

        add_pin(post, title, description, author, board)

    user_quim = User.objects.filter(username="ico")
    user_fran = User.objects.filter(username="fran")
    user_pere = User.objects.filter(username="pere")
    user_carol = User.objects.filter(username="carol")
    user_vicent = User.objects.filter(username="vicent")

    add_friendship(user_quim[0], user_fran[0])
    add_friendship(user_quim[0], user_carol[0])

    add_friendship(user_carol[0], user_fran[0])
    add_friendship(user_carol[0], user_vicent[0])

    add_friendship(user_vicent[0], user_quim[0])
    add_friendship(user_vicent[0], user_carol[0])

    add_friendship(user_fran[0], user_quim[0])
    add_friendship(user_fran[0], user_pere[0])

    add_friendship(user_pere[0], user_fran[0])
    add_friendship(user_pere[0], user_vicent[0])


def add_user(username, age, email, password):
    print("--- New User --")
    print("username: ", username)
    print("age: ", age)
    print("email: ", email)
    print("password: ", password)

    user = User.objects.create_user(
        email=email, age=age, username=username, password=password)
    user.save()
    add_board("Default", user)
    add_interests(user)
    
    return user


def add_user_admin(username, age, email, password):
    print("--- New User --")
    print("username: ", username)
    print("age: ", age)
    print("email: ", email)
    print("password: ", password)

    user = User.objects.create_superuser(
        email=email, age=age, username=username, password=password)
    user.save()
    add_board("Default", user)
    add_interests(user)

    return user


def add_pin(post, title, description, author, board):
    print("--- New Pin --")
    print("post: ", post)
    print("title: ", title)
    print("description: ", description)
    print("author: ", author)
    print("board: ", board)

    pin = Pin.objects.create(
        post=post, title=title, description=description, author=author, board=board)
    pin.save()
    return pin


def add_friendship(creator, friend):
    print("--- New Friendship --")
    friendship = Friendship.objects.create(
        creator=creator, friend=friend, accepted=True)
    friendship.save()
    return friendship


def add_board(name, author):
    print("--- New Board --")
    board = Board.objects.create(name=name, author=author)
    board.save()
    return board


def add_interests(user):
    print("--- New Interests --")
    interests = InterestsSimple.objects.create(user=user)
    interests.save()
    return interests


    # Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()
