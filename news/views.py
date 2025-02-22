from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsPost, comment
from .forms import NewsPostForm, CommentForm 
# Create your views here.

def news_list(request):
    posts = NewsPost.objects.all().order_by('-date_posted')
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