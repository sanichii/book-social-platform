from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Author, Book, Genre, ReadingShelf

User = get_user_model()


class BooksTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='booklover',
            email='booklover@example.com',
            password='StrongPassword123!'
        )
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky')
        self.genre = Genre.objects.create(name='Classic Literature')
        self.book = Book.objects.create(title='Crime and Punishment', publication_year=1866)
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)

    def test_catalog_and_book_detail_views(self):
        catalog_response = self.client.get(reverse('books:book_catalog'))
        self.assertEqual(catalog_response.status_code, 200)
        self.assertContains(catalog_response, 'Crime and Punishment')

        detail_response = self.client.get(reverse('books:book_detail', args=[self.book.pk]))
        self.assertEqual(detail_response.status_code, 200)

    def test_update_reading_shelf(self):
        self.client.login(email='booklover@example.com', password='StrongPassword123!')
        response = self.client.post(
            reverse('books:update_reading_shelf', args=[self.book.pk]),
            {'status': 'reading'}
        )
        self.assertEqual(response.status_code, 302)
        shelf = ReadingShelf.objects.get(user=self.user, book=self.book)
        self.assertEqual(shelf.status, 'reading')