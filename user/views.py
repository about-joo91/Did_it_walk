from django.shortcuts import render, redirect
from django.contrib import auth
from .models import UserModel
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('new_username',None)
        password = request.POST.get('new_password',None)
        nickname = request.POST.get('nickname',None)
        new_user = UserModel.objects.create_user(
            username = username,
            password = password,
            nickname = nickname
        )
        new_user.save()
        return redirect('/user/sign_in/')
    return render(request, 'user/sign_up.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        me = auth.authenticate(request, username = username, password= password)
        if me:
            auth.login(request, me)
            return render(request,'success.html',{'msg' : '성공'})
        return render(request, 'success.html', {'msg': '아이디/비밀번호를 확인하세요'})
    return render(request, 'user/sign_in.html')

@login_required
def sign_out(request):
    auth.logout(request)
    return render(request, 'success.html',{'msg': '로그아웃 됨'})

@login_required
def follow_page(request):
    cur_user = request.user
    user_list = UserModel.objects.all().exclude(username = cur_user.username).exclude(followee=cur_user)
    followers = UserModel.objects.filter(followee = cur_user)
    return render(request, 'user/follower.html', {'users':user_list,'followers':followers})