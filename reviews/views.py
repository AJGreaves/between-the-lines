from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.urls import reverse
from .models import Review
from .forms import ReviewForm


@login_required
def delete_review(request, review_id):
    """
    View to delete a review and provide feedback to the user.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_pk = review.book.pk
    book_slug = review.book.slug
    review.delete()
    messages.success(request, 'Your review has been deleted successfully!')
    return redirect(reverse(
        'book_detail', kwargs={'pk': book_pk, 'slug': book_slug}))


@login_required
def edit_review(request, review_id, slug):
    """
    View to edit a review, prepopulate the form with the existing data,
    handle form submission, and provide feedback to the user.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book = review.book
    average_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        average_rating = round(average_rating)
    else:
        average_rating = 0

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your review has been updated successfully!')
            return redirect(
                'book_detail', pk=review.book.pk, slug=review.book.slug)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'book': book,
        'average_rating': average_rating,
    }
    return render(request, 'edit_review.html', context)
