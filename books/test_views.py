from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.db.models import Avg
from .models import Book, Genre
from reviews.models import Review

class BookListViewTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction", slug="fiction")
        self.books = [
            Book.objects.create(
                title=f"Book {i}",
                genre=self.genre,
                average_rating=4.5 if i % 2 == 0 else 3.0,
                slug=f"book-{i}"
            ) for i in range(15) # generate 15 books for testing
        ]

    def test_book_list_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_books_sorted_by_rating_and_title(self):
        response = self.client.get(reverse('home'))
        books = response.context['page_obj'].object_list
        sorted_books = sorted(self.books, key=lambda x: (-x.average_rating, x.title))
        self.assertEqual(list(books), sorted_books[:10])

    def test_pagination(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_review_count_and_average_rating(self):
        response = self.client.get(reverse('home'))
        books = response.context['page_obj'].object_list
        for book in books:
            self.assertEqual(book.review_count, book.reviews.count())
            self.assertEqual(book.average_rating, round(book.reviews.aggregate(Avg('rating'))['rating__avg'] or 0))

    def test_no_books(self):
        Book.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['page_obj'].paginator.count, 0)


class BookDetailViewTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            genre=self.genre,
            average_rating=4.5
        )
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            content="Great book!"
        )

    def test_book_detail_view_status_code(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_detail_view_template(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'book_detail.html')

    def test_book_detail_view_context_data(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        self.assertIn('book', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('average_rating', response.context)
        self.assertIn('form', response.context)
        self.assertIn('user_review', response.context)
        self.assertEqual(response.context['book'].review_count, 1)

    def test_review_form_submission(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        # Log in as a different user to submit a new review
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.client.login(username='newuser', password='12345')
        response = self.client.post(url, {
            'title': 'Test Book',
            'rating': 4,
            'content': 'Another great review!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(Review.objects.count(), 2)  # Ensure a new review is created

    def test_review_ordering(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        reviews = response.context['reviews']
        self.assertEqual(reviews[0], self.review)  # User's review should be first

    def test_success_message(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        # Log in as a different user to submit a new review
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.client.login(username='newuser', password='12345')
        response = self.client.post(url, {
            'title': 'Test Book',
            'rating': 4,
            'content': 'Another great review!'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your review has been submitted successfully!')
    
    def test_no_form_for_existing_review(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        self.assertNotContains(response, '<form id="review-form"')  # Ensure the form is not present in the response