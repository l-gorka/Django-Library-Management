import csv
import datetime
import random
from os import error
import sys
from library.models import Book, Author, Genre
from timeit import default_timer as timer


def run():
    start = timer()
    with open('books.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # add 200 records
        x = 0
        for row in reader:
            if x > 200:
                break
            try:
                authors = row['author'].split(',')
                authors_objects = []
                for author in authors:
                    a, created = Author.objects.get_or_create(name=author)
                    authors_objects.append(a)

                genres = row['genre'].split(',')
                genres_objects = []
                for genre in genres:
                    b, created = Genre.objects.get_or_create(genre_name=genre)
                    genres_objects.append(b)
                b, created = Book.objects.get_or_create(title=row['title'],
                                                        description=row['desc'],
                                                        image=row['img'],
                                                        pages=row['pages'],
                                                        format=row['bookformat'],
                                                        isbn=row['isbn'],
                                                        )
                #print(b.id, b.title)
                for author in authors_objects:
                    b.authors.add(author)
                for genre in genres_objects:
                    b.genre.add(genre)
                b.save()
            except error as e:
                print(e)

            x += 1
        stop = timer()
        print('books time: ', datetime.timedelta(seconds=stop-start))
