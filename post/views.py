from email import message
from certifi import contents
from django.shortcuts import render, redirect
from flask import jsonify, request_started
from django.views.static import serve 
import os
from .models import Post_Img, Post, Shoe_tag
from user.models import UserModel
from django.contrib import messages


# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/post/home')
    else:
        return redirect('/user/sign_in')

def main(request):
    if request.method == 'GET':
        user = request.user
        posts = Post.objects.filter(user = user)
        post_images = [Post_Img.objects.get(post = post).id for post in posts]
        
        shoe_tags = []
        for post in posts:
            shoe_tag = post.shoe_tags.all()
            shoe_tags.append(*shoe_tag)
        for shoe_tag in shoe_tags:
            print("shoe_tag : ", shoe_tag.tag_title)
        
        all_shoe_list = []
        all_shoes = Shoe_tag.objects.all()
        for a in all_shoes:
            all_shoe_list.append(a)

        
            

        post_user_ids_list = [UserModel.objects.filter(id=post.user_id) for post in posts]
        post_user_ids_datas = []
        for post_user_ids in post_user_ids_list:
            for post_user_id in post_user_ids:
                post_user_ids_datas.append(post_user_id)

        post_shoe_list = zip(post_images, shoe_tags, posts, post_user_ids_datas)
        
        context={
            'post_shoe_list' : post_shoe_list,
            'all_shoe_list' : all_shoe_list
            }

        return render(request, 'post/main.html', context)


    elif request.method == 'POST':
        user_data = request.user
        input_image = request.FILES.get('input_file', '')
        input_content = request.POST.get('input_content')
        input_tag_title = request.POST.get('input_tag_title')
        if input_image and input_content and input_tag_title:
            
            post_info = Post(contents = input_content, user = user_data)
            post_info.save()

            shoe_tag_by_title = Shoe_tag.objects.get(tag_title=input_tag_title)
            post_info.shoe_tags.add(shoe_tag_by_title)
            post_info.save()

            Post_Img_info = Post_Img(post = post_info, post_img = input_image)
            Post_Img_info.save()

            return redirect('/post/home')
        else : 
            messages.info(request, 'image나 content가 비어있습니다.')
            return render(request, 'post/main.html',)

    
def show_image(request, obj_id):
    post_imgs = Post_Img.objects.get(id=obj_id)
    image_path = post_imgs.post_img.path
    return serve(request, os.path.basename(image_path), os.path.dirname(image_path))