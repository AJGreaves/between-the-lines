from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from books.models import Book, Genre
from .models import Review


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            genre=self.genre,
            author="Author Name",
            description="A test book description",
            summary="A test book summary",
            cover_image="image_url"
        )
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_review_creation(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            title="Great Book",
            content="This is a great book!",
            rating=5
        )
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.title, "Great Book")
        self.assertEqual(review.content, "This is a great book!")
        self.assertEqual(review.rating, 5)
        self.assertIsNotNone(review.id)

    def test_unique_review_per_user_per_book(self):
        Review.objects.create(
            book=self.book,
            user=self.user,
            title="Great Book",
            content="This is a great book!",
            rating=5
        )
        with self.assertRaises(Exception):
            Review.objects.create(
                book=self.book,
                user=self.user,
                title="Another Review by the same user",
                content="This is another review by the same user!",
                rating=4
            )

    def test_rating_validation(self):
        review = Review(
            book=self.book,
            user=self.user,
            title="Invalid Rating",
            content="This review has an invalid rating!",
            rating=6
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_string_representation(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            title="Great Book",
            content="This is a great book!",
            rating=5
        )
        self.assertEqual(
            str(review),
            f"5 star review of {self.book.title} by {self.user.username}")

    def test_average_rating_update(self):
        Review.objects.create(
            book=self.book,
            user=self.user,
            title="Great Book",
            content="This is a great book!",
            rating=5
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.average_rating, 5.0)

        new_user = User.objects.create_user(
            username='newuser', password='12345')
        Review.objects.create(
            book=self.book,
            user=new_user,
            title="Good Book",
            content="This is a good book!",
            rating=3
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.average_rating, 4.0)
