# between_the_lines/contexts/genre_context.py
from books.models import Genre

def genres(request):
    genres_with_books = Genre.objects.filter(books__isnull=False).distinct()
    return {
        'genres': genres_with_books
    }