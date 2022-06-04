from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    # user = request.user.is_authenticated
    # if user:
    #     return redirect('main')
    # else:
    #     return redirect('/user/sign_in')
    return redirect('main')

def main(request):
    return render(request, 'post/main.html')