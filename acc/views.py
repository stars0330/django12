from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password

def chpass(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        np = request.POST.get("npass")
        u.set_password(np)
        u.save()
        return redirect("acc:login")
    return redirect("acc:update")

def update(request):
    if request.method == "POST":
        u = request.user
        ue = request.POST.get("umail")
        uc = request.POST.get("ucom")
        up = request.FILES.get("upic")
        u.email, u.comment = ue, uc
        if up:
            u.pic.delete()
            u.pic = up
        u.save()
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def delete(request):
    u = request.user
    ck = request.POST.get("ck")
    if check_password(ck,u.password):
        u.pic.delete()
        u.delete()
        return redirect("acc:index")
    return redirect("acc:profile")

def profile(request):
    return render(request, "acc/profile.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucom")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
            return redirect("acc:login")
        except:
            pass # 마지막
    return render(request, "acc/signup.html")

def ulogout(request):
    logout(request)
    return redirect("acc:index")

def ulogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            return redirect("acc:index")
        else:
            pass # 마지막
    return render(request, "acc/login.html")

def index(request):
    context = {
        "dict" : {1:"one", 2:"two", 3:"three"}
    }
    return render(request, "acc/index.html")
