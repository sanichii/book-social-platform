from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class SubscriptionTier(models.TextChoices):
        FREE = 'FREE', 'Free'
        PREMIUM = 'PREMIUM', 'Premium'

    email = models.EmailField(unique=True, verbose_name="Email")
    subscription_tier = models.CharField(
        max_length=10,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE,
        verbose_name="Subscription Tier",
    )
    is_verified_author = models.BooleanField(
        default=False, verbose_name="Verified Author"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username