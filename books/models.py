from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    genre = models.ForeignKey(Genre, related_name="books", on_delete=models.CASCADE)
    cover_image = CloudinaryField('image', blank=False, null=False)

    def __str__(self):
        return self.title