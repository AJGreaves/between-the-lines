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
            ) for i in range(15)  # generate 15 books for testing
        ]

    def test_book_list_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

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
            self.assertEqual(book.average_rating, round(
                book.reviews.aggregate(Avg('rating'))['rating__avg'] or 0))

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
        self.user = User.objects.create_user(
            username='testuser', password='12345')
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
        new_user = User.objects.create_user(
            username='newuser', password='12345')
        self.client.login(username='newuser', password='12345')
        response = self.client.post(url, {
            'title': 'Test Book',
            'rating': 4,
            'content': 'Another great review!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    def test_review_ordering(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        reviews = response.context['reviews']
        # User's review should be first
        self.assertEqual(reviews[0], self.review)

    def test_success_message(self):
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        # Log in as a different user to submit a new review
        new_user = User.objects.create_user(
            username='newuser', password='12345')
        self.client.login(username='newuser', password='12345')
        response = self.client.post(url, {
            'title': 'Test Book',
            'rating': 4,
            'content': 'Another great review!'
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Your review has been submitted successfully!')

    def test_no_form_for_existing_review(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('book_detail', args=[self.book.pk, self.book.slug])
        response = self.client.get(url)
        # Ensure the form is not present in the response
        self.assertNotContains(response, '<form id="review-form"')


class BooksByGenreViewTestCase(TestCase):
    def setUp(self):
        # Create a genre and some books
        self.genre = Genre.objects.create(name="Fiction", slug="fiction")
        self.empty_genre = Genre.objects.create(
            name="Non-Fiction", slug="non-fiction")
        self.books = [
            Book.objects.create(
                title=f"Book {i}",
                genre=self.genre,
                average_rating=4.5
            ) for i in range(1, 12)  # Create 11 books
        ]

        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_books_by_genre_view_status_code(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_books_by_genre_view_invalid_genre(self):
        url = reverse('books_by_genre', args=['non-existent-genre'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_books_by_genre_view_template(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books_by_genre.html')

    def test_books_by_genre_view_context_data(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertIn('genre', response.context)
        self.assertEqual(response.context['genre'], self.genre)

    def test_books_by_genre_view_page_obj(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertIn('page_obj', response.context)
        self.assertTrue(hasattr(response.context['page_obj'], 'object_list'))

    def test_books_by_genre_view_total_books(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertIn('total_books', response.context)
        self.assertEqual(response.context['total_books'], 11)

    def test_books_by_genre_view_num_pages(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertIn('num_pages', response.context)
        self.assertEqual(
            response.context['num_pages'],
            response.context['page_obj'].paginator.num_pages)

    def test_books_by_genre_view_ordering(self):
        # Create additional books with varying ratings and review counts
        book_12 = Book.objects.create(title="Book 12", genre=self.genre)
        book_13 = Book.objects.create(title="Book 13", genre=self.genre)
        book_14 = Book.objects.create(title="Book 14", genre=self.genre)
        
        # Add reviews to adjust review counts and average ratings
        Review.objects.create(
            book=book_12, user=self.user1, title="Review 1",
            content="Good book", rating=4)
        Review.objects.create(
            book=book_12, user=self.user2, title="Review 2",
            content="Nice read", rating=4)
        Review.objects.create(
            book=book_13, user=self.user1, title="Review 3",
            content="Excellent", rating=5)
        Review.objects.create(
            book=book_14, user=self.user1, title="Review 4",
            content="Great", rating=4)
        Review.objects.create(
            book=book_14, user=self.user2, title="Review 5",
            content="Amazing", rating=5)
        
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        books = response.context['page_obj'].object_list
        
        # Check ordering by average rating and review count
        self.assertTrue(all(
            (books[i].average_rating > books[i + 1].average_rating) or
            (books[i].average_rating == books[i + 1].average_rating and
             books[i].review_count >= books[i + 1].review_count)
            for i in range(len(books) - 1)
        ))

    def test_books_by_genre_view_pagination(self):
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertIn('page_obj', response.context)
        # 10 books per page
        self.assertEqual(len(response.context['page_obj'].object_list), 10)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)

    def test_books_by_genre_view_empty_genre(self):
        url = reverse('books_by_genre', args=[self.empty_genre.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        # No books in this genre
        self.assertEqual(len(response.context['page_obj'].object_list), 0)
        self.assertEqual(response.context['total_books'], 0)

    def test_books_by_genre_view_large_number_of_books(self):
        # Create a large number of books
        for i in range(12, 102):  # Create 90 more books, total 101
            Book.objects.create(
                title=f"Book {i}",
                genre=self.genre,
                average_rating=4.5 if i % 2 == 0 else 4.0
            )
        url = reverse('books_by_genre', args=[self.genre.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        # 10 books per page
        self.assertEqual(len(response.context['page_obj'].object_list), 10)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 11)
