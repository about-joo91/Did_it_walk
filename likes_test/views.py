from django.shortcuts import redirect, render
from post.models import Post
from .models import Likes
# Create your views here.

def likes_test(request, post_id = None):
    if request.method == 'GET':
        posts = Post.objects.all()
        cur_user = request.user
        # shoe_tags = []
        # for post in posts:
        #     shoe_tag = post.shoe_tags.all()
        #     shoe_tags.append(*shoe_tag)
        likes = [Likes.objects.filter(post = post, user = cur_user).exists() for post in posts]
        post_infos = zip(posts, likes)
        context={
            'post_infos' : post_infos,
            }
        return render(request, 'likes_test/index.html',context)
    elif request.method == 'POST':
        cur_user = request.user
        post = Post.objects.get(id = post_id)
        new_like, created = Likes.objects.get_or_create(user= cur_user, post = post)
        if not created:
            new_like.delete()
        else:
            pass
        return redirect('/likes_test/')
    