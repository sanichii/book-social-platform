from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PostForm
from .models import Post
from interactions.models import Like


@login_required
def feed_view(request):
    post_type = request.GET.get('type', '')
    posts = (
        Post.objects.select_related('user', 'user__profile', 'book')
        .prefetch_related('likes', 'comments__user')
        .all()
    )

    if post_type in {'review', 'quote', 'thought'}:
        posts = posts.filter(post_type=post_type)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been shared!")
            return redirect('posts:feed')
    else:
        form = PostForm()

    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)
    )

    context = {
        'posts': posts,
        'form': form,
        'comment_form': CommentForm(),
        'liked_post_ids': liked_post_ids,
        'selected_type': post_type,
    }
    return render(request, 'posts/feed.html', context)


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added.")
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect('posts:feed')