from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import datetime

from .base_tests import BaseTestData, get_current_book_id



class UrlsUnauthenticatedUser(BaseTestData):

    def test_book_list_accessible(self):
        response = self.client.get(reverse('library:book-list'))
        self.assertEqual(response.status_code, 200)

    def test_my_books_redirect(self):
        response = self.client.get(reverse('library:user-books'))
        self.assertEqual(response.status_code, 302)

    def test_book_detail_accessible(self):
        response = self.client.get(reverse('library:book-detail', args=(1,)))
        self.assertEqual(response.status_code, 200)

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


