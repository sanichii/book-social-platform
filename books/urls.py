
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('catalog/', views.book_catalog, name='book_catalog'),
]
