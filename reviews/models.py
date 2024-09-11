from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from books.models import Book


# Create your models here.
class Review(models.Model):
    """
    Model representing a review of a book by a user.
    """

    book = models.ForeignKey(
        Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=4000)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def clean(self):
        if self.rating is None or not (1 <= self.rating <= 5):
            raise ValidationError('Rating must be between 1 and 5')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_average_rating()

    def __str__(self):
        return f"{self.rating} star review of {self.book.title} " \
               f"by {self.user.username}"
