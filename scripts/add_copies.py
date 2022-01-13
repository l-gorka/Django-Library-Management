from library.models import Book, BookItem

def run():
    book_obiects = Book.objects.all()
    book_copies = []
    for book in book_obiects:
        for x in range(2):
            book_copies.append(BookItem(book_item=book))

    added_copies = BookItem.objects.bulk_create(book_copies, batch_size=500)
    print(f'Successfully added book copies.')
            