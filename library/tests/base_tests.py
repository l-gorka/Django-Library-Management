from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import date, datetime

from django.views.generic.base import View

from library.models import Author, BookItem, Genre, Book, Order, PickUpSite

def make_order(user):
    order = Order.objects.create(
                user=user,
                item=BookItem.objects.all()[0],
                status=3,
                date_created=datetime.now(),
            )
    return order

def get_or_none(Model, **kwargs):
    try:
        return Model.objects.get(**kwargs)
    except Model.DoesNotExist:
        return None


class BaseTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        user, created = User.objects.get_or_create(
            username='test_user',
            email='mail@at.at',
            password='test4321'
        )
        user = User.objects.create_user(
            username='user', password='test4321')
        user2 = User.objects.create_user(
            username='user2', password='test4321', email='xd@asd.as')
        group = Group.objects.get_or_create(name='moderators')

        author = Author.objects.create(
            name='test_author'
        )
        genre = Genre.objects.create(
            genre_name='test_genre'
        )
        book = Book.objects.create(isbn='asd123', title='Hari pota')
        book_item = BookItem.objects.create(
            book_item=book
        )
        pick_site = PickUpSite.objects.create(site='main', adress='test_adress')

        super().setUpTestData()


class PaginationTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        user, created = User.objects.get_or_create(
            username='test_user',
            email='mail@at.at',
            password='test4321'
        )
        user = User.objects.create_user(
            username='user', password='test4321', is_staff=True)
        user2 = User.objects.create_user(
            username='user2', password='test4321', email='xd@asd.as', is_staff=True)
        group = Group.objects.get_or_create(name='moderators')

        author = Author.objects.create(
            name='test_author'
        )
        genre = Genre.objects.create(
            genre_name='test_genre'
        )
        for item in range(22):
            book = Book.objects.create(
                isbn='21e321e'+str(item),
                title='test_title',
            )
            book_item = BookItem.objects.create(
                book_item=book
            )
            order = Order.objects.create(
                user=user,
                item=book_item,
                status=0,
                date_created=datetime.now(),
            )
            order2 = Order.objects.create(
                user=user2,
                item=book_item,
                status=1,
                date_created=datetime.now(),
            )
        book_item = BookItem.objects.create(
            book_item=book
        )
        PickUpSite.objects.create(site='main', adress='test_adress')

        super().setUpTestData()