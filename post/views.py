from email import message
from certifi import contents
from django.shortcuts import render, redirect
from flask import jsonify, request_started
from django.views.static import serve 
import os
from .models import Post_Img, Posts
from django.contrib import messages


# Create your views here.
def home(request):
    # user = request.user.is_authenticated
    # if user:
    #     return redirect('main')
    # else:
    #     return redirect('/user/sign_in')
    return redirect('/post/home')

def main(request):
    if request.method == 'GET':
        post_imgs = Post_Img.objects.all()
        return render(request, 'post/main.html',{'post_imgs' : post_imgs})

    elif request.method == 'POST':
        user = request.user.is_authenticated
        if user :
            user_data = request.user
            input_image = request.FILES.get('input_file', '')
            input_content = request.POST.get('input_content')
            if input_image and input_content :
                Posts_info = Posts(contents = input_content, users = user_data)
                Posts_info.save()
                Post_Img(posts = Posts_info, post_img_url = input_image).save
                
                return redirect('/post/home')
            else : 
                messages.info(request, 'image나 content가 비어있습니다.')
                return render(request, 'post/main.html')

        return redirect("/user/sign_in")

    

def show_image(request, obj_id):
    post_imgs = Post_Img.objects.get(id=obj_id)
    image_path = post_imgs.post_img_url.path
    return serve(request, os.path.basename(image_path), os.path.dirname(image_path))