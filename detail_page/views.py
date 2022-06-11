from django.shortcuts import render
from post.models import Post, PostImg
# Create your views here.
def detail_page(request, pk):
    post = Post.objects.get(pk = pk)
    return render(request, 'detail_page/detail_page.html', {'post' : post })