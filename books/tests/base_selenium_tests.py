from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from library.models import Author, BookItem, Genre, Book, Order, PickUpSite
from django.contrib.auth.models import User, Group
from datetime import datetime


class BaseSeleniumTestData(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.browser = webdriver.Chrome()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        return super().tearDownClass()
    @classmethod
    def setUp(cls):
        user, created = User.objects.get_or_create(
            username='test_user',
            email='mail@at.at',
            password='test4321'
        )
        user = User.objects.create_user(
            username='user', password='test4321')
        user2 = User.objects.create_user(
            username='user2', password='test4321', email='xd@asd.as', is_staff=True)
        group = Group.objects.get_or_create(name='moderators')

        author = Author.objects.create(
            name='J. K. Rowling'
        )
        genre = Genre.objects.create(
            genre_name='Fantasy'
        )
        book = Book.objects.create(isbn='asd123', title='Harry Potter')
        book_item = BookItem.objects.create(
            book_item=book
        )
        book.authors.add(author)
        book.genre.add(genre)

        pick_site = PickUpSite.objects.create(
            site='main', adress='test_adress')
        pick2 = PickUpSite.objects.create(
            site='secondary',
            adress='some other adress'
        )
        order = Order.objects.create(
            user=user, item=book_item, status=0, date_created=datetime.now())

        super().setUpClass()

    @classmethod
    def tearDown(cls):
        pass