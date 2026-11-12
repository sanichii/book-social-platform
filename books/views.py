
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Book, Genre, ReadingShelf

def book_catalog(request):
    books = Book.objects.all().prefetch_related(
        'authors',
        'genres'
    )

    search_query = request.GET.get('search', '')
    genre_id = request.GET.get('genre', '')

    # Search by book title or author name
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(authors__first_name__icontains=search_query) |
            Q(authors__last_name__icontains=search_query)
        ).distinct()

    # Filter books by genre
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
        Book.objects.prefetch_related(
            'authors',
            'genres'
        ),
        pk=pk
    )

    reading_shelf = None

    if request.user.is_authenticated:
        reading_shelf = ReadingShelf.objects.filter(
            user=request.user,
            book=book
        ).first()

    context = {
        'book': book,
        'reading_shelf': reading_shelf,
    }

    return render(
        request,
        'books/book_detail.html',
        context
    )
