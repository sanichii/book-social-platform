from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Follow
from books.models import ReadingShelf
from posts.models import Post

User = get_user_model()


@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        messages.warning(request, "You cannot follow yourself.")
        return redirect('interactions:user_profile', username=username)

    if request.method == 'POST':
        follow_obj = Follow.objects.filter(follower=request.user, following=target_user).first()
        if follow_obj:
            follow_obj.delete()
            messages.info(request, f"Unfollowed @{target_user.username}.")
        else:
            Follow.objects.create(follower=request.user, following=target_user)
            messages.success(request, f"You are now following @{target_user.username}!")

    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def user_public_profile(request, username):
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    followers_count = profile_user.followers_set.count()
    following_count = profile_user.following_set.count()

    user_posts = Post.objects.filter(user=profile_user).select_related('book')
    user_shelves = ReadingShelf.objects.filter(user=profile_user).select_related('book')

    context = {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'user_posts': user_posts,
        'user_shelves': user_shelves,
    }
    return render(request, 'interactions/user_profile.html', context)


@login_required
def readers_list(request):
    readers = User.objects.select_related('profile').exclude(id=request.user.id)
    following_ids = set(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )
    context = {
        'readers': readers,
        'following_ids': following_ids,
    }
    return render(request, 'interactions/readers_list.html', context)