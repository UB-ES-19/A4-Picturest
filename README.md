# A4-Picturest
Picturest project's repository

## How to run for the first time
Clone the last version of the project on your computer (current: `quim/pins_from_following`)  
Make sure this file are deleted: `db.sqlite3` and the only file you have in the `migrations` folder is: ` __init__.py `  

Now on your terminal type `python3 manage.py shell` to open the Django shell  
To run the script `populate_db.py` execute the following command `exec(open('Picturest/populate_db.py').read());`  
To exit the shell type `exit`  

**IMPORTANT: You only have to execute the scrip once**  
If you want to flush the DB use the command: `python3 manage.py sqlflush | python3 manage.py dbshell`  

## Script populate_db.py
Aquest script crea 5 Users, 1 per cada un, que podeu fer servir per fer login:  
- **username**: ico, **email**: quim@gmail.com, **password**: quim  
- **username**: carol, **email**:  carolina@gmail.com, **password**: carolina  
- **username**: fran, **email**: fran@gmail.com, **password**: fran  
- **username**: pere, **email**: pere@gmail.com, **password**: pere  
- **username**: vicent, **email**: vicent@gmail.com, **password**: vicent  

Tambe crea 7 Pins, l'autor de cada Pin sera un User escollit aleatoriament (es a dir, algu de nosaltres). 

Per acabar crear 2 Friendships per User

Nota: degut a que l'autor dels Pins es escollit aleatoriament és possible que les teves 2 amistats no hagin creat cap Pin. Si aixo passa fes flush de la DB i torna a executar l'script

<!-- Req:
- docker
- docker-compose -->

## Docker 
Before this, `docker` and `docker-compose` need to be installed in your computer.  

Now that Picturest connects to docker some changes have been made to the DB config (settings.py). For a local instance of postgres we've used the following config:
````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Picturest',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
````
We'll use the next config when we want to connect to a dockerized postgres:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

Once this change is complete just execute the following command on the root of the project: `docker-compose up`. The DB and Pictures will be up after.

