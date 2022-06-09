from django.shortcuts import redirect, render
from post.models import Post, Post_Img
from .models import Likes
# Create your views here.

def likes_test(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        cur_user = request.user
        post_images = [Post_Img.objects.get(post = post).id for post in posts]
        shoe_tags = []
        for post in posts:
            shoe_tag = post.shoe_tags.all()
            shoe_tags.append(*shoe_tag)
        likes = [Likes.objects.filter(post = post, user = cur_user).exists() for post in posts]
        post_infos = zip(post_images, shoe_tags, likes)
        context={
            'post_infos' : post_infos,
            }
        return render(request, 'likes_test/index.html',context)
def like_post(request ,post_id):
    cur_user = request.user
    post = Post.objects.get(id = post_id)
    new_like, created = Likes.objects.get_or_create(user= cur_user, post = post)
    if not created:
        new_like.delete()
    else:
        pass
    return redirect('/likes_test/')