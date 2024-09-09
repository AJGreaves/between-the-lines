from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Review

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_pk = review.book.pk
    book_slug = review.book.slug
    review.delete()
    return redirect(reverse('book_detail', kwargs={'pk': book_pk, 'slug': book_slug}))