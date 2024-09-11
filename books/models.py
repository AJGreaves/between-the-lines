from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# Create your models here.
class Genre(models.Model):
    """
    Model to represent a book genre.
    Create a slug for each genre from the name.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Class representing a model for books in a database.
    Calculates and updates the average rating of the
    book based on its associated reviews.
    Automatically generates a slug for the book's URL
    if it doesn't already have one.
    """
    title = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    author = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    summary = models.TextField(max_length=1000)
    genre = models.ForeignKey(
        Genre, related_name="books", on_delete=models.CASCADE)
    cover_image = CloudinaryField('image', blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True)
    average_rating = models.FloatField(default=0)

    def update_average_rating(self):
        reviews = self.reviews.all()
        average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.average_rating = round(average_rating, 2)
        else:
            self.average_rating = 0
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
