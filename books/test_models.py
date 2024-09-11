from django.contrib.auth.models import User
from django.test import TestCase
from .models import Genre, Book
from reviews.models import Review
from django.utils.text import slugify

class GenreModelTestCase(TestCase):
    def setUp(self):
        self.genre_name = "Science Fiction"
        self.genre = Genre.objects.create(name=self.genre_name)
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, self.genre_name)
        self.assertIsNotNone(self.genre.id)

    def test_slug_generation(self):
        self.assertEqual(self.genre.slug, slugify(self.genre_name))

    def test_unique_name(self):
        with self.assertRaises(Exception):
            Genre.objects.create(name=self.genre_name)

    def test_unique_slug(self):
        with self.assertRaises(Exception):
            Genre.objects.create(name="Another Genre", slug=self.genre.slug)

    def test_string_representation(self):
        self.assertEqual(str(self.genre), self.genre_name)

class BookModelTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.book_title = "Test Book"
        self.book = Book.objects.create(
            title=self.book_title,
            genre=self.genre,
            author="Author Name",
            description="A test book description",
            summary="A test book summary",
            cover_image="image_url"
        )
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_book_creation(self):
        self.assertEqual(self.book.title, self.book_title)
        self.assertIsNotNone(self.book.id)

    def test_slug_generation(self):
        self.assertEqual(self.book.slug, slugify(self.book_title))

    def test_unique_title(self):
        with self.assertRaises(Exception):
            Book.objects.create(
                title=self.book_title,
                genre=self.genre,
                author="Another Author",
                description="Another description",
                summary="Another summary",
                cover_image="another_image_url"
            )

    def test_unique_slug(self):
        with self.assertRaises(Exception):
            Book.objects.create(
                title="Another Book",
                genre=self.genre,
                author="Another Author",
                description="Another description",
                summary="Another summary",
                cover_image="another_image_url",
                slug=self.book.slug
            )

    def test_string_representation(self):
        self.assertEqual(str(self.book), self.book_title)

    def test_update_average_rating(self):
        # Create some reviews for the book
        Review.objects.create(book=self.book, user=self.user1, rating=4, content="Good book")
        Review.objects.create(book=self.book, user=self.user2, rating=5, content="Great book")
        self.book.update_average_rating()
        self.assertEqual(self.book.average_rating, 4.5)