from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('catalog/', views.book_catalog, name='book_catalog'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]