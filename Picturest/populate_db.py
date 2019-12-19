from Picturest.models import *
import django
import os
import random
import csv
from inspect import getsourcefile
from os.path import abspath
from random import randrange

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
        "pin_8": {"post": "populate_script/wind-farm.jpg", "title": "Wind farm", "description": "Aren't they beautiful? #tecnology", "pin_id": "Default"},
        "pin_9": {"post": "populate_script/autumn.jpg", "title": "Autumm", "description": "Is that time of the year #photography", "pin_id": "Default"},
        "pin_10": {"post": "populate_script/cooperative.jpg", "title": "Cooperative", "description": " Maybe if we all collaborate to make a better world ... #photography", "pin_id": "Default"},
        "pin_11": {"post": "populate_script/cow.jpg", "title": "Cow", "description": "Trip to Scotland #animals", "pin_id": "Default"},
        "pin_12": {"post": "populate_script/landscape.jpg", "title": "Landscape", "description": "Good place to be #photography", "pin_id": "Default"},
        "pin_13": {"post": "populate_script/muffin.jpg", "title": "Mufifn", "description": "Mmmmmh #food", "pin_id": "Default"},
        "pin_14": {"post": "populate_script/rural.jpg", "title": "Rural", "description": "Hometown pleasure #photography", "pin_id": "Default"},
        "pin_15": {"post": "populate_script/artichokes.jpg", "title": "Arichokes", "description": "About to eat this arichokes. What is your favourite food? Tell me on the coments #food", "pin_id": "Default"},
        "pin_16": {"post": "populate_script/city-street.jpg", "title": "My last vacations", "description": "Japan, best place in the world #travel", "pin_id": "Default"},
        "pin_17": {"post": "populate_script/coffee.jpg", "title": "Coffee", "description": "What do you think about this new peace of art? #paint #food", "pin_id": "Default"},
        "pin_18": {"post": "populate_script/forest.jpg", "title": "Forest near home", "description": "Good place to spend sunday #photography", "pin_id": "Default"},
        "pin_19": {"post": "populate_script/forest2.jpg", "title": "Natural park of Cambrils", "description": "So happy te see new places, best trip ever #animals #travel", "pin_id": "Default"},
        "pin_19": {"post": "populate_script/lake.jpg", "title": "Lake", "description": "I think I'm gonna swim around #travel #photography", "pin_id": "Default"},
        "pin_19": {"post": "populate_script/trees.jpg", "title": "Trees and sky", "description": "Look how tall have they made. Huge profits, invest now #garden", "pin_id": "Default"}
    }

    n = 10
    for i in range(0, n):
        create_random_user()

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
    add_interests_show(user)

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
    add_interests_show(user)

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


def add_interests_show(user):
    print("--- New Interests Show --")
    interests_show = InterestsSimpleShow.objects.create(user=user)
    interests_show.save()
    return interests_show


def create_random_user():
    names = ["James", "Josephine", "Art", "Lenna", "Donette", "Simona", "Mitsue", "Leota", "Sage", "Kris", "Minna", "Abel",
             "Kiley", "Graciela", "Cammy", "Mattie", "Meaghan", "Gladys", "Yuki", "Fletcher", "Bette", "Veronika", "Willard", "Maryann",
             "Alisha", "Allene", "Chanel", "Ezekiel", "Willow", "Bernardo", "Ammie", "Francine", "Ernie", "Albina", "Alishia", "Solange",
             "Jose", "Rozella", "Valentine", "Kati", "Youlanda", "Dyan", "Roxane", "Lavera", "Erick", "Fatima", "Jina", "Kanisha", "Emerson"]

    # 50 lastnames
    lastnames = ["Butt", "Darakjy", "Venere", "Paprocki", "Foller", "Morasca", "Tollner", "Dilliard", "Wieser", "Marrier", "Amigon",
                 "Maclead", "Caldarera", "Ruta", "Albares", "Poquette", "Garufi", "Rim", "Whobrey", "Flosi", "Nicka", "Inouye", "Kolmetz",
                 "Royster", "Slusarski", "Iturbide", "Caudy", "Chui", "Kusko", "Figeroa", "Corrio", "Vocelka", "Stenseth", "Glick", "Sergi",
                 "Shinko", "Stockham", "Ostrosky", "Gillian", "Rulapaugh", "Schemmer", "Oldroyd", "Campain", "Perin", "Ferencz", "Saylors",
                 "Briddick", "Waycott", "Bowley"]

    name = random.choice(names)
    lastname = random.choice(lastnames)
    age = randrange(18, 50)
    seed = randrange(0, 99)

    email = name+lastname+str(age)+str(seed)+"@hotmail.com"
    username = name+str(age)+str(seed)
    password = "default"

    user = User.objects.create_user(
        email=email, age=age, username=username, password=password)
    user.save()
    add_board("Default", user)
    add_interests(user)
    add_interests_show(user)


    # Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()
