from django.contrib import admin
from .models import Book, Author, BookCopy, Genre, Loan, Reservation, PickUpSite
# Register your models here.



admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Reservation)
admin.site.register(PickUpSite)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookCopy)