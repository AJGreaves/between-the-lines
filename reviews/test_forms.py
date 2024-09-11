from django.test import TestCase
from .forms import ReviewForm


class ReviewFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'Great Book',
            'content': 'This is a great book!',
            'rating': 5
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        form_data = {
            'title': 'Great Book',
            'content': 'This is a great book!',
            'rating': 6  # Invalid rating
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(
            form.errors['rating'],
            ['Ensure this value is less than or equal to 5.'])

    def test_missing_title(self):
        form_data = {
            'content': 'This is a great book!',
            'rating': 5
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_missing_content(self):
        form_data = {
            'title': 'Great Book',
            'rating': 5
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])

    def test_missing_rating(self):
        form_data = {
            'title': 'Great Book',
            'content': 'This is a great book!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(form.errors['rating'], ['This field is required.'])
