
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'genres',
            'isbn',
            'cover_image',
            'publication_year',
            'summary',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
            }),
            'authors': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN',
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication year',
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter book summary',
            }),
        }
