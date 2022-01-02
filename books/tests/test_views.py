from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

from library.models import Author, BookItem, Genre, Book, Order, PickUpSite
from .base_tests import BaseTestData, PaginationTestData, make_order, get_or_none


class BookListViewTest(PaginationTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')
    def test_queryset_is_22(self):
        response = self.client.get(reverse('library:book-list'))
        self.assertEqual(len(response.context.get('book_list')), 20)
        response = self.client.get(reverse('library:book-list')+'?page=2')
        self.assertEqual(len(response.context.get('book_list')), 2)
        

class BookDetailViewTest(BaseTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')

    def test_pick_up_sites_and_book_copies_accessible(self):
        id = Book.objects.all()[0].id
        response = self.client.get(reverse('library:book-detail', args=(id,)))
        self.assertEqual(len(response.context.get('sites')), 1)
        self.assertEqual(len(response.context.get('items')), 1)


class UserBooksViewTest(PaginationTestData):
        
    def test_user_orders_statuses_visible(self):
        login = self.client.login(username='user', password='test4321')
        user = User.objects.get(username='user')
        order1 = Order.objects.filter(user=user)[1]        
        order1.status = 1
        order1.save()
        order2 = Order.objects.filter(user=user)[2]
        order2.status = 2
        order2.save()

        response = self.client.get(reverse('library:user-books'))
        self.assertEqual(len(response.context.get('reserved')), 20)
        self.assertEqual(len(response.context.get('waiting')), 1)
        self.assertEqual(len(response.context.get('on_loan')), 1)


class OrderDeleteViewTest(BaseTestData):

    def test_order_is_deleted(self):
        login = self.client.login(username='user', password='test4321')
        user = User.objects.get(username='user')
        order = make_order(user)
        id = order.id

        response = self.client.post(reverse('library:order-delete', args=(id,)))
        self.assertEqual(response.status_code, 302)
        deleted = get_or_none(Order, id=id)
        self.assertEqual(deleted, None)

    def test_delete_order_of_another_user(self):
        login = self.client.login(username='user', password='test4321')
        user2 = User.objects.get(username='user2')
        id = make_order(user2).id

        response = self.client.post(reverse('library:order-delete', args=(id,)))
        self.assertEqual(response.url, '/list/')
        deleted = get_or_none(Order, id=id)
        self.assertNotEqual(deleted, None)

class OrderUpdateViewTest(BaseTestData):

    def test_order_is_updated(self):
        login = self.client.login(username='user', password='test4321')
        user = User.objects.get(username='user')
        order = make_order(user)
        id = order.id
        site = PickUpSite.objects.all()[0]

        response = self.client.post(reverse('library:order-update', args=(id,)), {'pick_up_site': site.id})
        self.assertEqual(response.url, '/mybooks/')
        updated = Order.objects.get(id=id)
        self.assertEqual(str(updated.pick_up_site), 'main')

    def test_update_order_of_another_user(self):
        login = self.client.login(username='user', password='test4321')
        user2 = User.objects.get(username='user2')
        id = make_order(user2).id
        site = PickUpSite.objects.all()[0]

        response = self.client.post(reverse('library:order-update', args=(id,)), {'pick_up_site': site.id})
        self.assertEqual(response.url, '/list/')
        updated = Order.objects.get(id=id)
        self.assertEqual(updated.pick_up_site, None)


class ManageOrdersViewTest(PaginationTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')

    def test_is_accessible_for_authenticated_user(self):
        response = self.client.get(reverse('library:manage-orders'))
        self.assertEqual(response.status_code, 200)

    def test_is_paginated_by_20(self):
        response = self.client.get(reverse('library:manage-orders'))
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context.get('order_list')), 20)

    def test_view_with_search_parameter(self):
        book = Book.objects.create(isbn='2edawq32', title='test_title2')
        book_item = BookItem.objects.create(book_item=book)
        user = User.objects.get(username='user2')

        make_order(user)
        response = self.client.get(
            reverse('library:manage-orders') + '?search=user2')
        self.assertEqual(len(response.context.get('order_list')), 20)

    def test_status_search_page_parameters(self):
        response = self.client.get(
            reverse('library:manage-orders') + '?search=user2&status=1&page=2'
        )
        self.assertEqual(len(response.context.get('order_list')), 2)
