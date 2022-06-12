from django.shortcuts import render
from post.models import Post, PostImg, ShoeTag
# Create your views here.
def detail_page(request, pk):
    post = Post.objects.get(pk = pk)
    shoe_tag = ShoeTag.objects.get(shoe_taggie = post)
    post_info = {
        post : shoe_tag
    }
    return render(request, 'detail_page/detail_page.html', {'post_info' : post_info})