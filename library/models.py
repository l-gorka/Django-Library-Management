from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.forms import ModelForm, widgets

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre_name


class Book(models.Model):
    isbn = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=200)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

"""
class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['pages']
        widgets = {'title': widgets.Textarea, 'authors': widgets.Textarea}
"""

class BookItem(models.Model):
    book_item = models.ForeignKey('Book', on_delete=models.CASCADE)
    issued_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)

    class Meta():
        verbose_name_plural = 'Book copies'

    def __str__(self) -> str:
        id = str(self.pk)
        name = self.book_item
        return f'{name}'


class StatusChoices(models.IntegerChoices):
    pending = 0, 'Pending'
    ready = 1, 'Ready to pick up'
    picked_up = 2, 'Picked up'
    returned = 3, 'Returned'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('BookItem', on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusChoices.choices, max_length=50)
    pick_up_site = models.ForeignKey(
        'PickUpSite', null=True, on_delete=models.SET_NULL)
    date_created = models.DateField()
    date_expiry = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Order no. {self.pk} - The user {self.user} ordered {self.item} '


class PickUpSite(models.Model):
    site = models.CharField(max_length=200)
    adress = models.TextField()

    def __str__(self) -> str:
        return self.site


User._meta.get_field('email')._unique = True
