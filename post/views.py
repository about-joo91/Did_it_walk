from django.shortcuts import render, redirect
from user.views import follow
from .models import PostImg, Post, Likes, ShoeTag, Comments
from user.models import UserModel
from django.contrib import messages
import boto3
import os

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/post/home/recent')
    else:
        return redirect('/user/sign_in')
    
def main(request, page_name = 'recent'):
    if request.method == 'GET':
        all_shoe_list = ShoeTag.objects.all()
        if page_name == "recent":
            total_datas = recent_post_data(request.user)
            

        elif page_name == "following":
            total_datas = following_post_data(request.user)

        else:
            total_datas = suggest_post_data()

        context={
                'total_datas' : total_datas,
                "all_shoe_list" : all_shoe_list
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
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'])
    s3.put_object(
        ACL="public-read",
        Bucket = config.BUCKET_NAME,
        Body = file,
        Key = filename,
        ContentType = content_type
    )
    return f'https://diditwalk.s3.ap-northeast-2.amazonaws.com/{filename}'

def recent_post_data(user):

    recent_posts = Post.objects.all()
    shoe_tags = []
    is_like_list = []
    all_like_list = []
    comment_list = []
    
    for post in recent_posts:
        shoe_tag = post.shoe_tags.all()
        shoe_tags.append(*shoe_tag)
        is_like_list.append(Likes.objects.filter(user = user, post = post).exists())
        all_like_list.append(len(Likes.objects.filter(post_id = post.id)))
        comment_list.append(len(Comments.objects.filter(post = post)))
    
    total_datas = zip(recent_posts, shoe_tags, is_like_list, all_like_list, comment_list)
    return total_datas

def following_post_data(user):
    following_posts = following(user)

    shoe_tags = []
    is_like_list = []
    all_like_list = []
    comment_list = []
    for post in following_posts:
        shoe_tag = post.shoe_tags.all()
        shoe_tags.append(*shoe_tag)
        is_like_list.append(Likes.objects.filter(user = user, post = post).exists())
        all_like_list.append(len(Likes.objects.filter(post_id = post.id)))
        comment_list.append(len(Comments.objects.filter(post = post)))

    total_datas = zip(following_posts, shoe_tags, is_like_list, all_like_list, comment_list)
    return total_datas

def suggest_post_data(request):
    total_datas = []
    return total_datas

def following(user):
    my_follows= UserModel.objects.filter(followee = user)
    my_follows_posts_list = []
    for my_follow in my_follows:
        my_follows_posts = Post.objects.get(user_id = my_follow.id)
        my_follows_posts_list.append(my_follows_posts)

    return my_follows_posts_list


def like(request, post_id):
    if request.method == 'POST':
        cur_user = request.user
        post = Post.objects.get(id= post_id)
        like_obj, create = Likes.objects.get_or_create(user= cur_user, post = post)
        if not create:
            like_obj.delete()
        else:
            pass
        return redirect('/')
        
def comment(request, post_id, comment_id = None):
    content = request.POST.get('comment_input')
    if comment_id:
        Comments.objects.get(id = comment_id).delete()
    else:
        cur_user = request.user
        post = Post.objects.get(id = post_id)
        new_comment = Comments.objects.create(post=post, user = cur_user, content = content)
        new_comment.save()
    return redirect('/detail_page/'+ str(post_id))

def comment_edit(request, comment_id):
    new_content = request.POST.get('edit_box')
    comment = Comments.objects.filter(id = comment_id)
    comment.update(content = new_content)
    post_id = comment[0].post.id
    return redirect('/detail_page/'+str(post_id))