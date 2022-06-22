import json
from django.shortcuts import render, redirect
from .models import PostImg, Post, Likes, ShoeTag, Comments
from user.models import UserModel
from django.contrib import messages
import config
import boto3
from shoes_tag.recommand_md import recommendation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/post/home/recent')
    else:
        return redirect('/user/sign_in')
    
def main(request, page_name = 'recent'):
    user = request.user
    if request.method == 'GET':
        all_shoe_list = ShoeTag.objects.all()
        
        if page_name == "recent":
            total_datas = recent_post_data(request.user)
        elif page_name == "following":
            total_datas = following_post_data(request.user)

        else:
            total_datas = suggest_post_data(request.user)

        recent_posts = Post.objects.filter(user=user).order_by('-created_at')[:3]
        suggest_shoe_tags = []
        suggest_posts=[]
        for recent_post in recent_posts:
            shoe_tag = recent_post.shoe_tags.all()
            suggest_shoes_ids = recommendation.find_shoes_recommend(shoe_tag[0].id)
            for suggest_shoe_id in suggest_shoes_ids:
                str_suggest_shoe_id = str(suggest_shoe_id)
                new_shoe_tag = ShoeTag.objects.get(id = str_suggest_shoe_id)
                suggest_shoe_tags.append(new_shoe_tag)
                suggest_posts += Post.objects.filter(shoe_tags = new_shoe_tag)
                
        if len(suggest_shoe_tags) < 9:
            suggest_shoe_tags = [ShoeTag.objects.get(id = x) for x in range(1,10)]
            

        context={
                'total_datas' : total_datas,
                "all_shoe_list" : all_shoe_list,
                "suggest_shoe_tags": suggest_shoe_tags
                }
        return render(request, 'post/main_post.html', context)

    elif request.method == "POST":
        user_data = request.user
        input_image = request.FILES.get('input_file', '')
        input_content = request.POST.get('input_content')
        input_tag_title = request.POST.get('input_tag_title')
        
        if input_image and input_content and input_tag_title:
            splited_file = str(input_image).split('.')
            filename , content_type = splited_file[0], splited_file[1]
            image_url = upload_file(input_image, filename, content_type)
        
            Post_Img_info = PostImg(post_img = image_url)
            Post_Img_info.save()

            shoe_tag_by_title = ShoeTag.objects.filter(tag_title=input_tag_title)[0]
            post_info = Post.objects.create(
                contents = input_content,
                user = user_data,
                post_img = Post_Img_info,
                )
            post_info.shoe_tags.add(shoe_tag_by_title)
            post_info.save()
            return redirect('/post/home/recent')
        else : 
            messages.info(request, 'image나 content가 비어있습니다.')
            return render(request, 'post/main_base.html')

def upload_file(file, filename, content_type):
    s3 = boto3.client('s3',
    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY)
    s3.put_object(
        ACL="public-read",
        Bucket = config.BUCKET_NAME,
        Body = file,
        Key = filename,
        ContentType = content_type
    )
    return f'https://diditwalk.s3.ap-northeast-2.amazonaws.com/{filename}'

def recent_post_data(user):

    recent_page_posts = Post.objects.all().order_by('-created_at')
    shoe_tags = []
    is_like_list = []
    all_like_list = []
    comment_list = []
    is_following_list = []

    recent_posts = Post.objects.filter(user=user).order_by('-created_at')[:3]
    suggest_shoe_tags = []
    suggest_posts = []
    for recent_post in recent_posts:
        shoe_tag = recent_post.shoe_tags.all()
        suggest_shoes = recommendation.find_shoes_recommend(shoe_tag[0].id)
        for suggest_shoe in suggest_shoes:
            suggest_shoe_id = str(suggest_shoe)
            new_shoe_tag = ShoeTag.objects.get(id = suggest_shoe_id)
            suggest_shoe_tags.append(new_shoe_tag)
            suggest_posts += Post.objects.filter(shoe_tags = new_shoe_tag)

    
    for post in recent_page_posts:
        shoe_tag = post.shoe_tags.all()
        shoe_tags.append(*shoe_tag)
        is_like_list.append(Likes.objects.filter(user = user, post = post).exists())
        all_like_list.append(len(Likes.objects.filter(post_id = post.id)))
        comment_list.append(len(Comments.objects.filter(post = post)))
        is_following_list.append(UserModel.objects.filter(followee = user).filter(id=post.user.id).exists())

    total_datas = zip(recent_page_posts, shoe_tags, is_like_list, all_like_list, comment_list, is_following_list)
    return total_datas

