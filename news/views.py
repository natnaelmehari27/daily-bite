from django.shortcuts import render, redirect
from .models import NewsPost 
from .forms import NewsPostForm
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