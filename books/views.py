
from django.shortcuts import render
from django.db.models import Q

from .models import Book, Genre


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