def following_post_data(user):
    my_follows= UserModel.objects.filter(followee = user)
    following_posts = []
    for my_follow in my_follows:
        following_posts += Post.objects.filter(user_id = my_follow.id)

    recent_posts = Post.objects.filter(user=user).order_by('-created_at')[:3]
    suggest_shoe_tags = []
    suggest_posts = []
    for recent_post in recent_posts:
        shoe_tag = recent_post.shoe_tags.all()
        suggest_shoes = recommendation.find_shoes_recommend(shoe_tag[0].id)
        for suggest_shoe in suggest_shoes:
            suggest_shoe_id = str(suggest_shoe)
            new_shoe_tag = ShoeTag.objects.get(id = suggest_shoe_id)
            suggest_shoe_tags.append(new_shoe_tag)
            suggest_posts += Post.objects.filter(shoe_tags = new_shoe_tag)

    shoe_tags = []
    is_like_list = []
    all_like_list = []
    comment_list = []
    is_following_list = []
    for post in following_posts:
        shoe_tag = post.shoe_tags.all()
        shoe_tags.append(*shoe_tag)
        is_like_list.append(Likes.objects.filter(user = user, post = post).exists())
        all_like_list.append(len(Likes.objects.filter(post_id = post.id)))
        comment_list.append(len(Comments.objects.filter(post = post)))
        is_following_list.append(UserModel.objects.filter(followee = user).filter(id=post.user.id).exists())

    total_datas = zip(following_posts, shoe_tags, is_like_list, all_like_list, comment_list, is_following_list)
    return total_datas

def suggest_post_data(user):

    suggest_posts = []
    shoe_tags = []
    is_like_list = []
    all_like_list = []
    comment_list = []
    is_following_list = []

    recent_posts = Post.objects.filter(user=user).order_by('-created_at')[:3]
    suggest_shoe_tags = []
    if len(recent_posts) <=3:
        suggest_shoe_tags = [ShoeTag.objects.get(id = x) for x in range(1,10)]
        for suggest_shoe_tag in suggest_shoe_tags:
            suggest_posts += Post.objects.filter(shoe_tags = suggest_shoe_tag)
    else:
        for recent_post in recent_posts:
            shoe_tag = recent_post.shoe_tags.all()
            suggest_shoes_ids = recommendation.find_shoes_recommend(shoe_tag[0].id)
            for suggest_shoe_id in suggest_shoes_ids:
                str_suggest_shoe_id = str(suggest_shoe_id)
                new_shoe_tag = ShoeTag.objects.get(id = str_suggest_shoe_id)
                suggest_shoe_tags.append(new_shoe_tag)
                suggest_posts += Post.objects.filter(shoe_tags = new_shoe_tag)

    for post in suggest_posts:
        shoe_tag = post.shoe_tags.all()
        shoe_tags.append(*shoe_tag)
        is_like_list.append(Likes.objects.filter(user = user, post = post).exists())
        all_like_list.append(len(Likes.objects.filter(post_id = post.id)))
        comment_list.append(len(Comments.objects.filter(post = post)))
        is_following_list.append(UserModel.objects.filter(followee = user).filter(id=post.user.id).exists())

    total_datas = zip(suggest_posts, shoe_tags, is_like_list, all_like_list, comment_list, is_following_list)
    return total_datas


class LikeView(APIView):
    def post(self, request,post_id):
        cur_user = request.user
        post = Post.objects.get(id= post_id)
        like_obj, create = Likes.objects.get_or_create(user= cur_user, post = post)
        if not create:
            like_obj.delete()
        return Response({},status=status.HTTP_200_OK)
    
class ComentView(APIView):
    def post(self, request, pk):
        cur_user = request.user
        new_content = request.data.get('content')
        print(new_content)
        post = Post.objects.get(pk = pk)
        new_comment = Comments.objects.create(post=post, user = cur_user, content = new_content)
        new_comment.save()
        return Response({},status=status.HTTP_200_OK)
    def put(self, request, pk):
        new_content = request.data.get('content')
        comment = Comments.objects.get(pk = pk)
        comment.content = new_content
        comment.save()
        return Response({},status=status.HTTP_200_OK)
    def delete(self, request,pk):
        delete_comment = Comments.objects.get(pk = pk)
        delete_comment.delete()
        return Response({},status=status.HTTP_200_OK)

def edit_content(request, post_id):
    new_content = request.POST.get('edit_content_text')
    post = Post.objects.filter(id = post_id)
    post.update(contents= new_content)

    return redirect('/post/home/recent')

def delete_content(request, post_id):
    delete_post = Post.objects.get(id = post_id)
    delete_post.delete()

    return redirect('/post/home/recent')


