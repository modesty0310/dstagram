from django.shortcuts import render
from django.contrib.auth.models import User


def signup(request):
    if request.method == "POST":
        usrename = request.POST.get("username")
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 유저 객체 생성
        user = User()
        user.username = usrename
        user.set_password(password)
        user.save()
        return render(request, 'accounts/signup_complete.html')
    else:
        return render(request, 'accounts/signup.html')
