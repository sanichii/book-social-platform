
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='index'),

    path('users/', views.users_view, name='users'),
    path(
        'users/<int:user_id>/toggle-status/',
        views.toggle_user_status,
        name='toggle_user_status'
    ),

    path('books/', views.books_view, name='books'),
    path(
        'books/<int:book_id>/',
        views.book_detail_view,
        name='book_detail'
    ),
    path(
        'books/<int:book_id>/edit/',
        views.edit_book_view,
        name='edit_book'
    ),
    path(
        'books/<int:book_id>/delete/',
        views.delete_book_view,
        name='delete_book'
    ),

    path('posts/', views.posts_view, name='posts'),
    path(
        'posts/<int:post_id>/',
        views.post_detail_view,
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.delete_post_view,
        name='delete_post'
    ),
]
