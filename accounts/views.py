from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib import messages


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('tracker_home')  # Redirect to home if logged in
    return redirect('login')  # Redirect to login page if not logged in

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")
    
    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("tracker_home")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("logged_out")

@login_required
def home(request):
    return redirect("tracker_home")


def logged_out(request):
    return render(request, "logged_out.html")
