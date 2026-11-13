from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from books.models import Book
from posts.models import Post
from .models import Follow, Like

User = get_user_model()


class InteractionsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='StrongPassword123!'
        )
        self.user2 = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='StrongPassword123!'
        )
        self.book = Book.objects.create(title='Dune')
        self.post = Post.objects.create(
            user=self.user2,
            book=self.book,
            post_type='review',
            content='A sci-fi masterpiece.'
        )

    def test_cannot_follow_self(self):
        with self.assertRaises(ValidationError):
            Follow.objects.create(follower=self.user1, following=self.user1)

    def test_toggle_like_and_follow(self):
        self.client.login(email='alice@example.com', password='StrongPassword123!')

        self.client.post(reverse('posts:toggle_like', args=[self.post.pk]))
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())

        self.client.post(reverse('interactions:toggle_follow', args=[self.user2.username]))
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())