from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method != "POST":
        return render(request, "auth/login.html", {"signinURL":"/users/signin_user"})
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if request.GET.get('next') == None:
            return redirect("/")
        return redirect(request.GET['next'])
    else:
        return redirect('/users/login_user')

def signin_user(request):
    if request.method != "POST":
        return render(request, "auth/signin.html", {"loginURL":"/users/login_user"})
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = User.objects.create_user(username, email, password)
    return redirect('/users/login_user')

@login_required(login_url='/users/login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='/users/login_user')
def delete_user(request):
    user = request.user
    user.delete()
    return redirect("/users/signin_user")






