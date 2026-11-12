from django.conf import settings
from django.db import models
from books.models import Book


class Post(models.Model):
    POST_TYPES = [
        ('review', 'Book Review'),
        ('quote', 'Book Quote'),
        ('thought', 'Reading Thought'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Author User",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Related Book",
    )
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
        default='thought',
        verbose_name="Post Type",
    )
    content = models.TextField(verbose_name="Post Content / Quote")
    image = models.ImageField(
        upload_to='posts/images/',
        blank=True,
        null=True,
        verbose_name="Post Image (Book-gram)",
    )
    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Optional rating from 1 to 5",
        verbose_name="Rating (1-5)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.user.username} on {self.book.title} ({self.post_type})"