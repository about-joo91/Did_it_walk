import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from flask import jsonify
from .forms import *
from django.views.static import serve 
import os

# Create your views here.
def home(request):
    # user = request.user.is_authenticated
    # if user:
    #     return redirect('main')
    # else:
    #     return redirect('/user/sign_in')
    return redirect('/post/home')

def main(request):
    if request.method == 'POST':
        image = request.FILES.get('input_file', '')
        Post(post_img_url = image).save()
        return redirect('/post/home')


    elif request.method == 'GET':
        post_imgs = Post.objects.all()
        return render(request, 'post/main.html')

def show_image(request, obj_id):

    post_imgs = Post.objects.get(id=obj_id)
    image_path = post_imgs.post_img_url.path
    return serve(request, os.path.basename(image_path), os.path.dirname(image_path))