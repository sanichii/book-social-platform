from django import forms
from .models import Post
from interactions.models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['book', 'post_type', 'content', 'rating', 'image']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share a quote, review, or thought about this book...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': '1 to 5 (optional)',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write a comment...',
            }),
        }