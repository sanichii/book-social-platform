
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import CustomUser
from books.forms import BookForm
from books.models import Book, Genre, ReadingShelf
from posts.models import Post


@login_required(login_url='accounts:login')
def dashboard_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    context = {
        'total_users': CustomUser.objects.count(),
        'total_books': Book.objects.count(),
        'total_posts': Post.objects.count(),
        'total_reading_shelves': ReadingShelf.objects.count(),
    }

    return render(request, 'dashboard/index.html', context)


@login_required(login_url='accounts:login')
def analytics_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    today = timezone.localdate()
    start_date = today - timedelta(days=6)

    new_users_count = CustomUser.objects.filter(
        date_joined__date__gte=start_date,
        date_joined__date__lte=today
    ).count()

    daily_posts = []

    for day_offset in range(7):
        current_day = start_date + timedelta(days=day_offset)

        posts_count = Post.objects.filter(
            created_at__date=current_day
        ).count()

        daily_posts.append({
            'date': current_day,
            'count': posts_count,
        })

    popular_books = Book.objects.annotate(
        shelf_count=Count('reading_shelves')
    ).filter(
        shelf_count__gt=0
    ).order_by(
        '-shelf_count',
        'title'
    )[:5]

    shelf_status_counts = {
        status: 0
        for status, label in ReadingShelf.STATUS_CHOICES
    }

    shelf_stats = ReadingShelf.objects.values(
        'status'
    ).annotate(
        total=Count('id')
    )

    for item in shelf_stats:
        shelf_status_counts[item['status']] = item['total']

    shelf_statuses = [
        {
            'value': status,
            'label': label,
            'count': shelf_status_counts[status],
        }
        for status, label in ReadingShelf.STATUS_CHOICES
    ]

    context = {
        'new_users_count': new_users_count,
        'daily_posts': daily_posts,
        'popular_books': popular_books,
        'shelf_statuses': shelf_statuses,
        'start_date': start_date,
        'today': today,
    }

    return render(request, 'dashboard/analytics.html', context)


@login_required(login_url='accounts:login')
def users_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    search_query = request.GET.get('search', '').strip()
    subscription_filter = request.GET.get('subscription', '')

    users = CustomUser.objects.all().order_by('-date_joined')

    if search_query:
        users = users.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )

    if subscription_filter in ['FREE', 'PREMIUM']:
        users = users.filter(
            subscription_tier=subscription_filter
        )

    context = {
        'users': users,
        'search_query': search_query,
        'subscription_filter': subscription_filter,
    }

    return render(request, 'dashboard/users.html', context)


@login_required(login_url='accounts:login')
def books_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    search_query = request.GET.get('search', '').strip()
    genre_filter = request.GET.get('genre', '')

    books = Book.objects.prefetch_related(
        'authors',
        'genres'
    ).all()

    if search_query:
        books = books.filter(
            models.Q(title__icontains=search_query) |
            models.Q(authors__first_name__icontains=search_query) |
            models.Q(authors__last_name__icontains=search_query) |
            models.Q(isbn__icontains=search_query)
        ).distinct()

    if genre_filter.isdigit():
        books = books.filter(
            genres__id=int(genre_filter)
        ).distinct()

    genres = Genre.objects.all()

    context = {
        'books': books,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
    }

    return render(request, 'dashboard/books.html', context)


@login_required(login_url='accounts:login')
def book_detail_view(request, book_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    try:
        book = Book.objects.prefetch_related(
            'authors',
            'genres'
        ).get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('dashboard:books')

    context = {
        'book': book,
    }

    return render(request, 'dashboard/book_detail.html', context)


@login_required(login_url='accounts:login')
def edit_book_view(request, book_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('dashboard:books')

    if request.method == 'POST':
        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Book updated successfully."
            )
            return redirect(
                'dashboard:book_detail',
                book_id=book.id
            )
    else:
        form = BookForm(instance=book)

    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'dashboard/edit_book.html', context)


