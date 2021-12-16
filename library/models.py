from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField('Author')
    genre = models.ManyToManyField('Genre', null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.CharField(max_length=200)
    pages = models.IntegerField(null=True,blank=True)
    format = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre_name


User._meta.get_field('email')._unique = True