from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from books.models import Book, Genre
from .models import Review


class DeleteReviewViewTestCase(TestCase):
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
        self.user1 = User.objects.create_user(
            username='testuser', password='12345')
        self.user2 = User.objects.create_user(
            username='otheruser', password='12345')
        self.review = Review.objects.create(
            book=self.book,
            user=self.user1,
            rating=5,
            content="Great book!",
            title="Great book!"
        )

    def test_delete_review_success(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('delete_review', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, 302)
        self.assertFalse(Review.objects.filter(
            id=self.review.id).exists())

    def test_delete_review_unauthorized(self):
        self.client.login(username='otheruser', password='12345')
        url = reverse('delete_review', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_redirection(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('delete_review', args=[self.review.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse(
            'book_detail',
            kwargs={
                'pk': self.book.pk,
                'slug': self.book.slug
            }
        ))

    def test_delete_review_success_message(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('delete_review', args=[self.review.id])
        response = self.client.post(url, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Your review has been deleted successfully!')

    def test_delete_review_non_existent(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('delete_review', args=[self.review.id])
        self.review.delete()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class EditReviewViewTestCase(TestCase):
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
        self.user1 = User.objects.create_user(
            username='testuser', password='12345')
        self.user2 = User.objects.create_user(
            username='otheruser', password='12345')
        self.review = Review.objects.create(
            book=self.book,
            user=self.user1,
            rating=5,
            content="Great book!",
            title="Great book!"
        )

    def test_edit_review_success(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('edit_review', args=[self.review.id, self.book.slug])
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content',
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Title')
        self.assertEqual(self.review.content, 'Updated content')
        self.assertEqual(self.review.rating, 4)

    def test_edit_review_unauthorized(self):
        self.client.login(username='otheruser', password='12345')
        url = reverse('edit_review', args=[self.review.id, self.book.slug])
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content',
            'rating': 4
        })
        self.assertEqual(response.status_code, 404)
        self.review.refresh_from_db()
        self.assertNotEqual(self.review.title, 'Updated Title')

    def test_edit_review_redirection(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('edit_review', args=[self.review.id, self.book.slug])
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content',
            'rating': 4
        })
        self.assertRedirects(response, reverse(
            'book_detail',
            kwargs={
                'pk': self.book.pk,
                'slug': self.book.slug
            }
        ))

    def test_edit_review_success_message(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('edit_review', args=[self.review.id, self.book.slug])
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content',
            'rating': 4
        }, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Your review has been updated successfully!')

    def test_edit_review_form_pre_population(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('edit_review', args=[self.review.id, self.book.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great book!')
        self.assertContains(response, 'Great book!')
        self.assertContains(response, '5')
