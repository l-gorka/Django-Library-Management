import csv
import datetime
from os import error
from library.models import Author, Genre, Book
from timeit import default_timer as timer
from datetime import timedelta
from multiprocessing.pool import ThreadPool as Pool



def run():
    genres()
    authors()
    books2()


def genres():
    start = timer()
    with open('books.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        genres_list = []
        for row in reader:
            genres_list.extend([genre for genre in row['genre'].split(',')])
        genres_objects = [Genre(genre_name=genre)
                          for genre in list(set(genres_list))]
        print('genres list', len(genres_list))
        print('genres set', len(genres_objects))
        Genre.objects.bulk_create(genres_objects, batch_size=200)

        stop = timer()
        print('genres time ', datetime.timedelta(seconds=stop-start))


def authors():
    start = timer()
    with open('books.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        authors_list = []
        for row in reader:
            authors_list.extend(
                [author for author in row['author'].split(',')])
        genres_objects = [Author(name=author)
                          for author in list(set(authors_list))]
        print('authors list', len(authors_list))
        print('authors set', len(genres_objects))
        Author.objects.bulk_create(genres_objects, batch_size=200)

        stop = timer()
        print('authors time: ', datetime.timedelta(seconds=stop-start))


def books():
    start = timer()
    with open('books.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        i = 1
        for row in reader:
            book_object = Book(
                title=row['title'][:200],
                description=row['desc'],
                image=row['img'],
                pages=row['pages'],
                format=row['bookformat'],
                isbn=row['isbn'],
            )
            book_object.save()
            authors_object = [Author.objects.get(name=author) for author in row['author'].split(',')]
            book_object.authors.add(*authors_object)

            genres_object = [Genre.objects.get(genre_name=genre) for genre in row['genre'].split(',')]
            book_object.genre.add(*genres_object)

            book_object.save()
            i += 1
            #print(i, book_object)
            if i % 200 == 0:
                print(f'processed {i} books')

        stop = timer()
        print('books time: ', datetime.timedelta(seconds=stop-start))
        

def books2():
    start = timer()
    with open('books.csv', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        i = 1

        for row in reader:
            book_object = Book(
                id=i,
                title=row['title'][:200],
                description=row['desc'],
                image=row['img'],
                pages=row['pages'],
                format=row['bookformat'],
                isbn=row['isbn'],
            )
            authors_object = [Author.objects.get(name=author) for author in row['author'].split(',')]
            book_object.authors.t.add(*authors_object)

            genres_object = [Genre.objects.get(genre_name=genre) for genre in row['genre'].split(',')]
            book_object.genre.add(*genres_object)

            book_object.save()
            i += 1
            #print(i, book_object)
            if i % 200 == 0:
                print(f'processed {i} books')

        stop = timer()
        print('books time: ', datetime.timedelta(seconds=stop-start))


def multi_books():
    start = timer()
    
    def get_next_line():
        with open('books.csv', 'r', newline='') as csvfile:
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
        authors_object = [Author.objects.get(name=author) for author in row['author'].split(',')]
        book_object.authors.add(*authors_object)

        genres_object = [Genre.objects.get(genre_name=genre) for genre in row['genre'].split(',')]
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
        with open('books.csv', 'r', newline='') as csvfile:
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
        authors_object = [Author.objects.get(name=author) for author in row['author'].split(',')]
        book_object.authors.add(*authors_object)

        genres_object = [Genre.objects.get(genre_name=genre) for genre in row['genre'].split(',')]
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