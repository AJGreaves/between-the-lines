from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from reviews.forms import ReviewForm

# Create your views here.

# a funciton based view for home page that dispalys all the books and their average ratings
def book_list_view(request):
    # Sort books by average rating (descending) and title (ascending)
    books = Book.objects.all().order_by('-average_rating', 'title')
    
    for book in books:
        reviews = book.reviews.all()
        book.review_count = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            book.average_rating = round(average_rating)
        else:
            book.average_rating = 0

    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context)

# a function based view for each book that shows the book details and all its reviews
def book_detail_view(request, pk, slug):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    book.review_count = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        average_rating = round(average_rating)
    else:
        average_rating = 0
    reviews = reviews.order_by('-updated_at')
    # check if the user has already reviewed the book, if so, display their review first
    user_review = None
    if request.user.is_authenticated:
        user_review = book.reviews.filter(user=request.user).first()
        if user_review:
            reviews = [user_review] + [review for review in reviews if review != user_review]

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('book_detail', pk=book.pk, slug=book.slug)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'book_detail.html', context)