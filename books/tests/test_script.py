from django.test import TestCase
from library.models import Book, Author, Genre
from scripts.fast_load import run


class FastLoadScriptTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        run('books-min.csv')
        super().setUpTestData()

    def test_script_adds_book_objects(self):

        books = Book.objects.all().count()
        self.assertEqual(books, 29)

    def test_script_adds_genre_objects(self):

        genres = Genre.objects.all().count()
        self.assertEqual(genres, 85)

    def test_script_adds_author_objects(self):

        authors = Author.objects.all().count()
        self.assertEqual(authors, 33)

    def test_script_adds_genre_to_the_book(self):

        book = Book.objects.all()[0]

        self.assertIn('Native Americans', str(book.genre.all()))

    def test_script_adds_author_to_the_book(self):

        book = Book.objects.all()[0]

        self.assertIn('Laurence M. Hauptman', str(book.authors.all()))
