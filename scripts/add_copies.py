from library.models import Book, BookItem
import random

def run():
    book_obiects = Book.objects.all()
    for book in book_obiects:
        x = random.randint(1,2)
        for i in range(x):
            copy = BookItem(book_item=book)
            copy.save()
            print(copy)