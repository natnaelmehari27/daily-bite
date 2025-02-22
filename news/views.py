from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsPost, Comment
from .forms import NewsPostForm, CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
# Create your views here.

def news_list(request):
    posts = NewsPost.objects.annotate(
        like_count=Count('likes', filter=Q(likes__like_type=1)),
        dislike_count=Count('likes', filter=Q(likes__like_type=-1))
    ).order_by('-date_posted')
    return render(request, 'news/news_list.html', {'posts': posts})

def create_news_post(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsPostForm()
    return render(request, 'news/create_news_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(NewsPost, id=post_id)
    comments = post.comments.all().order_by('-date_posted')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'news/post_detail.html', context)

@require_POST
def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=403)

    post = get_object_or_404(NewsPost, id=post_id)
    action = request.POST.get('action')
    if action not in ['like', 'dislike']:
        return JsonResponse({'error': 'Invalid action.'}, status=400)

    like_type = 1 if action == 'like' else -1
    like_obj, created = Like.objects.get_or_create(user=request.user, post=post, defaults={'like_type': like_type})

    if not created:
        if like_obj.like_type == like_type:
            like_obj.delete()  # Toggle off
        else:
            like_obj.like_type = like_type
            like_obj.save()
    
    like_count = post.likes.filter(like_type=1).count()
    dislike_count = post.likes.filter(like_type=-1).count()
    return JsonResponse({'like_count': like_count, 'dislike_count': dislike_count})