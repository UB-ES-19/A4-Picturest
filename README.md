# A4-Picturest
Picturest project's repository

## How to run for the fist time
Clone the last version of the project on your computer (current: `quim/pins_from_following`)  
Make sure this file are deleted: `db.sqlite3` and the only file you have in the `migrations` folder is: ` __init__.py `  

Now on your terminal type `python3 ./manage.py shell` to open the Django shell  
Execute the following command `exec(open('Picturest/populate_db.py').read());` to run the script `populate_db.py`

## Script populate_db.py
Aquest script crea 5 Users:
"username": "ico", "age": 23, "email": "quim@gmail.com", "password": "quim"  
"username": "carol", "age": 23, "email":  "carolina@gmail.com", "password": "carolina"  
"username": "fran", "age": 23, "email": "fran@gmail.com", "password": "fran"  
"username": "pere", "age": 23, "email": "pere@gmail.com", "password": "pere"  
"username": "vicent", "age": 23, "email": "vicent@gmail.com", "password": "vicent"  





