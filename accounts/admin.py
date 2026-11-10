from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Info'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [ProfileInline]
    list_display = [
        'email',
        'username',
        'subscription_tier',
        'is_verified_author',
        'is_staff',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            'Role & Subscription',
            {'fields': ('subscription_tier', 'is_verified_author')},
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_genre', 'created_at']
    search_fields = ['user__username', 'user__email', 'favorite_genre']