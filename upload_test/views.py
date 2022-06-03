from django.shortcuts import redirect, render
from .forms import *


# Create your views here.
def main(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UploadForm()
    return render(request, 'post_test/main.html',{'form':form})
