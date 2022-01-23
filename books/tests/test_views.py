from django.urls import reverse
from django.contrib.auth.models import User

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

        response = self.client.get(reverse('library:user-books')+'?page=2')
        self.assertEqual(len(response.context.get('object_list')), 2)


class OrderDeleteViewTest(BaseTestData):

    def test_order_is_deleted(self):
        login = self.client.login(username='user', password='test4321')
        user = User.objects.get(username='user')
        order = make_order(user)
        id = order.id

        response = self.client.post(
            reverse('library:order-delete', args=(id,)))
        self.assertEqual(response.status_code, 302)
        deleted = get_or_none(Order, id=id)
        self.assertEqual(deleted, None)

    def test_delete_order_of_another_user(self):
        login = self.client.login(username='user', password='test4321')
        user2 = User.objects.get(username='user2')
        id = make_order(user2).id

        response = self.client.post(
            reverse('library:order-delete', args=(id,)))
        self.assertEqual(response.url, '/')
        deleted = get_or_none(Order, id=id)
        self.assertNotEqual(deleted, None)


class OrderUpdateViewTest(BaseTestData):

    def test_order_is_updated(self):
        login = self.client.login(username='user', password='test4321')
        user = User.objects.get(username='user')
        order = make_order(user)
        id = order.id
        site = PickUpSite.objects.all()[0]

        response = self.client.post(
            reverse('library:order-update', args=(id,)), {'pick_up_site': site.id})
        self.assertEqual(response.url, '/mybooks/')
        updated = Order.objects.get(id=id)
        self.assertEqual(str(updated.pick_up_site), 'main')

    def test_update_order_of_another_user(self):
        login = self.client.login(username='user', password='test4321')
        user2 = User.objects.get(username='user2')
        id = make_order(user2).id
        site = PickUpSite.objects.all()[0]

        response = self.client.post(
            reverse('library:order-update', args=(id,)), {'pick_up_site': site.id})
        self.assertEqual(response.url, '/')
        updated = Order.objects.get(id=id)
        self.assertEqual(updated.pick_up_site, None)


class StaffOrderUpdateViewTest(BaseTestData):

    def test_order_is_updated(self):
        login = self.client.login(username='user2', password='test4321')
        user = User.objects.get(username='user')
        order = make_order(user)
        id = order.id

        response = self.client.post(
            reverse('library:staff-update', args=(id,)), {'status': 2})
        self.assertEqual(response.url, '/manage/orders/')
        updated = Order.objects.get(id=id)
        self.assertEqual(str(updated.status), '2')
        self.assertNotEqual(updated.date_expiry, None)


class ManageBookViewTest(PaginationTestData):
    def setUp(self):
        login = self.client.login(username='user2', password='test4321')

    def test_search_and_page_parameters(self):
        response = self.client.get(
            reverse('library:manage-books') + '?search=test&page=2')
        self.assertEqual(len(response.context.get('book_list')), 2)


class DeleteBookViewTest(BaseTestData):

    def test_book_is_deleted(self):
        login = self.client.login(username='user2', password='test4321')
        id = Book.objects.all()[0].id

        response = self.client.post(reverse('library:book-delete', args=(id,)))
        deleted = get_or_none(Book, id=id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(deleted, None)


class UpdateBookViewTest(BaseTestData):

    def test_book_is_updated(self):
        login = self.client.login(username='user2', password='test4321')
        id = Book.objects.all()[0].id

        response = self.client.post(reverse('library:book-update', args=(id,)),
                                    {'title': 'game of thrones',
                                     'isbn': 'asde3',
                                     'image': 'test_image',
                                     'authors_str': 'author1, author2',
                                     'genres_str': 'genre1, genre2',
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all()[0].title, 'game of thrones')


class CreateBookViewTest(BaseTestData):

    def test_book_is_created(self):
        login = self.client.login(username='user2', password='test4321')
        response = self.client.post(reverse('library:add-book'),
                                    {'title': 'game of thrones',
                                     'isbn': 'asde3',
                                     'image': 'test_image',
                                     'authors_str': 'author1, author2',
                                     'genres_str': 'genre1, genre2',
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Book.objects.all()), 2)


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


class AuthorsListViewTest(BaseTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')
        Author.objects.create(name='JRR Tolkien')

    def test_authors_show_on_the_page(self):

        response = self.client.get(reverse('library:authors-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('author_list')), 2)

    def test_search_for_specified_author(self):
        response = self.client.get(
            reverse('library:authors-list')+'?search=rowling')
        self.assertEqual(len(response.context.get('author_list')), 1)
        self.assertEqual(str(response.context.get(
            'author_list')[0]), 'J. K. Rowling')


class GenresListViewTest(BaseTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')
        Genre.objects.create(genre_name='Science')

    def test_genres_show_on_the_page(self):
        response = self.client.get(reverse('library:genres-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('genre_list')), 2)


    def test_search_for_specified_genre(self):
        response = self.client.get(
            reverse('library:genres-list')+'?search=science')
        self.assertEqual(len(response.context.get('genre_list')), 1)
        self.assertEqual(str(response.context.get(
            'genre_list')[0]), 'Science')


class AuthorDetailViewTest(BaseTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')

    def test_books_of_specified_author_visible(self):
        author = Author.objects.all()[0]
        
        response = self.client.get(author.get_absolute_url())
        self.assertEqual(response.context.get('book_list')[0].__str__(), 'Harry Potter')

class GenreDetailViewTest(BaseTestData):
    def setUp(self):
        login = self.client.login(username='user', password='test4321')

    def test_books_with_specified_genre_visible(self):
        genre = Genre.objects.all()[0]
        
        response = self.client.get(genre.get_absolute_url())
        self.assertEqual(response.context.get('book_list')[0].__str__(), 'Harry Potter')