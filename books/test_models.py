from django.test import TestCase
from .models import Genre
from django.utils.text import slugify

class GenreModelTestCase(TestCase):
    def setUp(self):
        self.genre_name = "Science Fiction"
        self.genre = Genre.objects.create(name=self.genre_name)

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