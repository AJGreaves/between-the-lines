from django.urls import path
from .views import delete_review, edit_review

urlpatterns = [
    # Other URL patterns
    path('delete_review/<int:review_id>/',
        delete_review, name='delete_review'),
    path('edit_review/<int:review_id>/<slug:slug>/',
        edit_review, name='edit_review'),
]
