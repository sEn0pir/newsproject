from django.shortcuts import render
from .models import Post


def news_list(request):
    news = Post.objects.filter(post_type='NW').order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})

from django.shortcuts import get_object_or_404

def news_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'news/news_detail.html', {'post': post})

