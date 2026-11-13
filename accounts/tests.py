from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Profile

User = get_user_model()


class AccountsTests(TestCase):
    def test_profile_created_automatically_on_user_creation(self):
        user = User.objects.create_user(
            username='reader1',
            email='reader1@example.com',
            password='StrongPassword123!'
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_login_and_profile_page_access(self):
        user = User.objects.create_user(
            username='reader2',
            email='reader2@example.com',
            password='StrongPassword123!'
        )
        self.client.login(email='reader2@example.com', password='StrongPassword123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)