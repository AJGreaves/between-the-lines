from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from reviews.forms import ReviewForm


def book_list_view(request):
    """
    Function based view for home page that displays
    all the books and their average ratings
    Sorts books by average rating (descending) and number of ratings (descending)
    Paginates results by 10 books per page
    """
    books = Book.objects.all()

    for book in books:
        reviews = book.reviews.all()
        book.review_count = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            book.average_rating = round(average_rating)
        else:
            book.average_rating = 0

    books = sorted(books, key=lambda b: (-b.average_rating, -b.review_count))

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'num_pages': paginator.num_pages,
    }
    return render(request, 'index.html', context)


def book_detail_view(request, pk, slug):
    """
    Function based view for each book that shows
    the book details and all its reviews.
    checks if the user has already reviewed the book,
    if so, display their review first.
    Validates and saves review form after submission.
    """
    book = get_object_or_404(Book, pk=pk, slug=slug)
    reviews = book.reviews.order_by('-updated_at')
    book.review_count = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    user_review = None
    if request.user.is_authenticated:
        user_review = book.reviews.filter(user=request.user).first()
        if user_review:
            reviews = [user_review] + [
                review for review in reviews if review != user_review
            ]
    
    # Add pagination for reviews
    paginator = Paginator(reviews, 5)  # 5 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(
                request, 'Your review has been submitted successfully!')
            return redirect('book_detail', pk=book.pk, slug=book.slug)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'page_obj': page_obj,
        'average_rating': average_rating,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'book_detail.html', context)


def books_by_genre_view(request, slug):
    """
    Function based view for books by genre. Displays
    all books of a particular genre.
    Sorts books by average rating (descending) and number of ratings (descending)
    Paginates results by 10 books per page
    """

    genre = get_object_or_404(Genre, slug=slug)
    books = Book.objects.filter(
        genre=genre).order_by('-average_rating', 'title')

    for book in books:
        reviews = book.reviews.all()
        book.review_count = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            book.average_rating = round(average_rating)
        else:
            book.average_rating = 0

    books = sorted(books, key=lambda b: (-b.average_rating, -b.review_count))

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genre': genre,
        'total_books': len(books),
        'num_pages': paginator.num_pages,
    }
    return render(request, 'books_by_genre.html', context)
