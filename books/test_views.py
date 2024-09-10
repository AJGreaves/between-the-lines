from django.test import TestCase
from django.urls import reverse
from .models import Book, Genre

class BookViewsTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction", slug="fiction")
        self.book = Book.objects.create(
            title="Test Book",
            genre=self.genre,
            average_rating=4.5,
            slug="test-book"
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, self.book.title)

    def test_book_detail_view(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')
        self.assertContains(response, self.book.title)

    def test_books_by_genre_view(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_by_genre.html')
        self.assertContains(response, self.genre.name)