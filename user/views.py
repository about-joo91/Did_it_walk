import boto3
import config

from django.shortcuts import render, redirect
from django.contrib import auth
from .models import UserModel
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from post.models import Post, ShoeTag
from .serializers import UserSerializer

# Create your views here.


class UserCotrol(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def sign_up(request):
    return render(request, 'user/sign_up.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        me = auth.authenticate(request, username = username, password= password)
        if me:
            auth.login(request, me)
            return redirect('/')
        return render(request, 'user/sign_in.html', {'error': '아이디/비밀번호를 확인하세요'})
    return render(request, 'user/sign_in.html')

@login_required
def sign_out(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile_page(request):
    cur_user = request.user
    shoe_tag_rec = ShoeTag.objects.filter(shoe_taggie__user = cur_user)
    followers = UserModel.objects.filter(followee = cur_user)
    foloowees = UserModel.objects.filter(follow = cur_user)
    my_posts = Post.objects.filter(user = cur_user)
    return render(request, 'user/profile.html', {'follwees':foloowees,'followers':followers, 'shoe_tag_rec' : shoe_tag_rec, 'my_posts':my_posts})


@login_required
def follow(request, nickname):
    cur_user = request.user
    clicked_user = UserModel.objects.get(nickname=nickname)
    check_followee = UserModel.objects.filter(followee = cur_user).filter(nickname = nickname)
    if check_followee:
        clicked_user.followee.remove(cur_user)
    else:
        clicked_user.followee.add(cur_user)
    return redirect("/post/home/recent")

@login_required
def profile_upload(request):
    img = request.FILES['image']
    cur_user = request.user
    s3 = boto3.client('s3',
    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
    )
    splited_file = str(img).split('.')
    filename , content_type = splited_file[0], splited_file[1]
    if 'diditwalk' in cur_user.profile_url:
        file_name_before = cur_user.profile_url.split('/')[-1]
        s3.delete_object(
            Bucket = config.BUCKET_NAME,
            Key = file_name_before)
    s3.put_object(
    ACL="public-read",
    Bucket = config.BUCKET_NAME,
    Body = img,
    Key = filename,
    ContentType = content_type
    )
    cur_user.profile_url = f'https://diditwalk.s3.ap-northeast-2.amazonaws.com/{filename}'
    cur_user.save()
    return redirect('/user/profile')