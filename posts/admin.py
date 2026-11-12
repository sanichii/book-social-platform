from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'post_type', 'rating', 'created_at')
    list_filter = ('post_type', 'rating', 'created_at')
    search_fields = ('user__username', 'book__title', 'content')