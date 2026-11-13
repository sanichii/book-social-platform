from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from books.models import Book
from .models import Post

User = get_user_model()


class PostsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='poster',
            email='poster@example.com',
            password='StrongPassword123!'
        )
        self.book = Book.objects.create(title='The Little Prince')

    def test_create_post_and_view_feed(self):
        self.client.login(email='poster@example.com', password='StrongPassword123!')
        response = self.client.post(reverse('posts:feed'), {
            'book': self.book.pk,
            'post_type': 'quote',
            'content': 'What is essential is invisible to the eye.',
            'rating': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)