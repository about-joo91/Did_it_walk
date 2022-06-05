from django.shortcuts import render, redirect
from .forms import *

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
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/post/home')
    elif request.method == 'GET':
        form = UploadForm()
    return render(request, 'post/main.html',{'form':form})