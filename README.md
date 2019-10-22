# A4-Picturest
Picturest project's repository

## How to run for the fist time
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





