from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import datetime

from library.models import Author, BookItem, Genre, Book, Order


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        user, created = User.objects.get_or_create(
            username='test_user',
            email='mail@at.at',
            password='test4321'
        )

        group = Group.objects.get_or_create(name='moderators')
    
        author = Author.objects.create(
            name='test_author'
        )
        genre = Genre.objects.create(
            genre_name='test_genre'
        )
        for item in range(22):
            book = Book.objects.create(
                isbn='21e321e',
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

        super().setUpClass()


class BookListViewTest(ViewsTests):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='test4321', is_staff=True)     
        login = self.client.login(username='admin', password='test4321')

    def test_page_accessible(self):
        response = self.client.get(reverse('library:book-list'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_10(self):
        books = Book.objects.all()
        print(len(books))
        response = self.client.get(reverse('library:book-list'))
        self.assertFalse('is_paginated' in response.context)
