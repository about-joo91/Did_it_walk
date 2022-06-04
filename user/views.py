from django.shortcuts import render, redirect
from django.contrib import auth
from .models import UserModel

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