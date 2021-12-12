from django.contrib import admin
from .models import Book, Author, Genre
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    fields = ['title',
              'authors',
              'genre',
              'description',
              'image',
              'pages',
              'format',
              ]


class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']


class GenreAdmin(admin.ModelAdmin):
    fields = ['genre_name']


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
