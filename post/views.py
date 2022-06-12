from django.shortcuts import render, redirect
from django.views.static import serve 
import os
from user.views import follow
from .models import PostImg, Post, ShoeTag, Likes
from user.models import UserModel
from django.contrib import messages


# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/post/home/recent')
    else:
        return redirect('/user/sign_in')

def save_post(request):
    user_data = request.user
    input_image = request.FILES.get('input_file', '')
    input_content = request.POST.get('input_content')
    input_tag_title = request.POST.get('input_tag_title')
    if input_image and input_content and input_tag_title:
            
        Post_Img_info = PostImg(post_img = input_image)
        Post_Img_info.save()

        post_info = Post(contents = input_content, user = user_data, post_img = Post_Img_info)
        post_info.save()

        shoe_tag_by_title = ShoeTag.objects.get(tag_title=input_tag_title)
        post_info.shoe_tags.add(shoe_tag_by_title)
        post_info.save()

        return redirect('/post/home')
    else : 
        messages.info(request, 'image나 content가 비어있습니다.')
        return render(request, 'post/main_recent.html')


def following(request):
    my_user = request.user
    my_follows= UserModel.objects.filter(followee = my_user)
    my_follows_posts_list = []
    for my_follow in my_follows:
        my_follows_posts = Post.objects.get(user_id = my_follow.id)
        my_follows_posts_list.append(my_follows_posts)

    return my_follows_posts_list


def main_data(request):
    user = request.get("request").user
    
    if request.get("page_name") == "recent":
        recent_posts = Post.objects.all()
        recent_data = recent_posts

        shoe_tags = []
        for post in recent_posts:
            shoe_tags = post.shoe_tags.all()

        return recent_data, shoe_tags

    elif request.get("page_name") == "following":
        following_posts = following(request.get("request"))

        shoe_tags = []
        for post in following_posts:
            shoe_tags = post.shoe_tags.all()

        return following_posts, shoe_tags


def main(request, page_name):
    if request.method == 'GET':
        send_data = {"request" : request, "page_name" : page_name}
        posts, shoe_tags = main_data(send_data)
        total_datas = zip(posts, shoe_tags)
        all_shoe_list = ShoeTag.objects.all()
        context={
                'total_datas' : total_datas,
                "all_shoe_list" : all_shoe_list
                }
        return render(request, 'post/main_post.html', context)
        
    elif request.method == "POST":
        save_post(request)
        return redirect("/post/home/recent")


def show_image(request, obj_id):
    post_imgs = PostImg.objects.get(id=obj_id)
    image_path = post_imgs.post_img.path
    return serve(request, os.path.basename(image_path), os.path.dirname(image_path))

def like(request, post_id):
    if request.method == 'POST':
        cur_user = request.user
        new_like, created = Likes.objects.get_or_create(user= cur_user, post__id = post_id)
        if not created:
            new_like.delete()
        else:
            pass
        return redirect('/')