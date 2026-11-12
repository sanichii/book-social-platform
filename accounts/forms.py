from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email address',
            }
        ),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input', 'placeholder': 'Choose a username'}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-input', 'placeholder': 'Enter your email'}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'placeholder': 'Enter your password'}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            self.user = user
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = self.instance.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.original_email:
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already taken.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Tell us about your reading interests...',
            }
        ),
    )
    favorite_genre = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Science Fiction, Classic Literature',
            }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = Profile
        fields = ['bio', 'favorite_genre', 'avatar']