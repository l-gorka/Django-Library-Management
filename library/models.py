from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    isbn = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField('Author')
    genre = models.ManyToManyField('Genre', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=200)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class BookCopy(models.Model):
    copy_book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self) -> str:
        id = str(self.pk)
        name = self.copy_book
        return f'{id} {name}'


class Loan(models.Model):
    loan_book = models.ForeignKey('BookCopy', on_delete=models.CASCADE)
    loan_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_starts = models.DateField(auto_now_add=True)
    date_ends = models.DateField()

    def __str__(self):
        return f'{self.loan_user} borrowed {self.loan_book}'


class Reservation(models.Model):
    reservation_book = models.ForeignKey('BookCopy', on_delete=models.CASCADE)
    reservation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pick_up_site = models.ForeignKey('PickUpSite', on_delete=models.CASCADE)
    date_reserved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.reservation_user} reserved {self.reservation_book}'

class PickUpSite(models.Model):
    site = models.CharField(max_length=200)
    adress = models.TextField()

    def __str__(self) -> str:
        return self.site


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre_name


User._meta.get_field('email')._unique = True
