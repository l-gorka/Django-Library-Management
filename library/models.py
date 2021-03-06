from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete


class AuthorManager(models.Manager):

    def create_or_new(self, name):
        name = name.strip()
        qs = self.get_queryset().filter(name__iexact=name)
        if qs.exists():
            return qs.first(), False
        return Author.objects.create(name=name), True

    def comma_to_qs(self, authors_str):
        final_ids = []
        for author in authors_str.split(','):
            obj, created = self.create_or_new(author)
            final_ids.append(obj.id)
        qs = self.get_queryset().filter(id__in=final_ids).distinct()
        return qs


class GenreManager(models.Manager):

    def create_or_new(self, genre_name):
        genre_name = genre_name.strip()
        qs = self.get_queryset().filter(genre_name__iexact=genre_name)
        if qs.exists():
            return qs.first(), False
        return Genre.objects.create(genre_name=genre_name), True

    def comma_to_qs(self, genres_str):
        final_ids = []
        for genre in genres_str.split(','):
            obj, created = self.create_or_new(genre)
            final_ids.append(obj.id)
        qs = self.get_queryset().filter(id__in=final_ids).distinct()
        return qs


class Author(models.Model):
    name = models.CharField(max_length=200)

    objects = AuthorManager()

    def get_absolute_url(self):
        return reverse('library:author-detail', args=[str(self.pk)])
    

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    objects = GenreManager()

    def get_absolute_url(self):
        return reverse('library:genre-detail', kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.genre_name


class Book(models.Model):
    isbn = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, through='ThroughAuthor')
    genre = models.ManyToManyField(Genre, through='ThroughGenre')
    description = models.TextField(null=True, blank=True)
    image = models.CharField(
        max_length=200, default='https://isocarp.org/app/uploads/2014/05/noimage.jpg')
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class ThroughGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class ThroughAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BookItem(models.Model):
    book_item = models.ForeignKey('Book', on_delete=models.CASCADE)
    issued_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta():
        verbose_name_plural = 'Book items'

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
    status = models.IntegerField(choices=StatusChoices.choices)
    pick_up_site = models.ForeignKey(
        'PickUpSite', null=True, on_delete=models.SET_NULL)
    date_created = models.DateField()
    date_picked = models.DateField(null=True, blank=True)
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


def order_save(sender, instance, **kwargs):
    book_item = BookItem.objects.get(id=instance.item.id)

    if instance.status == 2:
        book_item.issued_to = instance.user
        book_item.issue_date = instance.date_picked
        book_item.expiry_date = instance.date_expiry
        book_item.save()

    if instance.status == 3:
        book_item.issued_to = None
        book_item.issue_date = None
        book_item.expiry_date = None
        book_item.save()

def order_delete(sender, instance, **kwargs):
    book_item = BookItem.objects.get(id=instance.item.id)
    book_item.issued_to = None
    book_item.issue_date = None
    book_item.expiry_date = None
    book_item.save()

post_save.connect(order_save, sender=Order)
pre_delete.connect(order_delete, sender=Order)
