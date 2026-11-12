
from django.db import models


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="First Name"
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="Last Name"
    )

    biography = models.TextField(
        blank=True,
        verbose_name="Biography"
    )

    image = models.ImageField(
        upload_to='authors/',
        blank=True,
        null=True,
        verbose_name="Author Image"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Genre Name"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Book Title"
    )

    authors = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name="Authors"
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='books',
        verbose_name="Genres"
    )

    isbn = models.CharField(
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="ISBN"
    )

    cover_image = models.ImageField(
        upload_to='books/covers/',
        blank=True,
        null=True,
        verbose_name="Cover Image"
    )

    publication_year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Publication Year"
    )

    summary = models.TextField(
        blank=True,
        verbose_name="Book Summary"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


class ReadingShelf(models.Model):

    STATUS_CHOICES = [
        ('want_to_read', 'Want to Read'),
        ('reading', 'Currently Reading'),
        ('finished', 'Finished'),
    ]

    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='reading_shelves',
        verbose_name='User'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reading_shelves',
        verbose_name='Book'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='want_to_read',
        verbose_name='Reading Status'
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Added At'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-updated_at']
        verbose_name = 'Reading Shelf'
        verbose_name_plural = 'Reading Shelves'

    def __str__(self):
        return f"{self.user} - {self.book} ({self.status})"
