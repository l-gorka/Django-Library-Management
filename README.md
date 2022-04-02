# Library management

- [General info](#general-info)
- [Screenshots](#screenshots)   
- [Features](#features)
- [Technologies](#technologies)
- [Setup & testing](#setup)  

<a name="general-info"></a>
# General info

This is my first web app created with the Django web framework. Primarily it was designed to familiarize me with core web development concepts such as request/response cycle, URL routing, working with the ORM. While writing this app I also learned about pagination, testing, providing different roles for moderators and regular users.

<a name="screenshots"></a>
# Screenshots:

![Home page](https://res.cloudinary.com/dgmcox/image/upload/v1648759037/library-home_tunruz.png)
<br>

![Manage orders](https://res.cloudinary.com/dgmcox/image/upload/v1648759037/library-orders_xe9lsu.png)

<br>

![Detail page](https://res.cloudinary.com/dgmcox/image/upload/v1648759038/library-detail_yr2vdq.png)

<a name="features"></a>
# Features:

The app is designed to help maintain the database of books and track the records of orders. 

As a user, you have the following options:
register an account
- search for a book by title, author or genre
- request for the book at the chosen site
- see the status of your orders
- change password

As a moderator you can:
- add, edit or delete the book
- add or remove book copy
- add pick up site
- change the status of the order

<a name="technologies"></a>
# Technologies:

- Django
- PostgreSQL
- Bootstrap
- unittest
- Docker
- docker-compose


<a name="setup"></a>
# Setup & testing:

## Setup

To run this project locally:
```bash
$ docker-copmose up
```

After the image is build and the migrations are applied, the app shoud be accessible at localhost:8000.


To populate database with some records, run:
```bash
$ docker exec -it books_web_1 bash
$ python manage.py runscript fast_load --script-args books-min.csv

```

## Tests

Some tests on the urls and the views are also included. To run them:
```bash
$ docker exec -it books_web_1 bash
$ python manage.py test
```
