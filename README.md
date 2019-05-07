
## Introduction
Internship Management Portal, made as a part of Software Engineering course CS4443, for Winter 2019 Semester at IIT Hyderabad.

## Pre-Requisites
This project uses various libraries listed below, please install them in order to run the application.

- Flask Library for python
Flask is a micro web framework written in Python.
install it using the following command: 
```
pip install Flask
```

- WT-Forms 
WT forms used to generate different forms in the file such as login forms, register forms, etc
install using the following command:
```
pip install flask-wtf
```

- SQL Alchemy
This library used so that we can create and manage sqlite databases in our program
install using the follwing command:
```
pip install flask-sqlalchemy
```

- Bcrypt
This library used to hash passwords before storing them in database so that passwords are safe
install using the follwing command:
```
pip install flask-bcrypt
```

- Flask-login
Used to maintain user login state information
install using the following command:
```
pip install flask-login
```

- Pillow
For image resizing
```
pip install Pillow
```


## How to run
This application assumes there is a db already created with required table formats,
to accomplish this use the following command:
browse to the directory location of run.py that is the top level in our hierarchy.
open a python console then write the following 2 commands
```
python
>>> from flaskblog import db
>>> db.create_all()
```

use the following command in console
```
FLASK_APP=run.py flask run
```
OR start in debug mode
```
python run.py
```

## Admin Guide
To unlock the ability to post internships from a newly created faculty account,
Check the userid of the account by logging in from the account and checking the
user id field displayed there.
go to the url "/admin"
> localhost:5000/admin

There in the ID section mention the ID
In the password section select the password, default one is "testing". This can
be changed in the "routes.py" file in line 237.


## Refrences
- Overall basic structure, layout and design of the code has been inspired from:
https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
For the purpose of understanding flask library syntax.

- Bootsrap html styles
https://getbootstrap.com/docs/4.3/getting-started/introduction/

- Flask Documentation
http://flask.pocoo.org/docs/1.0/

## Credits

Atul Raj 			CS15BTECH11006
Apoorv Choudhary	CS15BTECH11004
Narwade Shubham		CS15BTECH11026


