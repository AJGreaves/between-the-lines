from django.urls import path
from .views import delete_review

urlpatterns = [
    # Other URL patterns
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
]