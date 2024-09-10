# between_the_lines/contexts/genre_context.py
from books.models import Genre

def genres(request):
    return {
        'genres': Genre.objects.all()
    }