@login_required(login_url='accounts:login')
@require_POST
def delete_book_view(request, book_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to perform this action."
        )
        return redirect('posts:feed')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('dashboard:books')

    book_title = book.title
    book.delete()

    messages.success(
        request,
        f"Book '{book_title}' deleted successfully."
    )

    return redirect('dashboard:books')


@login_required(login_url='accounts:login')
def posts_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    search_query = request.GET.get('search', '').strip()
    post_type_filter = request.GET.get('post_type', '')

    posts = Post.objects.select_related(
        'user',
        'book'
    ).all()

    if search_query:
        posts = posts.filter(
            models.Q(content__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(book__title__icontains=search_query)
        )

    valid_post_types = [
        'review',
        'quote',
        'thought',
    ]

    if post_type_filter in valid_post_types:
        posts = posts.filter(
            post_type=post_type_filter
        )

    context = {
        'posts': posts,
        'search_query': search_query,
        'post_type_filter': post_type_filter,
    }

    return render(request, 'dashboard/posts.html', context)


@login_required(login_url='accounts:login')
def post_detail_view(request, post_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    try:
        post = Post.objects.select_related(
            'user',
            'book'
        ).get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect('dashboard:posts')

    context = {
        'post': post,
    }

    return render(request, 'dashboard/post_detail.html', context)


@login_required(login_url='accounts:login')
@require_POST
def delete_post_view(request, post_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to perform this action."
        )
        return redirect('posts:feed')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect('dashboard:posts')

    post.delete()

    messages.success(
        request,
        "Post deleted successfully."
    )

    return redirect('dashboard:posts')


@login_required(login_url='accounts:login')
@require_POST
def toggle_user_status(request, user_id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to perform this action."
        )
        return redirect('posts:feed')

    try:
        target_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('dashboard:users')

    if target_user.id == request.user.id:
        messages.error(
            request,
            "You cannot change your own account status."
        )
        return redirect('dashboard:users')

    if target_user.is_superuser and not request.user.is_superuser:
        messages.error(
            request,
            "You cannot change a superuser's status."
        )
        return redirect('dashboard:users')

    target_user.is_active = not target_user.is_active
    target_user.save(update_fields=['is_active'])

    messages.success(
        request,
        f"User {target_user.username} status updated successfully."
    )

    return redirect('dashboard:users')


# Staff Management

@login_required(login_url='accounts:login')
def staff_view(request):
    if not request.user.is_superuser:
        messages.error(
            request,
            "Only superusers can manage staff accounts."
        )
        return redirect('dashboard:index')

    staff_users = CustomUser.objects.filter(
        is_staff=True
    ).order_by('-date_joined')

    context = {
        'staff_users': staff_users,
    }

    return render(request, 'dashboard/staff.html', context)


@login_required(login_url='accounts:login')
@require_POST
def toggle_staff_status(request, user_id):
    if not request.user.is_superuser:
        messages.error(
            request,
            "Only superusers can change staff permissions."
        )
        return redirect('dashboard:index')

    try:
        target_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('dashboard:staff')

    if target_user.id == request.user.id:
        messages.error(
            request,
            "You cannot change your own staff permissions."
        )
        return redirect('dashboard:staff')

    if target_user.is_superuser:
        messages.error(
            request,
            "You cannot change another superuser's staff permissions."
        )
        return redirect('dashboard:staff')

    target_user.is_staff = not target_user.is_staff
    target_user.save(update_fields=['is_staff'])

    messages.success(
        request,
        f"Staff permissions for {target_user.username} updated successfully."
    )

    return redirect('dashboard:staff')


# Verified Authors

@login_required(login_url='accounts:login')
def verified_authors_view(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access this page."
        )
        return redirect('posts:feed')

    search_query = request.GET.get('search', '').strip()

    verified_authors = CustomUser.objects.filter(
        is_verified_author=True
    ).order_by('username')

    if search_query:
        verified_authors = verified_authors.filter(
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )

    context = {
        'verified_authors': verified_authors,
        'search_query': search_query,
    }

    return render(
        request,
        'dashboard/verified_authors.html',
        context
    )
