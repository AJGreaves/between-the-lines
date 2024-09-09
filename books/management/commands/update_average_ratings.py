from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Update average ratings for all books based on existing reviews'

    def handle(self, *args, **kwargs):
        books = Book.objects.all()
        for book in books:
            book.update_average_rating()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated average rating for book: {book.title}'))