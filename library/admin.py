from django.contrib import admin
from .models import Book, Author, BookItem, Genre, PickUpSite, Order
# Register your models here.



admin.site.register(Book)
admin.site.register(PickUpSite)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookItem)
admin.site.register(Order)