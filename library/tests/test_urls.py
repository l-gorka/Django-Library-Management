from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import datetime

from library.views import Book
from library.models import Author, BookItem, Genre, Book, Order


class UrlsTests(TestCase):
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


class UrlsUnauthenticatedUser(UrlsTests):

    def test_book_list_redirect(self):
        response = self.client.get(reverse('library:book-list'))
        self.assertEqual(response.status_code, 302)

    def test_my_books_redirect(self):
        response = self.client.get(reverse('library:user-books'))
        self.assertEqual(response.status_code, 302)

    def test_book_detail_redirect(self):
        response = self.client.get(reverse('library:book-detail', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_order_create_redirect(self):
        response = self.client.get(reverse('library:order-create', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_order_delete_redirect(self):
        response = self.client.get(reverse('library:order-delete', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_order_update_redirect(self):
        response = self.client.get(reverse('library:order-update', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_add_book_item_redirect(self):
        response = self.client.get(reverse('library:add-book-item', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_admin_index_redirect(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_register_page_accessible(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_accessible(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_account_redirect(self):
        response = self.client.get(reverse('user-account'))
        self.assertEqual(response.status_code, 302)

    def test_logout_page_accessible(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_redirect(self):
        response = self.client.get(reverse('password-change'))
        self.assertEqual(response.status_code, 302)


class UrlsTestUserAuthenticated(UrlsTests):

    def setUp(self) -> None:
        user = User.objects.create_user(username='user1', password='test4321')
        login = self.client.login(username='user1', password='test4321')

    def test_book_list_accessible(self):
        response = self.client.get(reverse('library:book-list'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_accessible(self):
        response = self.client.get(reverse('password-change'))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_accessible(self):
        response = self.client.get(reverse('library:book-detail', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_manage_orders_forbidden(self):
        response = self.client.get(reverse('library:manage-orders'))
        self.assertEqual(response.status_code, 403)


class UrlsTestUserIsStaff(UrlsTests):

    def setUp(self) -> None:
        admin = User.objects.create_user(username='admin', password='test4321', is_staff=True)     
        login = self.client.login(username='admin', password='test4321')

    def test_manage_orders_page_accessible(self):
        response = self.client.get(reverse('library:manage-orders'))
        self.assertEqual(response.status_code, 200)

    def test_admin_index_page_accessible(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_add_book_item_page_accessible(self):
        response = self.client.get(reverse('library:add-book-item', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_order_delete_page_accessible_by_moderators(self):
        admin = User.objects.get(username='admin')
        group = Group.objects.get(name='moderators')
        group.user_set.add(admin)   
        response = self.client.get(reverse('library:order-delete', args=(1,)))
        self.assertEqual(response.status_code, 200)