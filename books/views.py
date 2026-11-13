from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Book, Genre, ReadingShelf
from posts.models import Post


def book_catalog(request):
    books = Book.objects.all().prefetch_related('authors', 'genres')

    search_query = request.GET.get('search', '')
    genre_id = request.GET.get('genre', '')

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(authors__first_name__icontains=search_query) |
            Q(authors__last_name__icontains=search_query)
        ).distinct()

    if genre_id:
        books = books.filter(genres__id=genre_id)

    genres = Genre.objects.all()

    context = {
        'books': books,
        'genres': genres,
        'search_query': search_query,
        'selected_genre': genre_id,
    }
    return render(request, 'books/book_catalog.html', context)


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.prefetch_related('authors', 'genres'),
        pk=pk
    )

    reading_shelf = None
    if request.user.is_authenticated:
        reading_shelf = ReadingShelf.objects.filter(
            user=request.user,
            book=book
        ).first()

    book_posts = Post.objects.filter(book=book).select_related('user')

    context = {
        'book': book,
        'reading_shelf': reading_shelf,
        'status_choices': ReadingShelf.STATUS_CHOICES,
        'book_posts': book_posts,
    }
    return render(request, 'books/book_detail.html', context)


@login_required
def update_reading_shelf(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'remove':
            ReadingShelf.objects.filter(user=request.user, book=book).delete()
            messages.info(request, f'Removed "{book.title}" from your shelf.')
        elif status in dict(ReadingShelf.STATUS_CHOICES):
            ReadingShelf.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'status': status}
            )
            messages.success(request, f'Updated reading status for "{book.title}".')
    return redirect('books:book_detail', pk=book.pk)