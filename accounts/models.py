from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True,
        verbose_name="Avatar Image",
    )
    favorite_genre = models.CharField(
        max_length=100, blank=True, verbose_name="Favorite Genre"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()