import csv
import datetime
from os import error
from library.models import Author, Genre, Book, ThroughAuthor, ThroughGenre
from timeit import default_timer as timer
from datetime import timedelta
from multiprocessing.pool import ThreadPool as Pool


def run():
    g = genres()
    a = authors()
    books(g, a)


def genres():
    start = timer()
    with open('books-min.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        genres_list = []
        for row in reader:
            genres_list.extend([genre for genre in row['genre'].split(',')])
        genres_objects = [Genre(genre_name=genre)
                          for genre in list(set(genres_list))]
        print('genres list', len(genres_list))
        print('genres set', len(genres_objects))
        genres_created = Genre.objects.bulk_create(
            genres_objects, batch_size=200)

        stop = timer()
        print('genres time ', datetime.timedelta(seconds=stop-start))
        genres = []
        for item in genres_created:
            genres.append([item.id, item.genre_name])
        return genres


def authors():
    start = timer()
    with open('books-min.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        authors_list = []
        for row in reader:
            authors_list.extend(
                [author for author in row['author'].split(',')])
        genres_objects = [Author(name=author)
                          for author in list(set(authors_list))]
        print('authors list', len(authors_list))
        print('authors set', len(genres_objects))
        authors_created = Author.objects.bulk_create(
            genres_objects, batch_size=200)

        stop = timer()
        print('authors time: ', datetime.timedelta(seconds=stop-start))
        authors = []
        for author in authors_created:
            authors.append([author.id, author.name])
        return authors


def books(genres_objects, authors_objects):
    start = timer()
    with open('books-min.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        i = 0
        book_list = []
        for row in reader:
            book_list.append(Book(
                title=row['title'][:200],
                description=row['desc'],
                image=row['img'],
                pages=row['pages'],
                format=row['bookformat'],
                isbn=row['isbn'],
            ))

        Book.objects.bulk_create(book_list)

    with open('books-min.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        i = 1
        through_genre = []
        through_author = []
        for row in reader:
            genres = row['genre'].split(',')
            for genre in genres:
                id = genres_objects.index(genre)
                obj = ThroughGenre(book_id=i, genre_id=id)
                through_genre.append(obj)

            authors = row['author'].split(',')
            for author in authors:
                id = authors_objects.index(author)
                obj = ThroughAuthor(book_id=i, author_id=id)
                through_author.append(obj)

            i += 1
            if i % 1000 == 0:
                print('processed', i)

        ThroughGenre.objects.bulk_create(through_genre, batch_size=500)
        ThroughAuthor.objects.bulk_create(through_author, batch_size=500)
        stop = timer()
        print('books-min time: ', datetime.timedelta(seconds=stop-start))


def multi_books():
    start = timer()

    def get_next_line():
        with open('books-min.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def process_book(row):
        book_object = Book(
            title=row['title'][:200],
            description=row['desc'],
            image=row['img'],
            pages=row['pages'],
            format=row['bookformat'],
            isbn=row['isbn'],
        )
        book_object.save()
        authors_object = [Author.objects.get(
            name=author) for author in row['author'].split(',')]
        book_object.authors.add(*authors_object)

        genres_object = [Genre.objects.get(
            genre_name=genre) for genre in row['genre'].split(',')]
        book_object.genre.add(*genres_object)

        book_object.save()
        print(book_object)

    data = list(get_next_line())[:200]
    t = Pool(processes=8)

    for row in data:
        t.map(process_book, (row,))
    t.close()
    stop = timer()
    print('books time: ', datetime.timedelta(seconds=stop-start))


def multi_books_two():

    def get_next_line():
        with open('books-min.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def process_book(row):
        book_object = Book(
            title=row['title'][:200],
            description=row['desc'],
            image=row['img'],
            pages=row['pages'],
            format=row['bookformat'],
            isbn=row['isbn'],
        )
        book_object.save()
        authors_object = [Author.objects.get(
            name=author) for author in row['author'].split(',')]
        book_object.authors.add(*authors_object)

        genres_object = [Genre.objects.get(
            genre_name=genre) for genre in row['genre'].split(',')]
        book_object.genre.add(*genres_object)

        book_object.save()

    data = list(get_next_line())[:200]
    t = Pool(1)
    start = timer()
    for row in data:
        t.apply(process_book, (row,))
    t.close()
    stop = timer()
    print('books time: ', datetime.timedelta(seconds=stop-start))
